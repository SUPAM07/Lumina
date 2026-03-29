# Use Python 3.11-slim for a smaller footprint
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV U2NET_HOME=/root/.u2net

# Install system dependencies (build-essential for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the u2netp (lightweight) model so the first request doesn't lag
# We do this during build to bake the weight into the image.
RUN python -c "from rembg import new_session; new_session('u2netp')"

# Copy the application code
COPY . .

# Expose the port (matches waitress setup)
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
