#!/bin/bash
# Bilibili QuickView - 环境初始化脚本 (Linux/macOS)
# 自动创建虚拟环境并安装依赖

echo "========================================"
echo "Bilibili QuickView - 环境初始化"
echo "========================================"
echo ""

# 检查 Python 是否已安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.8+"
    exit 1
fi

echo "[1/4] 检测到 Python 版本:"
python3 --version
echo ""

# 创建虚拟环境
echo "[2/4] 创建虚拟环境 (.venv)..."
if [ -d ".venv" ]; then
    echo "虚拟环境已存在，跳过创建"
else
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[错误] 虚拟环境创建失败"
        exit 1
    fi
    echo "虚拟环境创建成功！"
fi
echo ""

# 激活虚拟环境并安装依赖
echo "[3/4] 激活虚拟环境并安装依赖..."
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[错误] 依赖安装失败"
    exit 1
fi
echo "依赖安装成功！"
echo ""

# 检查配置文件
echo "[4/4] 检查配置文件..."
if [ ! -f ".env" ]; then
    echo "[警告] 未找到 .env 文件，正在从模板创建..."
    cp .env.example .env
    echo ""
    echo "========================================"
    echo "重要：请编辑 .env 文件，填入你的 API Key"
    echo "========================================"
    echo "1. 硅基流动 API Key: https://siliconflow.cn"
    echo "2. DeepSeek API Key: https://platform.deepseek.com"
    echo ""
    echo "编辑完成后，运行以下命令启动程序："
    echo "  source .venv/bin/activate"
    echo "  python main.py"
    echo "========================================"
else
    echo ".env 文件已存在"
    echo ""
    echo "========================================"
    echo "环境初始化完成！"
    echo "========================================"
    echo ""
    echo "使用方法："
    echo "  1. 激活虚拟环境: source .venv/bin/activate"
    echo "  2. 运行程序: python main.py"
    echo "  3. 或直接运行: python main.py BV1xx411c7mD"
    echo "========================================"
fi
echo ""
