🎓 ISA: Intelligent Study Assistant (System Design Mentor)
ISA (Intelligent Study Assistant) is a production-ready, AI-driven mentoring engine designed to assist software engineers in mastering complex System Design concepts, distributed systems architecture, and Cloud-Native patterns.

Built with a robust LangGraph Multi-Agent architecture, ISA provides high-fidelity, audited answers backed by a specialized Retrieval-Augmented Generation (RAG) pipeline containing over 2,200 curated knowledge chunks.

🚀 Key Features
Multi-Agent Routing (LangGraph): Utilizes a central Supervisor node to intelligently route user queries to specialized agents (Answer Agent), ensuring high relevance and contextual accuracy.

Self-Correction & Auditing: Integrates an Eval Agent that critically reviews generated answers against the retrieved context. If an answer is deemed hallucinated or insufficient, the graph loops back for self-correction before presenting it to the user.

High-Fidelity RAG Pipeline: Powered by FAISS (CPU-optimized) and embedded with 2,244 high-density knowledge chunks sourced from foundational texts like Designing Data-Intensive Applications (DDIA).

Defensive Streaming UI: A professional Streamlit frontend featuring an asynchronous streaming generator. It implements strict node-level filtering to separate internal agent reasoning (JSON logs) from the clean, user-facing Markdown output.

Fully Serverless & CI/CD Integrated: Containerized via Docker and automatically deployed to Google Cloud Run (Sydney region) using GitHub Actions, demonstrating immutable infrastructure and secure secret management.

🏗️ System Architecture
Client Tier: Streamlit UI handles user inputs and renders chunked Server-Sent Events (SSE). Internal routing logs are caught and isolated in an expandable status widget.

API Tier: FastAPI backend exposes asynchronous endpoints (/chat/stream), utilizing astream_events to filter and yield tokens specifically from the answer_agent node.

Agentic Tier (LangGraph): * Supervisor: Intent classification and node routing.

Answer_Agent: Context synthesis and Markdown generation.

Eval_Agent: Quality assurance and hallucination detection.

Data Tier: In-memory FAISS vector store serving embedding representations of the knowledge base.

Gemini said
太棒了！跨过 CI/CD 这一关，你的 ISA (Intelligent Study Assistant) 已经是一套完整的云原生产品了。

作为你向 Senior AI/Software Engineer 转型的重要展示作品（Portfolio Piece），一份“超级专业”的 README 甚至比代码本身更重要。面试官和技术导师在看代码之前，第一眼看的就是架构设计文档。

这份 README 完全按照硅谷一线科技公司的开源项目标准编写，去掉了所有中文，强调了你的多智能体架构（Multi-Agent Architecture）、数据清洗策略以及云原生部署能力。

请直接将以下内容复制到你项目根目录的 README.md 文件中：

🎓 ISA: Intelligent Study Assistant (System Design Mentor)
ISA (Intelligent Study Assistant) is a production-ready, AI-driven mentoring engine designed to assist software engineers in mastering complex System Design concepts, distributed systems architecture, and Cloud-Native patterns.

Built with a robust LangGraph Multi-Agent architecture, ISA provides high-fidelity, audited answers backed by a specialized Retrieval-Augmented Generation (RAG) pipeline containing over 2,200 curated knowledge chunks.

🚀 Key Features
Multi-Agent Routing (LangGraph): Utilizes a central Supervisor node to intelligently route user queries to specialized agents (Answer Agent), ensuring high relevance and contextual accuracy.

Self-Correction & Auditing: Integrates an Eval Agent that critically reviews generated answers against the retrieved context. If an answer is deemed hallucinated or insufficient, the graph loops back for self-correction before presenting it to the user.

High-Fidelity RAG Pipeline: Powered by FAISS (CPU-optimized) and embedded with 2,244 high-density knowledge chunks sourced from foundational texts like Designing Data-Intensive Applications (DDIA).

Defensive Streaming UI: A professional Streamlit frontend featuring an asynchronous streaming generator. It implements strict node-level filtering to separate internal agent reasoning (JSON logs) from the clean, user-facing Markdown output.

Fully Serverless & CI/CD Integrated: Containerized via Docker and automatically deployed to Google Cloud Run (Sydney region) using GitHub Actions, demonstrating immutable infrastructure and secure secret management.

🏗️ System Architecture
Client Tier: Streamlit UI handles user inputs and renders chunked Server-Sent Events (SSE). Internal routing logs are caught and isolated in an expandable status widget.

API Tier: FastAPI backend exposes asynchronous endpoints (/chat/stream), utilizing astream_events to filter and yield tokens specifically from the answer_agent node.

Agentic Tier (LangGraph): * Supervisor: Intent classification and node routing.

Answer_Agent: Context synthesis and Markdown generation.

Eval_Agent: Quality assurance and hallucination detection.

Data Tier: In-memory FAISS vector store serving embedding representations of the knowledge base.

💻 Tech Stack
Component	Technology	Description
Frontend	Streamlit	Reactive UI with custom CSS and defensive streaming renderers.
Backend	FastAPI, Uvicorn	High-performance async REST API.
AI/Orchestration	LangChain, LangGraph	LLM integration, tool binding, and cyclic graph state management.
Vector Database	FAISS	Efficient similarity search and clustering of dense vectors.
Infrastructure	Docker, GCP Cloud Run	Serverless container hosting with automated scaling (--memory=2Gi).
CI/CD	GitHub Actions	Automated build, artifact registry push, and deployment pipeline.
🛠️ Local Development
Prerequisites
Docker & Docker Compose

OpenAI API Key

Quick Start
Clone the repository:

Bash
git clone https://github.com/yourusername/isa-ai-tutor.git
cd isa-ai-tutor
Set up environment variables:
Create a .env file in the root directory (this file is git-ignored):

Code snippet
OPENAI_API_KEY=sk-your-api-key-here
Build and run via Docker:

Bash
docker build -t isa-mentor-local .
docker run --rm -p 8080:8080 --env-file .env isa-mentor-local
Access the application:
Open your browser and navigate to http://localhost:8080 (or the mapped Streamlit port).

☁️ Deployment (CI/CD)
This project utilizes a fully automated CI/CD pipeline via GitHub Actions.

Any push to the main branch triggers the cloudrun-deploy.yml workflow, which:

Authenticates with Google Cloud via securely injected Service Account credentials.

Builds a new Docker image tagged with the specific Git commit SHA.

Pushes the artifact to GCP Artifact Registry (australia-southeast1).

Deploys the revision to Cloud Run, injecting the OPENAI_API_KEY dynamically at runtime to ensure zero-trust security.
