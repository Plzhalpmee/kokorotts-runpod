import runpod
import os
import base64
import numpy as np
import soundfile as sf
from kokoro import KModel,KPipeline
import tempfile
import uuid
import tempfile
from pydub import AudioSegment
import io
import torch

# 支持的语言代码映射
LANGUAGE_MAP = {
    "en-us": "a",  # 美式英语
    "en-gb": "b",  # 英式英语
    "es": "e",     # 西班牙语
    "fr": "f",     # 法语
    "hi": "h",     # 印地语
    "it": "i",     # 意大利语
    "ja": "j",     # 日语
    "pt-br": "p",  # 巴西葡萄牙语
    "zh": "z"      # 中文
}

# 存储不同语言的管道
pipelines = {}
REPO_ID = 'hexgrad/Kokoro-82M-v1.1-zh'
# 获取或创建语言管道
def get_pipeline(lang_code):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = KModel(repo_id=REPO_ID).to(device).eval()
    code = LANGUAGE_MAP.get(lang_code, "z")  # 默认回退到中文
    pipelines[lang_code] = KPipeline(lang_code=code,repo_id="hexgrad/Kokoro-82M-v1.1-zh",model=model,device=device)
    return pipelines[lang_code]

def handler(job):
    """
    RunPod 处理函数
    
    输入参数:
    - text: 要转换的文本 (必填)
    - voice: 使用的声音 ID (默认: zf_xiaobei)
    - language: 语言代码 (默认: zh)
    - speed: 语速 (默认: 1.0)
    - split_sentences: 是否按句分割 (默认: true)
    
    返回:
    - audio_base64: Base64编码的音频数据
    - message: 处理状态消息
    """
    job_input = job["input"]
    
    # 获取输入参数
    text = job_input.get("text")
    if not text:
        return {"error": "必须提供 'text' 参数"}
    
    voice = job_input.get("voice", "zf_xiaobei")
    language = job_input.get("language", "zh")
    speed = float(job_input.get("speed", 1.0))
    split_sentences = bool(job_input.get("split_sentences", True))
    
    try:
        # 检查语言支持
        if language not in LANGUAGE_MAP:
            return {"error": f"不支持的语言: {language}"}
        
        # 获取语言管道
        pipeline = get_pipeline(language)
        
        # 设置分割模式
        split_pattern = r'\n+' if split_sentences else None
        
        # 生成音频
        all_audio = []
        generator = pipeline(
            text, 
            voice=voice, 
            speed=speed,
            split_pattern=split_pattern
        )
        
        for i, (gs, ps, audio) in enumerate(generator):
            all_audio.append(audio)
        
        # 如果有多个片段，合并它们
        if len(all_audio) > 1:
            combined_audio = np.concatenate(all_audio)
        else:
            combined_audio = all_audio[0] if all_audio else None
        
        if combined_audio is None:
            return {"error": "生成音频失败"}
        
        # 创建临时文件来保存音频
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
            sf.write(temp_path, combined_audio, 24000)

        
         # 将 WAV 转换为 MP3
        wav_audio = AudioSegment.from_wav(temp_path)
        mp3_io = io.BytesIO()
        wav_audio.export(mp3_io, format="mp3", bitrate="192k")
        mp3_data = mp3_io.getvalue()
        
        # 将 MP3 数据转换为 base64
        audio_base64 = base64.b64encode(mp3_data).decode("utf-8")
        
        # 删除临时文件
        os.unlink(temp_path)
        
        # 返回结果
        return {
            "audio_base64": audio_base64,
            "message": "成功生成语音"
        }
    
    except Exception as e:
        return {"error": f"处理请求时出错: {str(e)}"}
def adjust_concurrency(current_concurrency):
    return 20
    
# 启动 RunPod Serverless
if __name__=="__main__":
    runpod.serverless.start({"handler": handler,"concurrency_modifier": adjust_concurrency})