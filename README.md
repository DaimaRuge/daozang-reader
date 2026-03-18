# 道藏阅读平台 (Daozang Reader)

> 《正统道藏》在线阅读平台 - 1504部道教经典文献

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![VitePress](https://img.shields.io/badge/VitePress-1.0+-green.svg)](https://vitepress.dev)

## 📖 项目简介

本项目是一个基于 [VitePress](https://vitepress.dev/) 构建的道教经典在线阅读平台，收录《正统道藏》及《续道藏》共1504部经典文献。

### 特色

- 🎨 **古典风格** - 水墨配色，思源宋体，营造沉浸式阅读体验
- 🔍 **全文检索** - 内置搜索功能，快速定位经文
- 📱 **多端适配** - 响应式设计，支持PC、平板、手机
- 🤖 **AI友好** - 提供结构化JSON API，便于程序调用
- ⚡ **极速加载** - 静态网站，CDN加速，毫秒级响应
- 🌐 **SEO优化** - 完善的元信息，便于搜索引擎收录

## 🚀 快速开始

### 前置要求

- Node.js 18+
- npm 或 pnpm

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/DaimaRuge/daozang-reader.git
cd daozang-reader

# 安装依赖
npm install
```

### 开发模式

```bash
npm run docs:dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
npm run docs:build
```

构建产物在 `docs/.vitepress/dist` 目录

### 预览生产版本

```bash
npm run docs:preview
```

## 📂 项目结构

```
daozang-reader/
├── docs/                    # VitePress文档目录
│   ├── .vitepress/         # VitePress配置
│   │   ├── config.mts      # 主配置文件
│   │   └── theme/          # 自定义主题
│   │       ├── index.ts    # 主题入口
│   │       └── custom.css  # 自定义样式
│   ├── public/             # 静态资源
│   │   └── logo.svg        # 网站Logo
│   ├── catalog/            # 分类目录（自动生成）
│   ├── api/                # API数据（自动生成）
│   ├── index.md            # 首页
│   └── api.md              # API文档
├── tools/                  # 工具脚本
│   └── converter.py        # 文本转换工具
├── package.json            # 项目配置
└── README.md               # 本文件
```

## 🔧 数据转换

### 使用Python工具转换原始文本

```bash
# 安装Python依赖（如需要）
pip install dataclasses

# 转换文本
python tools/converter.py \
  --source "D:\道藏\道藏_txt" \
  --output .
```

该工具会：
1. 读取原始txt文件
2. 解析文件名提取分类、作者、朝代等信息
3. 转换为结构化的Markdown文件
4. 生成分类索引页
5. 生成JSON API数据

## 🌐 部署

### 方式一：静态托管（推荐）

构建后，将 `docs/.vitepress/dist` 目录部署到任意静态托管服务：

- **Vercel**: `vercel deploy`
- **Netlify**: 连接GitHub仓库，自动部署
- **GitHub Pages**: 使用GitHub Actions自动部署
- **Cloudflare Pages**: 连接仓库，自动构建

### 方式二：自有服务器

```bash
# 构建
npm run docs:build

# 上传到服务器
scp -r docs/.vitepress/dist/* user@your-server:/var/www/daozang/

# Nginx配置示例
cat > /etc/nginx/sites-available/daozang << 'EOF'
server {
    listen 80;
    server_name daozang.your-domain.com;
    
    root /var/www/daozang;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 缓存静态资源
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用站点
ln -s /etc/nginx/sites-available/daozang /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

### GitHub Actions自动部署

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      
      - run: npm ci
      - run: npm run docs:build
      
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs/.vitepress/dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

## 🎨 自定义

### 修改主题色

编辑 `docs/.vitepress/theme/custom.css`:

```css
:root {
  --vp-c-brand-1: #8b4513;  /* 主色调 */
  --vp-c-brand-2: #a0522d;  /* 辅助色 */
  --vp-c-brand-3: #cd853f;  /* 强调色 */
}
```

### 添加新经文

1. 将txt文件放入源目录
2. 运行转换工具
3. 重新构建网站

### 修改字体

编辑 `docs/.vitepress/config.mts`:

```typescript
head: [
  ['link', { 
    href: 'https://fonts.googleapis.com/css2?family=Your+Font&display=swap', 
    rel: 'stylesheet' 
  }]
]
```

然后在CSS中应用：

```css
:root {
  --vp-font-family-base: 'Your Font', serif;
}
```

## 📡 API使用

详见 [API文档](./docs/api.md)

### 示例：获取所有经文

```javascript
fetch('/api/index.json')
  .then(res => res.json())
  .then(data => {
    console.log(`总计 ${data.total_scriptures} 部经典`);
    for (const [category, info] of Object.entries(data.categories)) {
      console.log(`${category}: ${info.count}部`);
    }
  });
```

### 示例：AI调用

```python
import requests

# 获取经文索引
response = requests.get('https://your-domain.com/api/index.json')
index = response.json()

# 搜索特定经文
for scripture in index['categories']['正統道藏洞真部']['scriptures']:
    if '道德' in scripture['title']:
        print(scripture)
```

## 🤝 贡献

欢迎贡献！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 原始文本来源：《正统道藏》明万历刊本
- 网站框架：[VitePress](https://vitepress.dev/)
- 字体：[思源宋体](https://github.com/adobe-fonts/source-han-serif)
- 图标设计：太极八卦元素

## 📮 联系

- GitHub: [@DaimaRuge](https://github.com/DaimaRuge)
- 项目地址: [https://github.com/DaimaRuge/daozang-reader](https://github.com/DaimaRuge/daozang-reader)

---

<div align="center">

**道法自然 · 阅藏知津**

Made with ☯ by DaimaRuge

</div>
