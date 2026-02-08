"""
B站视频音频下载模块
使用 yt-dlp 下载指定 BV 号的视频音频
"""
import os
import yt_dlp


class BilibiliDownloader:
    def __init__(self, download_dir="downloads"):
        """
        初始化下载器
        :param download_dir: 音频文件下载目录
        """
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
    
    def download_audio(self, bv_id, force_download=False):
        """
        下载B站视频的音频（带缓存机制）
        :param bv_id: B站视频的BV号（如 BV1xx411c7mD）
        :param force_download: 是否强制重新下载（忽略缓存）
        :return: 下载的音频文件路径
        """
        # 构造B站视频URL
        if not bv_id.startswith("BV"):
            bv_id = f"BV{bv_id}"
        
        url = f"https://www.bilibili.com/video/{bv_id}"
        
        # 输出文件路径
        output_path = os.path.join(self.download_dir, f"{bv_id}.mp3")
        
        # 检查缓存
        if not force_download and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 0:
                print(f"[缓存] 发现已下载的音频文件: {output_path}")
                print(f"[缓存] 文件大小: {file_size / 1024 / 1024:.2f} MB")
                print(f"[缓存] 跳过下载，直接使用缓存")
                return output_path
            else:
                print(f"[警告] 发现空文件，将重新下载")
                os.remove(output_path)
        
        # yt-dlp 配置
        ydl_opts = {
            'format': 'worstaudio/worst',  # 使用最低音质，节省带宽和时间
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '64',  # 64kbps 低音质，足够语音识别使用
            }],
            'outtmpl': os.path.join(self.download_dir, f"{bv_id}.%(ext)s"),
            'quiet': False,
            'no_warnings': False,
        }
        
        try:
            print(f"[下载] 开始下载 {bv_id} 的音频...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 验证下载完成
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"[下载] 完成！音频保存至: {output_path}")
                print(f"[下载] 文件大小: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
                return output_path
            else:
                raise Exception("下载完成但文件不存在或为空")
        
        except Exception as e:
            print(f"[错误] 下载失败: {str(e)}")
            # 清理可能的损坏文件
            if os.path.exists(output_path):
                os.remove(output_path)
            raise


if __name__ == "__main__":
    # 测试代码
    downloader = BilibiliDownloader()
    # 示例: downloader.download_audio("BV1xx411c7mD")
    print("下载模块已就绪，请在主程序中调用。")
