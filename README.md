# 📸 Passport Photo Pro (Local Edition)

A premium, private, and local-first tool to generate print-ready passport photo sheets. No API keys, no external credits, and no images leave your machine.

---

## 🚀 Key Features

- **100% Local Processing** — No dependency on `remove.bg`, `Cloudinary`, or any external APIs.
- **AI Background Removal** — Powered by `rembg` (u2netp) running directly on your CPU.
- **Per-Photo Adjustments** — Fine-tune **Brightness, Contrast, and Saturation** for *each* photo individually.
- **Premium Sidebar UI** — A modern, glassmorphic sidebar layout that keeps controls accessible while editing.
- **In-Browser Cropping** — Perfectly align each photo to the required passport aspect ratio.
- **Smart Sharpening** — Automatic 1.5x sharpening for crisp, professional results.
- **Live Preview** — Visual feedback for adjustments reflects directly on each thumbnail.

---

## 🧰 Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | HTML5, Tailwind CSS, Particles.js   |
| Image Prep | Cropper.js (Local CSS Filters)      |
| Backend    | Python, Flask                       |
| Image AI   | `rembg` (U2NetP Lightweight)        |
| Processing | Pillow (PIL)                        |
| Server     | Gunicorn (Production Ready)         |

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.8+
- [Optional] Silicon Mac (M1/M2/M3) or any modern CPU.

### 2. Clone & Install
```bash
git clone https://github.com/your-username/passport-photo-pro.git
cd passport-photo-pro

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
# Activate the environment and run
source venv/bin/activate
python app.py

# Or run directly via venv python:
./venv/bin/python app.py
```

The server will start at `http://localhost:5001`.

---

## 📁 Project Structure

```
passport-photo-pro/
├── app.py                  # Flask backend — image processing & PDF generation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── templates/
│   └── index.html          # Frontend UI
└── README.md
```

---

## 📋 requirements.txt

Make sure your `requirements.txt` includes:

```
flask
pillow
rembg
```

Generate it automatically with:

```bash
pip freeze > requirements.txt
```

---

## 🖼️ How to Use

1. **Upload**: Drag and drop your photos. They will appear in a responsive grid.
2. **Select**: Click on any photo to "select" it (indicated by a blue border).
3. **Crop**: Use the **Crop** button on the selected card to frame your shot.
4. **Enhance**: Use the **Advanced Options** in the sidebar to adjust brightness/contrast for the *selected* photo.
5. **Background**: Choose your layout background (White/Blue/Green/Yellow) for the final sheet.
6. **Generate**: Click **Generate Sheet**. All enhancements and background removal are processed locally.
7. **Download**: Preview and download your A4 passport sheet!

---

## 🔒 Privacy & Performance

- **Privacy**: This application does not use any cloud-based image processing. All ML inference happens on your local machine.
- **Performance**: The first time you use it, `rembg` will download a small (~4MB) model file. Subsequent runs are near-instant.

---

## 📄 License
MIT License. Free to use, modify, and distribute.
