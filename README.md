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
