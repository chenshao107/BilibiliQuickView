"""
语音转文字模块
调用硅基流动的 SenseVoiceSmall API 进行音频识别
"""
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class SenseVoiceASR:
    def __init__(self):
        """
        初始化 ASR 客户端
        """
        self.api_key = os.getenv("SILICONFLOW_API_KEY")
        if not self.api_key:
            raise ValueError("未找到 SILICONFLOW_API_KEY，请在 .env 文件中配置")
        
        self.api_url = "https://api.siliconflow.cn/v1/audio/transcriptions"
        self.model = "FunAudioLLM/SenseVoiceSmall"
    
    def transcribe(self, audio_path):
        """
        将音频文件转换为文字
        :param audio_path: 音频文件路径
        :return: 识别出的文本内容
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        print(f"[ASR] 正在识别音频: {audio_path}")
        
        # 准备请求
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        files = {
            "file": open(audio_path, "rb"),
            "model": (None, self.model)
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                files=files,
                timeout=300  # 5分钟超时
            )
            
            response.raise_for_status()
            result = response.json()
            
            # 提取转录文本
            text = result.get("text", "")
            
            print(f"[ASR] 识别完成，文本长度: {len(text)} 字符")
            return text
        
        except requests.exceptions.RequestException as e:
            print(f"[错误] ASR 请求失败: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[错误详情] {e.response.text}")
            raise
        
        finally:
            # 关闭文件
            if 'files' in locals():
                files['file'][1].close() if isinstance(files['file'], tuple) else files['file'].close()


if __name__ == "__main__":
    # 测试代码
    asr = SenseVoiceASR()
    print("ASR 模块已就绪，请在主程序中调用。")
