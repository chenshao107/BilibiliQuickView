@echo off
REM Bilibili QuickView - 环境初始化脚本 (Windows)
REM 自动创建虚拟环境并安装依赖

echo ========================================
echo Bilibili QuickView - 环境初始化
echo ========================================
echo.

REM 检查 Python 是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] 检测到 Python 版本:
python --version
echo.

REM 创建虚拟环境
echo [2/4] 创建虚拟环境 (.venv)...
if exist .venv (
    echo 虚拟环境已存在，跳过创建
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功！
)
echo.

REM 激活虚拟环境并安装依赖
echo [3/4] 激活虚拟环境并安装依赖...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo 依赖安装成功！
echo.

REM 检查配置文件
echo [4/4] 检查配置文件...
if not exist .env (
    echo [警告] 未找到 .env 文件，正在从模板创建...
    copy .env.example .env
    echo.
    echo ========================================
    echo 重要：请编辑 .env 文件，填入你的 API Key
    echo ========================================
    echo 1. 硅基流动 API Key: https://siliconflow.cn
    echo 2. DeepSeek API Key: https://platform.deepseek.com
    echo.
    echo 编辑完成后，运行以下命令启动程序：
    echo   .venv\Scripts\activate
    echo   python main.py
    echo ========================================
) else (
    echo .env 文件已存在
    echo.
    echo ========================================
    echo 环境初始化完成！
    echo ========================================
    echo.
    echo 使用方法：
    echo   1. 激活虚拟环境: .venv\Scripts\activate
    echo   2. 运行程序: python main.py
    echo   3. 或直接运行: python main.py BV1xx411c7mD
    echo ========================================
)
echo.

pause
