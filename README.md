# Bilibili QuickView

B站视频快速预览工具 - 输入BV号，自动下载音频、转录文字、AI智能分析

## 功能特性

- 🎬 **自动下载**：输入BV号，自动提取B站视频音频
- 📋 **批量处理**：读取B站账号的稍后再看列表，批量分析视频
- 💾 **智能缓存**：音频和转录文本自动缓存，避免重复下载和 API 调用
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

### 4. 配置 API Key 和 SESSDATA（可选）

编辑 `.env` 文件，填入你的 API Key：

```env
# 必需：API Keys
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 可选：B站 SESSDATA（用于批量处理稍后再看）
BILIBILI_SESSDATA=your_bilibili_sessdata_here
```

**获取 API Key：**
- 硅基流动：https://siliconflow.cn
- DeepSeek：https://platform.deepseek.com

**获取 B站 SESSDATA（可选，用于批量处理稍后再看）：**
1. 登录 B站 (https://www.bilibili.com)
2. 按 F12 打开开发者工具
3. 切换到 "应用程序/Application" 标签
4. 左侧选择 Cookie → https://www.bilibili.com
5. 找到名为 "SESSDATA" 的 Cookie，复制其值
6. 粘贴到 `.env` 文件中

### 5. 运行程序

**方式1：交互模式**
```bash
.venv\Scripts\activate  # Windows
# 或
source .venv/bin/activate  # Linux/macOS

python main.py

# 选择模式：
# 1. 输入单个BV号
# 2. 批量处理稍后再看
```

**方式2：处理单个视频（命令行）**
```bash
python main.py BV1xx411c7mD
```

**方式3：批量处理稍后再看（命令行）**
```bash
python main.py --watchlater
# 或
python main.py -w
```

## 使用示例

### 示例1：处理单个视频
```bash
# 激活虚拟环境
.venv\Scripts\activate

# 运行程序
python main.py

# 选择模式 1
请选择 (1/2/q): 1

# 输入BV号
BV号 > BV1xx411c7mD

# 等待处理...
# 完成后会生成分析报告并显示在控制台
```

### 示例2：批量处理稍后再看
```bash
# 方式1：交互模式
python main.py
请选择 (1/2/q): 2

# 方式2：命令行模式
python main.py --watchlater

# 输出示例：
📋 批量处理稍后再看
============================================================

📥 正在获取稍后再看列表...
[API] 成功获取 10 个视频

============================================================
发现 10 个视频：
============================================================
1. [BV1xx411c7mD] Python教程第一课
   UP主: 某某老师 | 时长: 15分钟
2. [BV1yy411c8mE] AI入门指南
   UP主: AI爱好者 | 时长: 20分钟
...
============================================================

是否批量处理这些视频？(y/n，或输入序号范围如 1-5): y
# 或输入 1-5 只处理前5个
# 或输入 3 只处理第3个
```

## 项目结构

```
BilibiliQuickView/
├── main.py              # 主程序入口
├── downloader.py        # B站视频下载模块（带缓存）
├── asr.py              # 语音识别模块（带缓存）
├── summarizer.py       # AI分析模块
├── bilibili_api.py     # B站 API 模块（稍后再看）
├── requirements.txt    # Python依赖
├── setup.bat           # Windows初始化脚本
├── setup.sh            # Linux/macOS初始化脚本
├── .env.example        # 配置模板
├── .gitignore          # Git忽略规则
├── downloads/          # 音频文件缓存目录（自动生成）
├── cache/              # 转录文本缓存目录（自动生成）
└── output/             # 分析报告目录（自动生成）
```

## 技术栈

- **下载**：yt-dlp（支持B站视频音频提取）
- **B站 API**：稍后再看列表获取
- **ASR**：硅基流动 SenseVoiceSmall（免费，15倍速于Whisper）
- **LLM**：DeepSeek API（智能分析和摘要）
- **缓存**：本地文件缓存（音频 + 转录文本）
- **其他**：requests, python-dotenv, openai

## 注意事项

1. 首次运行需要下载 yt-dlp 的依赖
2. **缓存机制**：音频文件和转录文本会自动缓存，避免重复处理
   - 音频缓存：`downloads/` 目录
   - 转录缓存：`cache/` 目录
   - 分析报告：`output/` 目录
3. **批量处理**：需要配置 `BILIBILI_SESSDATA` 才能使用稍后再看功能
4. 确保网络畅通，能访问B站和API服务
5. **程序崩溃恢复**：如果处理中断，重新运行会自动使用已有缓存

## 常见问题

**Q: 下载失败怎么办？**
A: 检查网络连接，确认BV号正确，尝试更新 yt-dlp：`pip install -U yt-dlp`

**Q: ASR 识别失败？**
A: 检查 SILICONFLOW_API_KEY 是否正确，确认API余额充足

**Q: 没有安装 FFmpeg？**
A: 参考上方"安装 FFmpeg"章节

**Q: 如何使用批量处理稍后再看？**
A: 需要在 `.env` 中配置 `BILIBILI_SESSDATA`，然后运行 `python main.py -w`

**Q: 稍后再看列表获取失败？**
A: 检查 SESSDATA 是否正确或已过期，重新登录B站后获取新的 SESSDATA

**Q: 如何清除缓存重新处理？**
A: 删除 `downloads/` 或 `cache/` 目录下对应的文件，或使用 `force_download=True` 参数

## 开源协议

MIT License
