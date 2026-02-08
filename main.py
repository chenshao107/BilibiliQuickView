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
    output_file = os.path.join(output_dir, f"{bv_id}_{timestamp}.txt")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"B站视频快速分析报告\n")
        f.write(f"视频BV号: {bv_id}\n")
        f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("【AI 智能分析】\n")
        f.write("-" * 60 + "\n")
        f.write(analysis)
        f.write("\n\n")
        
        f.write("【完整转录文本】\n")
        f.write("-" * 60 + "\n")
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
        # 步骤1: 下载音频
        print("📥 [1/3] 下载视频音频...")
        downloader = BilibiliDownloader()
        audio_path = downloader.download_audio(bv_id)
        
        # 步骤2: 音频转文字
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
        
        # 在控制台显示分析结果
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


def main():
    """
    主程序入口
    """
    print("\n" + "🎯" * 30)
    print("  Bilibili QuickView - B站视频快速预览工具")
    print("🎯" * 30 + "\n")
    
    if len(sys.argv) > 1:
        # 命令行参数模式
        bv_id = sys.argv[1]
        process_video(bv_id)
    else:
        # 交互模式
        print("请输入B站视频的BV号（输入 'q' 退出）：")
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


if __name__ == "__main__":
    main()
