import streamlit as st
import os
import tempfile
from src.document_loader import load_document
from src.text_processor import process_document
from src.vector_store import add_documents_to_vector_store, get_vector_store_stats, clear_vector_store
from src.rag_chain import create_rag_chain, ask_question

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'rag_chain' not in st.session_state:
        st.session_state.rag_chain = None
    if 'vector_store_initialized' not in st.session_state:
        st.session_state.vector_store_initialized = False

def main():
    st.set_page_config(page_title="RAG智能问答系统", page_icon="📚", layout="wide")
    
    initialize_session_state()
    
    st.title("📚 基于本地知识库的RAG智能问答系统")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("知识库管理")
        
        uploaded_files = st.file_uploader(
            "上传文档（支持PDF/DOCX）",
            type=["pdf", "docx"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
        
        if st.button("📥 构建知识库", type="primary"):
            if not st.session_state.uploaded_files:
                st.warning("请先上传文档")
                return
            
            with st.spinner("正在处理文档..."):
                clear_vector_store()
                
                all_docs = []
                for uploaded_file in st.session_state.uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    
                    text = load_document(tmp_path)
                    if text.strip():
                        docs = process_document(text, uploaded_file.name)
                        all_docs.extend(docs)
                    
                    os.unlink(tmp_path)
                
                if all_docs:
                    add_documents_to_vector_store(all_docs)
                    st.session_state.vector_store_initialized = True
                    st.session_state.rag_chain = create_rag_chain()
                    st.success(f"✅ 知识库构建完成！共处理 {len(st.session_state.uploaded_files)} 个文档，生成 {len(all_docs)} 个文本块")
                else:
                    st.error("未能从文档中提取有效内容")
        
        if st.button("🗑️ 清空知识库"):
            clear_vector_store()
            st.session_state.vector_store_initialized = False
            st.session_state.rag_chain = None
            st.session_state.chat_history = []
            st.success("知识库已清空")
        
        stats = get_vector_store_stats()
        st.info(f"📊 当前知识库状态：\n- 文本块数量: {stats.get('document_count', 0)}")
        
        if st.session_state.uploaded_files:
            st.subheader("已上传文档")
            for i, file in enumerate(st.session_state.uploaded_files):
                st.write(f"{i+1}. {file.name}")
    
    with col2:
        st.header("问答交互")
        
        if not st.session_state.vector_store_initialized:
            st.info("请先在左侧上传文档并构建知识库")
            return
        
        if st.session_state.chat_history:
            st.subheader("对话历史")
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                with st.chat_message("user"):
                    st.write(f"**用户:** {question}")
                with st.chat_message("assistant"):
                    st.write(f"**助手:** {answer}")
        
        user_question = st.text_input("请输入您的问题：")
        
        if st.button("🔍 提问", type="primary"):
            if not user_question.strip():
                st.warning("请输入问题")
                return
            
            with st.spinner("正在思考..."):
                result = ask_question(
                    st.session_state.rag_chain,
                    user_question,
                    st.session_state.chat_history
                )
                
                st.session_state.chat_history.append((user_question, result['answer']))
                
                st.subheader("回答")
                st.write(result['answer'])
                
                if result['source_documents']:
                    st.subheader("参考来源")
                    sources = set([doc.metadata['source'] for doc in result['source_documents']])
                    for source in sources:
                        st.write(f"- {source}")

if __name__ == "__main__":
    main()
