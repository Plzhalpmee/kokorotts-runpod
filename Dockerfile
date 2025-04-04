FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    espeak-ng \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download and pre-cache model
RUN python -c "from kokoro import KModel; \
    model = KModel(repo_id='hexgrad/Kokoro-82M-v1.1-zh'); \
    print('Model preloaded successfully')"

# Preload all supported language pipelines
RUN python -c "from kokoro import KPipeline; \
    en_pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M-v1.1-zh'); \
    print('English pipeline loaded'); \
    zh_pipeline = KPipeline(lang_code='z', repo_id='hexgrad/Kokoro-82M-v1.1-zh'); \
    print('Chinese pipeline loaded')"

# Set environment variables
ENV PYTHONUNBUFFERED=1

COPY . .
# Set entry point
CMD ["python", "-u", "handler.py"]
