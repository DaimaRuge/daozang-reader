---
layout: home

hero:
  name: 道藏
  text: 《正统道藏》在线阅读平台
  tagline: 明代官修道藏 · 三洞四辅 · 1504部经典
  image:
    src: /logo.svg
    alt: 道藏
  actions:
    - theme: brand
      text: 开始阅读
      link: /catalog/dongzhen
    - theme: alt
      text: API文档
      link: /api
    - theme: alt
      text: GitHub
      link: https://github.com/DaimaRuge/daozang-reader

features:
  - icon: 📖
    title: 三洞四辅
    details: 完整收录洞真、洞玄、洞神三部，及太平、太玄、太清、正一四辅，共1504部经典。
  
  - icon: 🔍
    title: 全文检索
    details: 内置全文搜索功能，快速定位经文内容，支持关键词高亮显示。
  
  - icon: 📱
    title: 多端适配
    details: 响应式设计，完美支持PC、平板、手机等多种设备阅读。
  
  - icon: 🎨
    title: 古典排版
    details: 采用中国传统配色与字体，宣纸色背景，营造沉浸式阅读体验。
  
  - icon: 🤖
    title: AI友好
    details: 提供结构化JSON API，便于大模型、小模型调用和查询。
  
  - icon: ⚡
    title: 极速加载
    details: 静态网站架构，CDN加速，毫秒级响应，流畅阅读体验。
---

<style>
:root {
  --vp-home-hero-name-color: transparent;
  --vp-home-hero-name-background: -webkit-linear-gradient(135deg, #8b4513 0%, #cd853f 100%);
  --vp-home-hero-image-background-image: linear-gradient(135deg, #8b4513 50%, #cd853f 50%);
  --vp-home-hero-image-filter: blur(44px);
}

.VPHero .image-bg {
  transition: all 0.5s ease;
}

@media (min-width: 640px) {
  :root {
    --vp-home-hero-image-filter: blur(56px);
  }
}

@media (min-width: 960px) {
  :root {
    --vp-home-hero-image-filter: blur(68px);
  }
}
</style>

<div class="intro-section">

## 📚 关于道藏

《正统道藏》是明代第43代天师张宇初奉敕编纂的道教经典总集，刊成于正统十年（1445年），共480函，5305卷。万历三十五年（1607年），第50代天师张国祥奉命续补《续道藏》180卷。这是现存最早的官修道藏，也是研究道教文献的重要资料。

## 🗂️ 分类体系

道藏按"三洞四辅"体系分类：

### 三洞（Three Caverns）

| 部类 | 文献数 | 说明 |
|------|--------|------|
| **洞真部** | 319部 | 上清经系，主修存思服气 |
| **洞玄部** | 303部 | 灵宝经系，主修斋醮科仪 |
| **洞神部** | 364部 | 三皇经系，主修符箓禁咒 |

### 四辅（Four Supplements）

| 部类 | 文献数 | 说明 |
|------|--------|------|
| **太平部** | 65部 | 辅助洞玄部，重社会教化 |
| **太玄部** | 113部 | 辅助洞真部，重哲理玄学 |
| **太清部** | 24部 | 辅助洞神部，重外丹服食 |
| **正一部** | 237部 | 通辅三洞，为天师道经典 |

### 续道藏

| 部类 | 文献数 | 说明 |
|------|--------|------|
| **续道藏** | 59部 | 明万历年间续补文献 |

## 🎯 快速导航

<div class="quick-links">

[📖 洞真部](/catalog/dongzhen) - 上清经系经典  
[📖 洞玄部](/catalog/dongxuan) - 灵宝经系经典  
[📖 洞神部](/catalog/dongshen) - 三皇经系经典  
[📖 太平部](/catalog/taiping) - 太平经系文献  
[📖 太玄部](/catalog/taixuan) - 玄学哲理文献  
[📖 太清部](/catalog/taiqing) - 外丹服食文献  
[📖 正一部](/catalog/zhengyi) - 天师道经典  
[📖 续道藏](/catalog/xudaozang) - 明代续补文献  

</div>

## 🌟 特色功能

- **古风设计**：水墨风格配色，思源宋体，营造沉浸式阅读体验
- **全文检索**：内置搜索功能，快速定位经文
- **多端适配**：响应式设计，支持PC、平板、手机
- **AI友好**：提供JSON API，便于程序调用
- **开源免费**：所有内容开源，仅供学术研究使用

## 📮 使用说明

本站所有文献仅供学术研究使用，原始文本来自《正统道藏》明万历刊本整理。如有引用，请注明出处。

</div>

<style>
.intro-section {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.quick-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.quick-links a {
  display: block;
  padding: 1rem 1.5rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border);
  border-radius: 8px;
  transition: all 0.3s;
}

.quick-links a:hover {
  background: var(--vp-c-bg);
  border-color: var(--vp-c-brand-1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
