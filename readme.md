# Kokoro TTS RunPod 服务使用文档

## 简介

Kokoro 是一款开源的轻量级 TTS（文本转语音）模型，拥有 8200 万参数。尽管架构轻量，但提供了与大型模型相当的质量，同时运行速度更快，成本更低。基于 Apache 许可的权重，Kokoro 可以部署在从生产环境到个人项目的任何地方。

本文档介绍如何通过 RunPod Serverless 平台使用 Kokoro TTS 服务。

## 特性

- **轻量级**：仅 82M 参数，比同类模型更高效
- **多语言支持**：支持英语、中文、日语、西班牙语等多种语言
- **多声音选择**：提供各种声音选项，适合不同场景
- **高质量输出**：生成自然流畅的语音
- **成本效益高**：运行快速，资源占用低
- **开源授权**：Apache 许可证，可用于商业项目

## 快速入门

### 发送请求

以下是使用 Python 向 Kokoro TTS RunPod 服务发送请求的基本示例：

```python
import requests
import json
import base64

# 替换为您的 RunPod 端点和 API 密钥
ENDPOINT_URL = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run"
API_KEY = "YOUR_API_KEY"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

payload = {
    "input": {
        "text": "欢迎使用 Kokoro 文本转语音服务。",
        "voice": "af_heart",
        "language": "zh",
        "speed": 1.0,
        "split_sentences": True
    }
}

response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
print(response.json())
```

### 参数说明

| 参数 | 类型 | 必填 | 描述 | 默认值 |
|------|------|------|------|--------|
| text | 字符串 | 是 | 要转换为语音的文本 | - |
| voice | 字符串 | 否 | 使用的声音 ID | "af_heart" |
| language | 字符串 | 否 | 语言代码 | "en-us" |
| speed | 浮点数 | 否 | 语速倍数 | 1.0 |
| split_sentences | 布尔值 | 否 | 是否按句分割 | true |

### 响应格式

成功响应示例：

```json
{
  "audio_base64": "BASE64_ENCODED_AUDIO_DATA",
  "message": "成功生成语音"
}
```

错误响应示例：

```json
{
  "error": "处理请求时出错: 无效的声音ID"
}
```
## 支持的语言

| 语言 | 代码 | 内部代码 | 备注 |
|------|------|----------|------|
| 美式英语 | en-us | a | 使用 misaki[en] |
| 英式英语 | en-gb | b | 使用 misaki[en] |
| 西班牙语 | es | e | - |
| 法语 | fr | f | - |
| 印地语 | hi | h | - |
| 意大利语 | it | i | - |
| 日语 | ja | j | 需要 misaki[ja] |
| 巴西葡萄牙语 | pt-br | p | - |
| 中文 | zh | z | 需要 misaki[zh] |

## v1.0可用声音
REPO_ID = 'hexgrad/Kokoro-82M' handler.py文件默认为hexgrad/Kokoro-82M-v1.1-zh

### 美式英语 (en-us, lang_code='a')

| 声音 ID | 特征 | 总体评级 | SHA256 |
|---------|------|----------|--------|
| af_heart | 🚺❤️ | A | 0ab5709b |
| af_bella | 🚺🔥 | A- | 8cb64e02 |
| af_nicole | 🚺🎧 | B- | c5561808 |
| af_alloy | 🚺 | C | 6d877149 |
| af_aoede | 🚺 | C+ | c03bd1a4 |
| af_kore | 🚺 | C+ | 8bfbc512 |
| af_sarah | 🚺 | C+ | 49bd364e |
| af_nova | 🚺 | C | e0233676 |
| af_sky | 🚺 | C- | c799548a |
| af_jessica | 🚺 | D | cdfdccb8 |
| af_river | 🚺 | D | e149459b |
| am_fenrir | 🚹 | C+ | 98e507ec |
| am_michael | 🚹 | C+ | 9a443b79 |
| am_puck | 🚹 | C+ | dd1d8973 |
| am_echo | 🚹 | D | 8bcfdc85 |
| am_eric | 🚹 | D | ada66f0e |
| am_liam | 🚹 | D | c8255075 |
| am_onyx | 🚹 | D | e8452be1 |
| am_santa | 🚹 | D- | 7f2f7582 |
| am_adam | 🚹 | F+ | ced7e284 |

### 英式英语 (en-gb, lang_code='b')

| 声音 ID | 特征 | 总体评级 | SHA256 |
|---------|------|----------|--------|
| bf_emma | 🚺 | B- | d0a423de |
| bf_isabella | 🚺 | C | cdd4c370 |
| bm_fable | 🚹 | C | d44935f3 |
| bm_george | 🚹 | C | f1bc8122 |
| bf_alice | 🚺 | D | d292651b |
| bf_lily | 🚺 | D | 6e09c2e4 |
| bm_daniel | 🚹 | D | fc3fce4e |
| bm_lewis | 🚹 | D+ | b5204750 |

### 中文 (zh, lang_code='z')

| 声音 ID | 特征 | 总体评级 | SHA256 |
|---------|------|----------|--------|
| zf_xiaobei | 🚺 | D | 9b76be63 |
| zf_xiaoni | 🚺 | D | 95b49f16 |
| zf_xiaoxiao | 🚺 | D | cfaf6f2d |
| zf_xiaoyi | 🚺 | D | b5235dba |
| zm_yunjian | 🚹 | D | 76cbf8ba |
| zm_yunxi | 🚹 | D | dbe6e1ce |
| zm_yunxia | 🚹 | D | bb2b03b0 |
| zm_yunyang | 🚹 | D | 5238ac22 |

## v1.1-zh 版本支持的语言
REPO_ID = 'hexgrad/Kokoro-82M-v1.1-zh' handler.py文件默认为hexgrad/Kokoro-82M-v1.1-zh

| 语言 | 代码 | 内部代码 | 备注 |
|------|------|----------|------|
| 美式英语 | en-us | a | 使用 misaki[en] |
| 英式英语 | en-gb | b | 使用 misaki[en] |
| 中文 | zh | z | 需要 misaki[zh] |

## v1.1-zh 版本支持的声音

### 英语声音 (v1.1-zh)

| 声音 ID | 特征 | 描述 |
|---------|------|------|
| af_maple | 🚺 | 美国女性，1小时训练数据 |
| af_sol | 🚺 | 美国女性，1小时训练数据 |
| bf_vale | 🚺 | 年长的英国女性，1小时训练数据 |

### 中文声音 (v1.1-zh)

v1.1-zh 版本支持 100 个中文声音，命名规则如下：

- **女性声音**：`zf_001` 到 `zf_050`
- **男性声音**：`zm_001` 到 `zm_050`

这些声音来自专业数据集，质量较高。

## 完整客户端示例

以下是一个完整的客户端示例，展示如何发送请求、接收响应并保存音频文件：

```python
import requests
import json
import base64
import os
import time

# RunPod 配置
RUNPOD_ENDPOINT = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run"
RUNPOD_API_KEY = "YOUR_API_KEY"

def text_to_speech(text, voice="af_heart", language="en-us", speed=1.0):
    """
    调用 RunPod Kokoro TTS 将文本转换为语音
    
    参数:
    - text: 要转换的文本
    - voice: 使用的声音 ID
    - language: 语言代码（en-us, en-gb, es, fr, hi, it, ja, pt-br, zh）
    - speed: 语速倍数
    
    返回:
    - audio_path: 保存的音频文件路径
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    payload = {
        "input": {
            "text": text,
            "voice": voice,
            "language": language,
            "speed": speed,
            "split_sentences": True
        }
    }
    
    response = requests.post(RUNPOD_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"错误: {response.status_code}")
        print(response.text)
        return None
    
    response_data = response.json()
    
    # 检查是否有错误
    if "error" in response_data:
        print(f"API 错误: {response_data['error']}")
        return None
    
    # 获取作业 ID 并等待结果
    job_id = response_data.get("id")
    status_url = f"https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/status/{job_id}"
    
    print(f"作业已提交，ID: {job_id}. 等待结果...")
    
    while True:
        status_response = requests.get(status_url, headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"})
        status_data = status_response.json()
        
        status = status_data.get("status")
        
        if status == "COMPLETED":
            output = status_data.get("output", {})
            
            if "error" in output:
                print(f"处理错误: {output['error']}")
                return None
                
            # 获取 base64 编码的音频数据
            audio_base64 = output.get("audio_base64")
            
            if not audio_base64:
                print("未找到音频数据")
                return None
            
            # 将 base64 解码为音频文件
            audio_data = base64.b64decode(audio_base64)
            
            # 保存音频文件
            output_path = f"{language}_{voice}_{int(time.time())}.wav"
            with open(output_path, "wb") as f:
                f.write(audio_data)
            
            print(f"音频已保存到 {output_path}")
            return output_path
            
        elif status == "FAILED":
            print(f"作业失败: {status_data.get('error', 'Unknown error')}")
            return None
            
        elif status in ["IN_QUEUE", "IN_PROGRESS"]:
            print(f"作业状态: {status}...")
            time.sleep(2)  # 等待 2 秒后重试
            
        else:
            print(f"未知状态: {status}")
            return None

# 使用示例
if __name__ == "__main__":
    text = "这是一个 Kokoro TTS 测试。它可以生成非常自然的语音。"
    output_path = text_to_speech(text, voice="zf_xiaoxiao", language="zh")
    
    if output_path:
        print(f"生成的音频文件: {output_path}")
```

## 高级用法

### 处理长文本

对于长文本，建议按段落或章节分批处理，以避免超过 RunPod 的执行时间限制：

```python
def process_long_text(text, max_length=1000, **kwargs):
    """处理长文本，按段落分批"""
    paragraphs = text.split('\n\n')
    results = []
    
    current_batch = ""
    for para in paragraphs:
        if len(current_batch) + len(para) > max_length:
            # 处理当前批次
            result = text_to_speech(current_batch, **kwargs)
            if result:
                results.append(result)
            current_batch = para
        else:
            if current_batch:
                current_batch += "\n\n"
            current_batch += para
    
    # 处理最后一个批次
    if current_batch:
        result = text_to_speech(current_batch, **kwargs)
        if result:
            results.append(result)
    
    return results
```

### 音频合并

处理多个音频片段后，您可能需要将它们合并为一个文件：

```python
def merge_audio_files(file_list, output_file):
    """合并多个 WAV 文件"""
    import wave
    import numpy as np
    
    data = []
    for file in file_list:
        w = wave.open(file, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()
    
    output = wave.open(output_file, 'wb')
    output.setparams(data[0][0])
    
    for i in range(len(data)):
        output.writeframes(data[i][1])
    
    output.close()
    
    return output_file
```

## 最佳实践

- **选择合适的声音**：根据表格中的评级选择质量更好的声音
- **考虑文本长度**：过长的文本可能需要分批处理
- **语言匹配**：确保所选声音与语言代码匹配
- **冷启动考量**：首次请求可能需要较长时间，后续请求会更快
- **错误处理**：始终包含适当的错误处理逻辑

## 故障排除

### 常见问题

1. **请求超时**
   - 可能原因：文本过长或服务器冷启动
   - 解决方案：分批处理文本，增加超时时间

2. **语音质量不佳**
   - 可能原因：选择了低评级的声音
   - 解决方案：尝试使用评级更高的声音（A 或 B 级）

3. **语言不匹配**
   - 可能原因：声音与语言代码不匹配
   - 解决方案：确保选择与语言匹配的声音

4. **服务不可用**
   - 可能原因：RunPod 端点未运行
   - 解决方案：检查 RunPod 控制台中的端点状态

## 技术细节

- 模型架构：基于 StyleTTS 2 和 ISTFTNet
- 模型大小：82M 参数
- 输出采样率：24000 Hz
- 输出格式：WAV

## 联系与支持

- Discord 服务器：https://discord.gg/QuGxSWBfQy
- GitHub 仓库：https://github.com/hexgrad/kokoro
- 演示：https://hf.co/spaces/hexgrad/Kokoro-TTS
