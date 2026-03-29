from flask import Flask, request, render_template, send_file
from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO
from rembg import remove, new_session

app = Flask(__name__)

# Initialize the lightweight model session globally so it loads once
rembg_session = new_session("u2netp")

@app.route("/")
def index():
    return render_template("index.html")


def process_single_image(input_image_bytes, bg_color_name="white", brightness=1.0, contrast=1.0, saturation=1.0):
    """Process image locally with rembg for background removal."""
    img = Image.open(BytesIO(input_image_bytes))

    # Apply Image Adjustments
    if brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if saturation != 1.0:
        img = ImageEnhance.Color(img).enhance(saturation)

    # Remove background using the lightweight local ML model (u2netp)
    img = remove(img, session=rembg_session)

    # Apply lightweight sharpening to replace Cloudinary's enhancement
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)  # 1.5 adds a crispness without over-processing

    # Map color names to RGB
    color_map = {
        "white": (255, 255, 255),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0)
    }
    bg_color_rgb = color_map.get(bg_color_name.lower(), (255, 255, 255))

    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, bg_color_rgb)
        background.paste(img, mask=img.split()[-1])
        processed_img = background
    else:
        processed_img = img.convert("RGB")

    return processed_img


@app.route("/process", methods=["POST"])
def process():
    print("==== /process endpoint hit ====")

    # Layout settings
    passport_width = int(request.form.get("width", 390))
    passport_height = int(request.form.get("height", 480))
    border = int(request.form.get("border", 2))
    spacing = int(request.form.get("spacing", 10))
    bg_color = request.form.get("bgColor", "white")
    brightness = float(request.form.get("brightness", 1.0))
    contrast = float(request.form.get("contrast", 1.0))
    saturation = float(request.form.get("saturation", 1.0))
    margin_x = 10
    margin_y = 10
    horizontal_gap = 10
    a4_w, a4_h = 2480, 3508

    # Collect images and their settings
    images_data = []

    i = 0
    while f"image_{i}" in request.files:
        file = request.files[f"image_{i}"]
        copies = int(request.form.get(f"copies_{i}", 6))
        # Get individual filters, fallback to global or 1.0
        i_brightness = float(request.form.get(f"brightness_{i}", brightness))
        i_contrast = float(request.form.get(f"contrast_{i}", contrast))
        i_saturation = float(request.form.get(f"saturation_{i}", saturation))
        
        images_data.append({
            "bytes": file.read(),
            "copies": copies,
            "brightness": i_brightness,
            "contrast": i_contrast,
            "saturation": i_saturation
        })
        i += 1

    # Fallback to single image mode
    if not images_data and "image" in request.files:
        file = request.files["image"]
        copies = int(request.form.get("copies", 6))
        images_data.append({
            "bytes": file.read(),
            "copies": copies,
            "brightness": brightness,
            "contrast": contrast,
            "saturation": saturation
        })

    if not images_data:
        return "No image uploaded", 400

    print(f"DEBUG: Processing {len(images_data)} image(s)")

    # Process all images
    passport_images = []
    for idx, data in enumerate(images_data):
        print(f"DEBUG: Processing image {idx + 1} with {data['copies']} copies")
        try:
            img = process_single_image(
                data["bytes"], 
                bg_color, 
                data["brightness"], 
                data["contrast"], 
                data["saturation"]
            )
            img = img.resize((passport_width, passport_height), Image.LANCZOS)
            img = ImageOps.expand(img, border=border, fill="black")
            passport_images.append((img, data["copies"]))
        except ValueError as e:
            err_str = str(e)
            if "410" in err_str or "face" in err_str.lower():
                return {"error": "face_detection_failed"}, 410
            elif "429" in err_str or "quota" in err_str.lower():
                return {"error": "quota_exceeded"}, 429
            else:
                print(err_str)
                return {"error": err_str}, 500
                

    paste_w = passport_width + 2 * border
    paste_h = passport_height + 2 * border

    # Build all pages
    pages = []
    current_page = Image.new("RGB", (a4_w, a4_h), "white")
    x, y = margin_x, margin_y

    def new_page():
        nonlocal current_page, x, y
        pages.append(current_page)
        current_page = Image.new("RGB", (a4_w, a4_h), "white")
        x, y = margin_x, margin_y

    for passport_img, copies in passport_images:
        for _ in range(copies):
            # Move to next row if needed
            if x + paste_w > a4_w - margin_x:
                x = margin_x
                y += paste_h + spacing

            # Move to next page if needed
            if y + paste_h > a4_h - margin_y:
                new_page()

            current_page.paste(passport_img, (x, y))
            print(f"DEBUG: Placed at x={x}, y={y}")
            x += paste_w + horizontal_gap

    pages.append(current_page)
    print(f"DEBUG: Total pages = {len(pages)}")

    # Export multi-page PDF
    output = BytesIO()
    if len(pages) == 1:
        pages[0].save(output, format="PDF", dpi=(300, 300))
    else:
        pages[0].save(
            output,
            format="PDF",
            dpi=(300, 300),
            save_all=True,
            append_images=pages[1:],
        )
    output.seek(0)
    print("DEBUG: Returning PDF to client")

    return send_file(
        output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="passport-sheet.pdf",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)