# Bilibili QuickView

B站视频快速预览工具 - 输入BV号，自动下载音频、转录文字、AI智能分析

## 功能特性

- 🎬 **自动下载**：输入BV号，自动提取B站视频音频
- 🎤 **语音识别**：使用硅基流动 SenseVoiceSmall（超快速、高准确率）
- 🤖 **AI分析**：DeepSeek 智能分析视频内容，识别信息密度和潜在风险
- 📊 **结构化输出**：生成易读的分析报告，包含核心要点和观看建议

## 快速开始

### 1. 环境要求

- Python 3.8+
- FFmpeg（用于音频处理）

### 2. 安装 FFmpeg

**Windows:**
```bash
# 使用 winget
winget install FFmpeg

# 或从官网下载：https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

### 3. 初始化项目

**Windows:**
```bash
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

### 4. 配置 API Key

编辑 `.env` 文件，填入你的 API Key：

```env
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

**获取 API Key：**
- 硅基流动：https://siliconflow.cn
- DeepSeek：https://platform.deepseek.com

### 5. 运行程序

**方式1：交互模式**
```bash
.venv\Scripts\activate  # Windows
# 或
source .venv/bin/activate  # Linux/macOS

python main.py
```

**方式2：命令行模式**
```bash
python main.py BV1xx411c7mD
```

## 使用示例

```bash
# 激活虚拟环境
.venv\Scripts\activate

# 运行程序
python main.py

# 输入BV号
BV号 > BV1xx411c7mD

# 等待处理...
# 完成后会生成分析报告并显示在控制台
```

## 项目结构

```
BilibiliQuickView/
├── main.py              # 主程序入口
├── downloader.py        # B站视频下载模块
├── asr.py              # 语音识别模块
├── summarizer.py       # AI分析模块
├── requirements.txt    # Python依赖
├── setup.bat           # Windows初始化脚本
├── setup.sh            # Linux/macOS初始化脚本
├── .env.example        # 配置模板
├── .gitignore          # Git忽略规则
├── downloads/          # 音频文件目录（自动生成）
└── output/             # 分析报告目录（自动生成）
```

## 技术栈

- **下载**：yt-dlp
- **ASR**：硅基流动 SenseVoiceSmall（免费，15倍速于Whisper）
- **LLM**：DeepSeek API
- **其他**：requests, python-dotenv, openai

## 注意事项

1. 首次运行需要下载 yt-dlp 的依赖
2. 音频文件会保存在 `downloads/` 目录
3. 分析报告会保存在 `output/` 目录
4. 确保网络畅通，能访问B站和API服务

## 常见问题

**Q: 下载失败怎么办？**
A: 检查网络连接，确认BV号正确，尝试更新 yt-dlp：`pip install -U yt-dlp`

**Q: ASR 识别失败？**
A: 检查 SILICONFLOW_API_KEY 是否正确，确认API余额充足

**Q: 没有安装 FFmpeg？**
A: 参考上方"安装 FFmpeg"章节

## 开源协议

MIT License
