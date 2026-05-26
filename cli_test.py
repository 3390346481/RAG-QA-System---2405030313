import os
from src.document_loader import load_documents_from_folder
from src.text_processor import process_documents
from src.vector_store import add_documents_to_vector_store, get_vector_store_stats, clear_vector_store
from src.rag_chain import create_rag_chain, ask_question

def main():
    print("=== RAG智能问答系统 - 命令行测试版 ===")
    
    clear_vector_store()
    print("已清空向量数据库")
    
    documents = load_documents_from_folder("docs")
    print(f"从docs文件夹加载了 {len(documents)} 个文档")
    
    if not documents:
        print("未找到任何文档，请先在docs文件夹中放置PDF或DOCX文件")
        return
    
    processed_docs = process_documents(documents)
    print(f"文本分块完成，共生成 {len(processed_docs)} 个文本块")
    
    add_documents_to_vector_store(processed_docs)
    print("已将文本块存入向量数据库")
    
    stats = get_vector_store_stats()
    print(f"向量数据库状态: {stats}")
    
    chain = create_rag_chain()
    print("RAG问答链已创建")
    
    print("\n=== 开始问答测试 ===")
    questions = [
        "什么是自然语言处理？",
        "NLP的主要应用领域有哪些？",
        "Transformer模型是什么？",
        "什么是词向量？",
        "机器学习和深度学习的区别是什么？",
        "什么是量子计算？",
        "人工智能的历史发展"
    ]
    
    chat_history = []
    for q in questions:
        print(f"\n问题: {q}")
        result = ask_question(chain, q, chat_history)
        print(f"答案: {result['answer']}")
        sources = [doc.metadata['source'] for doc in result['source_documents']]
        print(f"来源文档: {', '.join(sources)}")
        chat_history.append((q, result['answer']))
    
    print("\n=== 交互式问答（输入 'quit' 退出）===")
    while True:
        question = input("请输入问题: ")
        if question.lower() == "quit":
            break
        result = ask_question(chain, question, chat_history)
        print(f"答案: {result['answer']}")
        chat_history.append((question, result['answer']))

if __name__ == "__main__":
    main()
