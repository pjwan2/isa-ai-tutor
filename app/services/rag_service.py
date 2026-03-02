import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

class RAGService:
    # 🌟 Staff Fix: Added 'index_dir' to the signature
    def __init__(self, data_dir: str, index_dir: str):
        self.data_dir = data_dir
        self.index_dir = index_dir
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = None
        self._load_or_build_index()

    def _load_or_build_index(self):
        # Check if the folder exists AND contains the FAISS index file
        index_file = os.path.join(self.index_dir, "index.faiss")
        
        if os.path.exists(index_file):
            print(f"[*] Found local index at {self.index_dir}. Loading...")
            self.vectorstore = FAISS.load_local(
                self.index_dir, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            print("[*] Persistent index loaded successfully.")
        else:
            print("[*] No local index found. Starting fresh indexing...")
            self._build_and_save_index()

    def _build_and_save_index(self):
        print(f"📥 Loading PDFs from {self.data_dir}...")
        loader = PyPDFDirectoryLoader(self.data_dir)
        docs = loader.load()
        
        if not docs:
            raise ValueError(f"No PDFs found in {self.data_dir}!")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", "", "。", "！", "？"]
        )
        splits = text_splitter.split_documents(docs)
        print(f"✂️  Created {len(splits)} chunks. Generating embeddings...")
        
        # Build and Save
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        self.vectorstore.save_local(self.index_dir)
        print(f"[*] Index successfully built and saved to: {self.index_dir}")

    def query(self, text: str, k: int = 3):
        return self.vectorstore.similarity_search(text, k=k)

# --- Path Injection Logic ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))

data_path = os.path.join(project_root, "data")
index_path = os.path.join(project_root, "faiss_index")

# Now this call will match the __init__(self, data_dir, index_dir) signature
rag_service = RAGService(data_path, index_path)