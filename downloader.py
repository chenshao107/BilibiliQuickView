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
    
    def download_audio(self, bv_id):
        """
        下载B站视频的音频
        :param bv_id: B站视频的BV号（如 BV1xx411c7mD）
        :return: 下载的音频文件路径
        """
        # 构造B站视频URL
        if not bv_id.startswith("BV"):
            bv_id = f"BV{bv_id}"
        
        url = f"https://www.bilibili.com/video/{bv_id}"
        
        # 输出文件路径
        output_path = os.path.join(self.download_dir, f"{bv_id}.mp3")
        
        # yt-dlp 配置
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.download_dir, f"{bv_id}.%(ext)s"),
            'quiet': False,
            'no_warnings': False,
        }
        
        try:
            print(f"[下载] 开始下载 {bv_id} 的音频...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"[下载] 完成！音频保存至: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"[错误] 下载失败: {str(e)}")
            raise


if __name__ == "__main__":
    # 测试代码
    downloader = BilibiliDownloader()
    # 示例: downloader.download_audio("BV1xx411c7mD")
    print("下载模块已就绪，请在主程序中调用。")
