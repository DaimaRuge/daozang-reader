import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '道藏',
  description: '《正统道藏》在线阅读 - 明代官修道藏全文',
  
  // 基础配置
  base: '/',
  cleanUrls: true,
  lastUpdated: true,
  
  // 主题配置
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: '道藏',
    
    // 导航
    nav: [
      { text: '首页', link: '/' },
      { text: '三洞', items: [
        { text: '洞真部', link: '/catalog/dongzhen' },
        { text: '洞玄部', link: '/catalog/dongxuan' },
        { text: '洞神部', link: '/catalog/dongshen' }
      ]},
      { text: '四辅', items: [
        { text: '太平部', link: '/catalog/taiping' },
        { text: '太玄部', link: '/catalog/taixuan' },
        { text: '太清部', link: '/catalog/taiqing' },
        { text: '正一部', link: '/catalog/zhengyi' }
      ]},
      { text: '续道藏', link: '/catalog/xudaozang' },
      { text: 'API', link: '/api' }
    ],
    
    // 侧边栏
    sidebar: {
      '/catalog/': [
        {
          text: '分类导航',
          items: [
            { text: '洞真部 (319)', link: '/catalog/dongzhen' },
            { text: '洞玄部 (303)', link: '/catalog/dongxuan' },
            { text: '洞神部 (364)', link: '/catalog/dongshen' },
            { text: '太平部 (65)', link: '/catalog/taiping' },
            { text: '太玄部 (113)', link: '/catalog/taixuan' },
            { text: '太清部 (24)', link: '/catalog/taiqing' },
            { text: '正一部 (237)', link: '/catalog/zhengyi' },
            { text: '续道藏 (59)', link: '/catalog/xudaozang' }
          ]
        }
      ]
    },
    
    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/DaimaRuge/daozang-reader' }
    ],
    
    // 搜索
    search: {
      provider: 'local',
      options: {
        detailedView: true
      }
    },
    
    // 页脚
    footer: {
      message: '基于《正统道藏》明万历刊本整理',
      copyright: '© 2026 道藏阅读平台 | 仅供学术研究'
    },
    
    // 大纲
    outline: {
      level: [2, 3],
      label: '目录'
    },
    
    // 文档页脚
    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },
    
    // 最后更新时间
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'short'
      }
    }
  },
  
  // Markdown配置
  markdown: {
    theme: {
      light: 'vitesse-light',
      dark: 'vitesse-dark'
    },
    lineNumbers: false,
    image: {
      lazyLoading: true
    }
  },
  
  // 头部配置
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg' }],
    ['meta', { name: 'theme-color', content: '#2c3e50' }],
    ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { href: 'https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=ZCOOL+XiaoWei&display=swap', rel: 'stylesheet' }]
  ],
  
  // 多语言（暂时只支持中文）
  lang: 'zh-CN'
})
