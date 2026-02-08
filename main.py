"""
Bilibili QuickView - B站视频快速预览工具
输入BV号，自动下载音频 -> 转录 -> AI分析
"""
import os
import sys
from datetime import datetime
from downloader import BilibiliDownloader
from asr import SenseVoiceASR
from summarizer import DeepSeekSummarizer
from bilibili_api import BilibiliAPI, get_sessdata_guide
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def save_result(bv_id, transcript, analysis):
    """
    保存分析结果到文件
    :param bv_id: 视频BV号
    :param transcript: 转录文本
    :param analysis: AI分析结果
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{bv_id}_{timestamp}.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# B站视频快速分析报告\n\n")
        f.write(f"**视频BV号**: {bv_id}\n\n")
        f.write(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## AI 智能分析\n\n")
        f.write(analysis)
        f.write("\n\n")
        
        f.write("---\n\n")
        f.write("## 完整转录文本\n\n")
        f.write(transcript)
        f.write("\n")
    
    print(f"\n✅ 分析报告已保存至: {output_file}")
    return output_file


def process_video(bv_id):
    """
    处理单个B站视频
    :param bv_id: 视频BV号
    """
    print("\n" + "=" * 60)
    print(f"🎬 开始处理视频: {bv_id}")
    print("=" * 60 + "\n")
    
    try:
        # 步骤1: 下载音频（带缓存）
        print("📥 [1/3] 下载视频音频...")
        downloader = BilibiliDownloader()
        audio_path = downloader.download_audio(bv_id)
        
        # 步骤2: 音频转文字（带缓存）
        print("\n🎤 [2/3] 语音识别转录...")
        asr = SenseVoiceASR()
        transcript = asr.transcribe(audio_path)
        
        if not transcript or len(transcript.strip()) == 0:
            print("⚠️ 警告: 转录文本为空，可能是音频无内容或识别失败")
            return
        
        # 步骤3: AI 分析
        print("\n🤖 [3/3] AI 智能分析...")
        summarizer = DeepSeekSummarizer()
        analysis = summarizer.analyze(transcript, bv_id)
        
        # 保存结果
        output_file = save_result(bv_id, transcript, analysis)
        
        # 在控制台显示AI分析结果
        print("\n" + "=" * 60)
        print("📊 AI 分析结果")
        print("=" * 60)
        print(analysis)
        print("=" * 60 + "\n")
        
        print(f"✨ 处理完成！可以查看完整报告: {output_file}")
        
    except Exception as e:
        print(f"\n❌ 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()


def process_watchlater_batch():
    """
    批量处理稍后再看列表
    """
    print("\n" + "=" * 60)
    print("📋 批量处理稍后再看")
    print("=" * 60 + "\n")
    
    # 获取 SESSDATA
    sessdata = os.getenv("BILIBILI_SESSDATA")
    if not sessdata:
        print("❌ 错误：未配置 BILIBILI_SESSDATA")
        print("\n请先在 .env 文件中配置你的 B站 SESSDATA：")
        get_sessdata_guide()
        return
    
    try:
        # 获取稍后再看列表
        print("📥 正在获取稍后再看列表...")
        api = BilibiliAPI(sessdata)
        videos = api.get_watchlater_list()
        
        if not videos:
            print("\n✅ 稍后再看列表为空，无需处理")
            return
        
        # 显示视频列表
        print("\n" + "=" * 60)
        print(f"发现 {len(videos)} 个视频：")
        print("=" * 60)
        for i, video in enumerate(videos, 1):
            duration_min = video['duration'] // 60
            print(f"{i}. [{video['bvid']}] {video['title']}")
            print(f"   UP主: {video['owner']} | 时长: {duration_min}分钟")
        print("=" * 60 + "\n")
        
        # 询问是否批量处理
        choice = input("是否批量处理这些视频？(y/n，或输入序号范围如 1-5): ").strip().lower()
        
        if choice == 'n':
            print("👋 已取消")
            return
        
        # 确定要处理的视频
        to_process = []
        if choice == 'y':
            to_process = videos
        elif '-' in choice:
            # 处理范围输入（如 1-5）
            try:
                start, end = map(int, choice.split('-'))
                to_process = videos[start-1:end]
            except:
                print("❌ 无效的范围格式")
                return
        elif choice.isdigit():
            # 单个序号
            idx = int(choice) - 1
            if 0 <= idx < len(videos):
                to_process = [videos[idx]]
        else:
            print("❌ 无效的输入")
            return
        
        # 批量处理
        print(f"\n🚀 开始批量处理 {len(to_process)} 个视频...\n")
        success_count = 0
        fail_count = 0
        
        for i, video in enumerate(to_process, 1):
            print(f"\n{'='*60}")
            print(f"处理进度: {i}/{len(to_process)}")
            print(f"{'='*60}")
            
            try:
                process_video(video['bvid'])
                success_count += 1
            except Exception as e:
                print(f"❌ 处理失败: {str(e)}")
                fail_count += 1
            
            # 避免请求过快
            if i < len(to_process):
                print("\n⏳ 等待 3 秒后继续...")
                import time
                time.sleep(3)
        
        # 总结
        print("\n" + "=" * 60)
        print("📊 批量处理完成！")
        print("=" * 60)
        print(f"✅ 成功: {success_count} 个")
        print(f"❌ 失败: {fail_count} 个")
        print("=" * 60 + "\n")
    
    except Exception as e:
        print(f"\n❌ 批量处理失败: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """
    主程序入口
    """
    print("\n" + "🎯" * 30)
    print("  Bilibili QuickView - B站视频快速预览工具")
    print("🎯" * 30 + "\n")
    
    if len(sys.argv) > 1:
        # 命令行参数模式
        if sys.argv[1] == "--watchlater" or sys.argv[1] == "-w":
            # 批量处理稍后再看
            process_watchlater_batch()
        else:
            # 处理单个BV号
            bv_id = sys.argv[1]
            process_video(bv_id)
    else:
        # 交互模式
        print("选择模式：")
        print("  1. 输入单个BV号")
        print("  2. 批量处理稍后再看")
        print("  q. 退出\n")
        
        mode = input("请选择 (1/2/q): ").strip()
        
        if mode == '1':
            # 单个BV号模式
            print("\n请输入B站视频的BV号（输入 'q' 返回）：")
            while True:
                bv_id = input("\nBV号 > ").strip()
                
                if bv_id.lower() == 'q':
                    print("👋 再见！")
                    break
                
                if not bv_id:
                    print("⚠️ 请输入有效的BV号")
                    continue
                
                process_video(bv_id)
                print("\n" + "-" * 60)
                print("继续输入BV号，或输入 'q' 退出")
        
        elif mode == '2':
            # 批量处理模式
            process_watchlater_batch()
        
        elif mode.lower() == 'q':
            print("👋 再见！")
        
        else:
            print("❌ 无效的选择")


if __name__ == "__main__":
    main()
