# API 文档

道藏阅读平台提供结构化的JSON API，便于开发者、AI模型调用和查询。

## 📡 API端点

### 获取总索引

```http
GET /api/index.json
```

**返回示例**：

```json
{
  "generated_at": "2026-03-19T03:52:00",
  "total_scriptures": 1504,
  "categories": {
    "正統道藏洞真部": {
      "slug": "dongzhen",
      "count": 319,
      "scriptures": [
        {
          "title": "大洞玉經",
          "dynasty": "宋元間",
          "author": "趙真人",
          "path": "/catalog/dongzhen/正統道藏洞真部本文類-大洞玉經"
        }
      ]
    }
  }
}
```

### 按分类获取

```http
GET /api/catalog/{category}.json
```

**参数**：
- `category`: 分类名称
  - `dongzhen` - 洞真部
  - `dongxuan` - 洞玄部
  - `dongshen` - 洞神部
  - `taiping` - 太平部
  - `taixuan` - 太玄部
  - `taiqing` - 太清部
  - `zhengyi` - 正一部
  - `xudaozang` - 续道藏

**返回示例**：

```json
{
  "category": "正統道藏洞真部",
  "count": 319,
  "subcategories": {
    "本文類": {
      "count": 50,
      "scriptures": [...]
    },
    "玉訣類": {
      "count": 30,
      "scriptures": [...]
    }
  }
}
```

### 获取单篇经文

```http
GET /api/scripture/{path}.json
```

**返回示例**：

```json
{
  "title": "大洞玉經",
  "category": "正統道藏洞真部本文類",
  "dynasty": "宋元間",
  "author": "趙真人",
  "content": "经文全文...",
  "metadata": {
    "word_count": 12345,
    "source": "明万历刊本"
  }
}
```

## 🔍 搜索API

### 全文搜索

```http
GET /api/search?q={keyword}
```

**参数**：
- `q`: 搜索关键词
- `category`: （可选）限定分类
- `dynasty`: （可选）限定朝代
- `limit`: （可选）返回数量，默认20

**返回示例**：

```json
{
  "query": "道德经",
  "total": 15,
  "results": [
    {
      "title": "道德真經",
      "category": "洞神部本文類",
      "author": "老子",
      "excerpt": "道可道，非常道...",
      "path": "/catalog/dongshen/道德真經"
    }
  ]
}
```

## 🤖 AI调用示例

### Python示例

```python
import requests

# 获取总索引
response = requests.get('https://daozang.example.com/api/index.json')
data = response.json()

# 遍历所有经文
for category, info in data['categories'].items():
    print(f"{category}: {info['count']}部")
    for scripture in info['scriptures']:
        print(f"  - {scripture['title']}")
```

### 使用LangChain

```python
from langchain.document_loaders import JSONLoader

# 加载道藏索引
loader = JSONLoader(
    file_path='./api/index.json',
    jq_schema='.categories',
    text_content=False
)
documents = loader.load()

# 现在可以在RAG系统中使用
```

### 使用OpenAI Function Calling

```python
import openai

functions = [
    {
        "name": "search_daozang",
        "description": "搜索道藏经文",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词"
                },
                "category": {
                    "type": "string",
                    "enum": ["dongzhen", "dongxuan", "dongshen", "taiping", "taixuan", "taiqing", "zhengyi", "xudaozang"],
                    "description": "经文分类"
                }
            },
            "required": ["query"]
        }
    }
]

# GPT可以调用此函数查询道藏内容
```

## 📊 数据格式

### Scripture对象

```typescript
interface Scripture {
  title: string;        // 经文名称
  category: string;     // 所属分类
  subcategory?: string; // 子分类
  dynasty?: string;     // 朝代
  author?: string;      // 作者
  path: string;         // 访问路径
  word_count?: number;  // 字数
  excerpt?: string;     // 摘要
}
```

### Category对象

```typescript
interface Category {
  name: string;         // 分类名称
  slug: string;         // URL slug
  count: number;        // 经文数量
  description?: string; // 分类说明
  scriptures: Scripture[];
}
```

## ⚡ 性能优化

### 缓存策略

- 静态JSON文件，CDN缓存
- 建议客户端缓存1小时
- 索引文件每周更新

### 分页

对于大量数据，建议使用分页：

```http
GET /api/catalog/dongzhen.json?page=1&limit=50
```

## 🔒 使用限制

- 本API仅供学术研究使用
- 请勿滥用，建议添加适当延迟
- 商业使用需联系授权
- 建议缓存结果，避免重复请求

## 📮 示例应用

### 1. 道藏问答机器人

```python
def answer_daozang_question(question: str) -> str:
    # 1. 使用LLM提取关键词
    keywords = extract_keywords(question)
    
    # 2. 搜索相关经文
    results = search_daozang(keywords)
    
    # 3. 使用RAG生成答案
    context = '\n\n'.join([r['content'] for r in results])
    answer = llm.generate(question, context)
    
    return answer
```

### 2. 经文推荐系统

```python
def recommend_scriptures(user_interests: List[str]) -> List[Scripture]:
    # 基于用户兴趣推荐经文
    all_scriptures = get_all_scriptures()
    
    scored = []
    for s in all_scriptures:
        score = calculate_relevance(s, user_interests)
        scored.append((s, score))
    
    return sorted(scored, key=lambda x: x[1], reverse=True)[:10]
```

### 3. 数据可视化

```javascript
// 使用D3.js展示分类统计
d3.json('/api/index.json').then(data => {
  const chart = PieChart()
    .data(Object.entries(data.categories).map(([k, v]) => ({
      label: k,
      value: v.count
    })));
  
  // 渲染图表...
});
```

## 🛠️ 本地部署

```bash
# 克隆仓库
git clone https://github.com/DaimaRuge/daozang-reader.git

# 安装依赖
npm install

# 构建静态文件
npm run docs:build

# API文件在 docs/public/api/ 目录
# 可部署到任意静态托管服务
```

## 📚 更多资源

- [VitePress文档](https://vitepress.dev/)
- [GitHub仓库](https://github.com/DaimaRuge/daozang-reader)
- [原始文本库](https://github.com/DaimaRuge/daozang-text)

---

<div class="api-note">

💡 **提示**: 本API为静态JSON文件，可直接通过HTTP访问，无需认证。适合嵌入各类应用和AI系统。

</div>
