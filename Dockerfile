FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    espeak-ng \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 复制应用代码
COPY handler.py .
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 预下载和预缓存模型
RUN python -c "from kokoro import KModel; \
    model = KModel(repo_id='hexgrad/Kokoro-82M-v1.1-zh'); \
    print('模型已成功预加载')"

# 预加载所有支持的语言管道
RUN python -c "from kokoro import KPipeline; \
    en_pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M-v1.1-zh'); \
    print('英语管道已加载'); \
    zh_pipeline = KPipeline(lang_code='z', repo_id='hexgrad/Kokoro-82M-v1.1-zh'); \
    print('中文管道已加载')"

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV RUNPOD_DEBUG_MODE=1

# 设置入口点
CMD ["python", "-u", "handler.py"]