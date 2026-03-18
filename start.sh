#!/bin/bash

echo "╔════════════════════════════════════════╗"
echo "║    道藏阅读平台 - 快速启动脚本        ║"
echo "╚════════════════════════════════════════╝"
echo ""

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未检测到Node.js，请先安装Node.js 18+"
    echo "   下载地址: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f 2 | cut -d'.' -f 1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js版本过低 (当前: $(node -v))"
    echo "   请升级到Node.js 18或更高版本"
    exit 1
fi

echo "✅ Node.js版本: $(node -v)"
echo ""

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ 未检测到npm"
    exit 1
fi

echo "✅ npm版本: $(npm -v)"
echo ""

# 安装依赖
echo "📦 安装依赖..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo ""
echo "✅ 依赖安装成功！"
echo ""

# 启动开发服务器
echo "🚀 启动开发服务器..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  本地地址: http://localhost:5173"
echo "  按 Ctrl+C 停止服务器"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

npm run docs:dev
