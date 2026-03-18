# 部署指南

本文档介绍如何在您的VPS上部署道藏阅读平台。

## 📋 前置要求

- VPS服务器（推荐配置：1核1G内存以上）
- 操作系统：Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- 域名（可选，但推荐）
- 已安装：Node.js 18+, Nginx

## 🚀 方式一：使用Vercel/Netlify（推荐，最简单）

### Vercel部署

1. Fork本项目到您的GitHub账号
2. 访问 [vercel.com](https://vercel.com)
3. 导入您的GitHub仓库
4. Vercel会自动检测VitePress项目并部署
5. 绑定自定义域名（可选）

**优势**：
- 免费SSL证书
- 全球CDN加速
- 自动CI/CD
- 零运维成本

### Netlify部署

1. Fork项目
2. 访问 [netlify.com](https://netlify.com)
3. 连接GitHub仓库
4. 构建命令：`npm run docs:build`
5. 发布目录：`docs/.vitepress/dist`

## 🖥️ 方式二：自有VPS部署

### 步骤1：准备服务器

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 安装Nginx
sudo apt install -y nginx

# 安装Git
sudo apt install -y git
```

### 步骤2：获取代码

```bash
# 创建应用目录
sudo mkdir -p /var/www/daozang
sudo chown $USER:$USER /var/www/daozang

# 克隆代码
cd /var/www/daozang
git clone https://github.com/DaimaRuge/daozang-reader.git .

# 安装依赖
npm install
```

### 步骤3：构建静态文件

```bash
# 构建生产版本
npm run docs:build

# 构建产物在 docs/.vitepress/dist
```

### 步骤4：配置Nginx

```bash
# 创建Nginx配置
sudo tee /etc/nginx/sites-available/daozang << 'EOF'
server {
    listen 80;
    server_name daozang.your-domain.com;  # 改为您的域名
    
    root /var/www/daozang/docs/.vitepress/dist;
    index index.html;
    
    # 启用gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_min_length 1000;
    
    # SPA路由
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 缓存静态资源
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # 访问日志
    access_log /var/log/nginx/daozang.access.log;
    error_log /var/log/nginx/daozang.error.log;
}
EOF

# 启用站点
sudo ln -s /etc/nginx/sites-available/daozang /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 步骤5：配置HTTPS（推荐）

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d daozang.your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 步骤6：设置自动部署（可选）

创建自动部署脚本：

```bash
cat > /var/www/daozang/deploy.sh << 'EOF'
#!/bin/bash
set -e

cd /var/www/daozang

# 拉取最新代码
git pull origin main

# 安装依赖（如有更新）
npm install

# 构建
npm run docs:build

# 重启Nginx（可选）
# sudo systemctl reload nginx

echo "部署完成！$(date)"
EOF

chmod +x /var/www/daozang/deploy.sh
```

#### 使用Webhook自动部署

1. 安装webhook：

```bash
sudo apt install -y webhook
```

2. 创建hook配置：

```bash
sudo tee /etc/webhook.conf << 'EOF'
[
  {
    "id": "daozang-deploy",
    "execute-command": "/var/www/daozang/deploy.sh",
    "command-working-directory": "/var/www/daozang",
    "response-message": "Deploying...",
    "trigger-rule": {
      "match": {
        "type": "payload-hmac-sha256",
        "secret": "your-webhook-secret",
        "parameter": {
          "source": "header",
          "name": "X-Hub-Signature-256"
        }
      }
    }
  }
]
EOF
```

3. 启动webhook服务：

```bash
sudo tee /etc/systemd/system/webhook.service << 'EOF'
[Unit]
Description=Webhook Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/webhook -hooks /etc/webhook.conf -verbose
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable webhook
sudo systemctl start webhook
```

4. 在GitHub仓库设置中添加Webhook：
   - URL: `http://your-vps-ip:9000/hooks/daozang-deploy`
   - Secret: `your-webhook-secret`
   - Content type: `application/json`

## 🐳 方式三：Docker部署

### 创建Dockerfile

```dockerfile
# 构建阶段
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run docs:build

# 运行阶段
FROM nginx:alpine

COPY --from=builder /app/docs/.vitepress/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 构建和运行

```bash
# 构建镜像
docker build -t daozang-reader .

# 运行容器
docker run -d -p 80:80 --name daozang daozang-reader
```

### 使用Docker Compose

```yaml
version: '3'

services:
  daozang:
    build: .
    ports:
      - "80:80"
    restart: unless-stopped
```

```bash
docker-compose up -d
```

## 🔄 更新维护

### 手动更新

```bash
cd /var/www/daozang
git pull
npm install
npm run docs:build
```

### 查看日志

```bash
# Nginx访问日志
sudo tail -f /var/log/nginx/daozang.access.log

# Nginx错误日志
sudo tail -f /var/log/nginx/daozang.error.log
```

### 性能优化

1. **启用HTTP/2**：

```nginx
# 在Nginx配置中添加
listen 443 ssl http2;
```

2. **启用Brotli压缩**：

```bash
# 安装模块
sudo apt install -y libnginx-mod-http-brotli

# Nginx配置
brotli on;
brotli_types text/plain text/css application/json application/javascript text/xml application/xml;
```

3. **配置CDN**：

推荐使用Cloudflare CDN：
- 免费SSL
- 全球CDN加速
- DDoS防护
- 缓存优化

## 📊 监控

### 安装监控工具

```bash
# 安装PM2（进程管理）
sudo npm install -g pm2

# 创建静态文件服务器进程
pm2 serve /var/www/daozang/docs/.vitepress/dist 8080 --name daozang

# 保存PM2配置
pm2 save
pm2 startup
```

### 监控命令

```bash
pm2 status        # 查看状态
pm2 logs daozang  # 查看日志
pm2 monit         # 实时监控
```

## 🔒 安全建议

1. **配置防火墙**：

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

2. **定期更新系统**：

```bash
sudo apt update && sudo apt upgrade -y
```

3. **配置Fail2Ban**（防暴力破解）：

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

4. **限制SSH访问**：

```bash
# 编辑 /etc/ssh/sshd_config
Port 2222  # 改用非标准端口
PermitRootLogin no
```

## 🆘 故障排查

### 网站无法访问

1. 检查Nginx状态：`sudo systemctl status nginx`
2. 检查端口：`sudo netstat -tlnp | grep :80`
3. 查看错误日志：`sudo tail -f /var/log/nginx/error.log`

### 构建失败

1. 检查Node.js版本：`node -v`（需要18+）
2. 删除依赖重装：`rm -rf node_modules && npm install`
3. 清除缓存：`npm cache clean --force`

### HTTPS证书问题

1. 检查域名解析：`nslookup daozang.your-domain.com`
2. 手动续期：`sudo certbot renew`
3. 查看证书状态：`sudo certbot certificates`

## 📮 技术支持

- GitHub Issues: https://github.com/DaimaRuge/daozang-reader/issues
- 文档: https://github.com/DaimaRuge/daozang-reader

---

**祝您部署顺利！** 🎉
