"""
AI 文本加工模块
调用 DeepSeek API 对转录文本进行摘要和分析
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class DeepSeekSummarizer:
    def __init__(self):
        """
        初始化 DeepSeek 客户端
        """
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("未找到 DEEPSEEK_API_KEY，请在 .env 文件中配置")
        
        # DeepSeek 使用 OpenAI SDK
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        self.model = "deepseek-chat"
    
    def analyze(self, transcript_text, bv_id=""):
        """
        对视频转录文本进行智能分析和摘要
        :param transcript_text: 视频转录文本
        :param bv_id: 视频BV号（可选）
        :return: AI 分析结果
        """
        print(f"[AI] 正在分析文本内容...")
        
        # 构建 Prompt
        system_prompt = """你是一位专业的视频内容分析师。你的任务是帮助用户快速了解一个 B 站视频的价值，避免浪费时间。

请根据用户提供的视频转录文本，提供以下内容：

1. **视频概要**（1-2 句话）：用简洁的语言总结视频主题。
2. **核心要点**（3-5 个要点）：提取视频中最重要的信息点。
3. **信息密度评估**（高/中/低）：评价该视频的信息量和价值。
4. **观看建议**：
   - 值得看：如果视频内容实用、信息量大、无明显营销。
   - 选择性观看：如果有部分有价值的内容，但存在冗余或营销。
   - 不建议看：如果视频是明显的标题党、废话太多或纯营销内容。
5. **潜在风险提示**（如有）：识别视频中是否存在误导信息、过度营销、情绪煽动等问题。

请以结构化、易读的格式输出你的分析结果。"""

        user_prompt = f"""以下是一个 B 站视频的转录文本：

{transcript_text}

请对这个视频进行深入分析。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis = response.choices[0].message.content
            print(f"[AI] 分析完成！")
            
            return analysis
        
        except Exception as e:
            print(f"[错误] DeepSeek API 调用失败: {str(e)}")
            raise


if __name__ == "__main__":
    # 测试代码
    summarizer = DeepSeekSummarizer()
    print("AI 摘要模块已就绪，请在主程序中调用。")
