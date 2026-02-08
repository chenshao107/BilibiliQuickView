"""
语音转文字模块
调用硅基流动的 SenseVoiceSmall API 进行音频识别
"""
import os
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class SenseVoiceASR:
    def __init__(self, cache_dir="cache"):
        """
        初始化 ASR 客户端
        :param cache_dir: 缓存目录，用于存储转录文本
        """
        self.api_key = os.getenv("SILICONFLOW_API_KEY")
        if not self.api_key:
            raise ValueError("未找到 SILICONFLOW_API_KEY，请在 .env 文件中配置")
        
        self.api_url = "https://api.siliconflow.cn/v1/audio/transcriptions"
        self.model = "FunAudioLLM/SenseVoiceSmall"
        
        # 创建缓存目录
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, audio_path):
        """
        获取音频文件对应的缓存文件路径
        :param audio_path: 音频文件路径
        :return: 缓存文件路径
        """
        # 使用音频文件名作为缓存文件名
        audio_filename = os.path.basename(audio_path)
        cache_filename = os.path.splitext(audio_filename)[0] + "_transcript.json"
        return os.path.join(self.cache_dir, cache_filename)
    
    def _load_from_cache(self, audio_path):
        """
        从缓存加载转录文本
        :param audio_path: 音频文件路径
        :return: 转录文本，如果缓存不存在返回 None
        """
        cache_path = self._get_cache_path(audio_path)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # 验证缓存数据
            if 'text' in cache_data and cache_data['text']:
                print(f"[缓存] 发现转录文本缓存: {cache_path}")
                print(f"[缓存] 文本长度: {len(cache_data['text'])} 字符")
                return cache_data['text']
            else:
                print(f"[警告] 缓存数据无效，将重新转录")
                return None
        
        except Exception as e:
            print(f"[警告] 读取缓存失败: {str(e)}，将重新转录")
            return None
    
    def _save_to_cache(self, audio_path, text):
        """
        保存转录文本到缓存
        :param audio_path: 音频文件路径
        :param text: 转录文本
        """
        cache_path = self._get_cache_path(audio_path)
        
        try:
            cache_data = {
                'audio_path': audio_path,
                'text': text,
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'model': self.model
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print(f"[缓存] 转录文本已保存: {cache_path}")
        
        except Exception as e:
            print(f"[警告] 保存缓存失败: {str(e)}")
    
    def transcribe(self, audio_path, use_cache=True):
        """
        将音频文件转换为文字（带缓存机制）
        :param audio_path: 音频文件路径
        :param use_cache: 是否使用缓存
        :return: 识别出的文本内容
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        # 尝试从缓存加载
        if use_cache:
            cached_text = self._load_from_cache(audio_path)
            if cached_text:
                print(f"[缓存] 使用缓存的转录文本")
                return cached_text
        
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
            
            # 保存到缓存
            if text:
                self._save_to_cache(audio_path, text)
            
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
