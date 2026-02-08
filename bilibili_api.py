"""
B站 API 模块
用于获取用户的稍后再看列表等信息
"""
import requests
import json


class BilibiliAPI:
    def __init__(self, sessdata=""):
        """
        初始化 B站 API 客户端
        :param sessdata: B站登录后的 SESSDATA Cookie（用于获取个人数据）
        """
        self.sessdata = sessdata
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.bilibili.com',
        }
        if sessdata:
            self.headers['Cookie'] = f'SESSDATA={sessdata}'
    
    def get_watchlater_list(self):
        """
        获取稍后再看列表
        :return: 视频列表 [{'bvid': 'BV1xx...', 'title': '视频标题', ...}, ...]
        """
        url = "https://api.bilibili.com/x/v2/history/toview"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') != 0:
                error_msg = data.get('message', '未知错误')
                if data.get('code') == -101:
                    raise ValueError("未登录或 SESSDATA 无效，请检查配置")
                raise ValueError(f"获取稍后再看列表失败: {error_msg}")
            
            # 提取视频列表
            videos = []
            video_list = data.get('data', {}).get('list', [])
            
            for item in video_list:
                video = {
                    'bvid': item.get('bvid', ''),
                    'title': item.get('title', ''),
                    'owner': item.get('owner', {}).get('name', ''),
                    'duration': item.get('duration', 0),
                    'pic': item.get('pic', ''),
                }
                videos.append(video)
            
            print(f"[API] 成功获取 {len(videos)} 个稍后再看视频")
            return videos
        
        except requests.exceptions.RequestException as e:
            print(f"[错误] 请求失败: {str(e)}")
            raise
    
    def get_video_info(self, bvid):
        """
        获取视频基本信息
        :param bvid: 视频BV号
        :return: 视频信息字典
        """
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') != 0:
                raise ValueError(f"获取视频信息失败: {data.get('message', '未知错误')}")
            
            video_data = data.get('data', {})
            return {
                'bvid': video_data.get('bvid', ''),
                'title': video_data.get('title', ''),
                'owner': video_data.get('owner', {}).get('name', ''),
                'duration': video_data.get('duration', 0),
                'desc': video_data.get('desc', ''),
            }
        
        except requests.exceptions.RequestException as e:
            print(f"[错误] 获取视频信息失败: {str(e)}")
            raise


def get_sessdata_guide():
    """
    打印获取 SESSDATA 的指南
    """
    guide = """
    ================================
    如何获取 B站 SESSDATA Cookie？
    ================================
    
    1. 打开浏览器，登录 B站 (https://www.bilibili.com)
    
    2. 按 F12 打开开发者工具
    
    3. 切换到 "应用程序/Application" 或 "存储/Storage" 标签页
    
    4. 左侧选择 "Cookie" -> "https://www.bilibili.com"
    
    5. 找到名称为 "SESSDATA" 的 Cookie，复制它的值
    
    6. 将复制的值粘贴到 .env 文件中：
       BILIBILI_SESSDATA=你的SESSDATA值
    
    注意：
    - SESSDATA 类似于你的登录凭证，请妥善保管
    - 如果退出登录，SESSDATA 会失效，需要重新获取
    - 不要分享你的 SESSDATA 给他人
    ================================
    """
    print(guide)


if __name__ == "__main__":
    # 测试代码
    print("B站 API 模块已就绪")
    print("\n如需获取稍后再看列表，请先配置 SESSDATA")
    get_sessdata_guide()
