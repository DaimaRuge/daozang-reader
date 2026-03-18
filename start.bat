@echo off
chcp 65001 >nul
title 道藏阅读平台

echo ╔════════════════════════════════════════╗
echo ║    道藏阅读平台 - 快速启动脚本        ║
echo ╚════════════════════════════════════════╝
echo.

REM 检查Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 未检测到Node.js，请先安装Node.js 18+
    echo    下载地址: https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
echo ✅ Node.js版本: %NODE_VERSION%
echo.

REM 检查npm
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 未检测到npm
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm -v') do set NPM_VERSION=%%i
echo ✅ npm版本: %NPM_VERSION%
echo.

REM 检查是否已安装依赖
if not exist "node_modules" (
    echo 📦 首次运行，正在安装依赖...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo.
    echo ✅ 依赖安装成功！
    echo.
)

REM 启动开发服务器
echo 🚀 启动开发服务器...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   本地地址: http://localhost:5173
echo   按 Ctrl+C 停止服务器
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

call npm run docs:dev
