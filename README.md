# RAG智能问答系统

基于本地知识库的检索增强生成（RAG）智能问答系统，使用Ollama本地大模型、LangChain框架和Streamlit构建。

## 功能特点

- 📚 支持PDF和DOCX文档的批量上传
- 🔍 基于Chroma向量数据库的相似性检索
- 💬 支持多轮对话，具有会话记忆功能
- 🖥️ 可视化Web界面，操作简单便捷
- 📦 可打包成独立的exe可执行文件

## 环境要求

- Python 3.10+
- Ollama（用于部署本地大模型）
- 推荐模型：deepseek-r1:7b 或 qwen2:7b

## 安装步骤

1. **安装Ollama**
   - 下载地址：https://ollama.com/
   - 安装完成后运行命令下载模型：
     ```bash
     ollama pull deepseek-r1:7b
     ollama pull nomic-embed-text
     ```

2. **创建虚拟环境并安装依赖**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

## 使用说明

### 运行Web应用

```bash
streamlit run app.py
```

### 使用步骤

1. 在左侧面板上传PDF或DOCX格式的文档
2. 点击"构建知识库"按钮，系统会自动解析文档并构建向量数据库
3. 在右侧问答交互区输入问题，点击"提问"获取答案
4. 系统会显示回答及参考来源文档

### 命令行测试

```bash
python cli_test.py
```

## 关键技术点

### RAG流程
1. **文档加载**：支持PDF和DOCX格式文档的读取
2. **文本分块**：使用RecursiveCharacterTextSplitter，chunk_size=1000，chunk_overlap=200
3. **向量化存储**：使用Ollama的nomic-embed-text模型将文本块向量化，存入Chroma向量数据库
4. **相似性检索**：根据用户查询返回最相关的3个文本块
5. **问答生成**：使用ConversationalRetrievalChain连接检索器和大模型

### 模型配置
- 大语言模型：deepseek-r1:7b（可配置为qwen2:7b等其他模型）
- 嵌入模型：nomic-embed-text
- 向量数据库：Chroma

## 项目结构

```
RAG-QA-System/
├── src/
│   ├── ollama_utils.py      # Ollama模型工具函数
│   ├── document_loader.py   # 文档加载模块
│   ├── text_processor.py    # 文本分块处理
│   ├── vector_store.py      # 向量数据库管理
│   └── rag_chain.py         # RAG问答链
├── docs/                    # 示例文档目录
├── vector_db/               # 向量数据库存储目录（自动生成）
├── app.py                   # Streamlit Web应用
├── cli_test.py              # 命令行测试脚本
├── test_ollama.py           # Ollama连接测试
├── requirements.txt         # 依赖包列表
└── README.md               # 项目说明文档
```

## 项目效果截图

### 界面截图1：主界面
![主界面](screenshots/main_interface.png)

### 界面截图2：文档上传与知识库构建
![文档上传](screenshots/document_upload.png)

### 界面截图3：问答交互示例
![问答示例](screenshots/qa_example.png)

## 问答示例

**问题1：什么是自然语言处理？**
- 回答：自然语言处理（NLP）是计算机科学、人工智能和语言学的交叉领域，致力于使计算机能够理解、解释和生成人类语言。

**问题2：Transformer模型是什么？**
- 回答：Transformer模型是NLP领域的重大突破，由Google在2017年提出。它使用自注意力机制来处理序列数据。

**问题3：什么是量子计算？**
- 回答：文档中未找到相关答案

## 已知问题与改进方向

- [ ] 支持更多文档格式（如TXT、Markdown）
- [ ] 优化文本分块策略
- [ ] 增加文档摘要功能
- [ ] 支持多语言问答
- [ ] 优化界面响应速度

## License

MIT License
