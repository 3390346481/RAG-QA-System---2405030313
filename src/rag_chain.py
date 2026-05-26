from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from src.ollama_utils import get_ollama_llm
from src.vector_store import get_retriever

SYSTEM_PROMPT = """
你是一个基于知识库的智能问答助手。请根据提供的参考文档内容来回答用户的问题。

重要规则：
1. 必须严格基于提供的参考文档进行回答，不要使用文档外的知识。
2. 如果文档中没有相关信息，请明确回答"文档中未找到相关答案"。
3. 回答要简洁明了，直接针对问题进行回答。

参考文档：
{context}

用户问题：
{question}
"""

def create_rag_chain():
    llm = get_ollama_llm()
    retriever = get_retriever(k=3)
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": SYSTEM_PROMPT},
        return_source_documents=True
    )
    
    return chain

def ask_question(chain, question: str, chat_history: list = None) -> dict:
    if chat_history is None:
        chat_history = []
    
    result = chain({
        "question": question,
        "chat_history": chat_history
    })
    
    return {
        "answer": result.get("answer", ""),
        "source_documents": result.get("source_documents", []),
        "chat_history": result.get("chat_history", [])
    }

if __name__ == "__main__":
    chain = create_rag_chain()
    
    questions = [
        "What is natural language processing?",
        "What is machine learning?",
        "What is deep learning?",
        "How does NLP work?",
        "What are the applications of NLP?",
        "What is quantum computing?"
    ]
    
    chat_history = []
    for q in questions:
        print(f"Question: {q}")
        result = ask_question(chain, q, chat_history)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {[doc.metadata['source'] for doc in result['source_documents']]}")
        print("-" * 50)
        chat_history.append((q, result['answer']))
