import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(
    page_title="ISA - Intelligent Study Assistant",
    page_icon="🎓",
    layout="centered"
)

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 12px; border: 1px solid #f0f2f6; }
    .stStatusWidget { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.title("🎓 ISA: System Design Mentor")
st.caption("Expert Knowledge Engine | DDIA & Cloud Native Library")
st.divider()

# Initialize Conversation History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Handling
if prompt := st.chat_input("Ask about distributed systems or architectural trade-offs..."):
    # 1. User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Assistant Response with Professional Guardrails
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Using st.status to keep background logs (JSON) hidden from the final answer
        with st.status("🧠 Analyzing knowledge base & auditing...", expanded=False) as status:
            try:
                # Backend streaming endpoint
                backend_url = "http://localhost:8080/chat/stream"
                response = requests.post(
                    backend_url, 
                    json={"message": prompt}, 
                    stream=True,
                    timeout=60
                )
                response.raise_for_status()

                # Process raw stream chunks
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        # 🌟 DEFENSIVE FILTER: Catch and hide any internal JSON logic
                        # This ensures the user in Aspendale Gardens only sees clean text
                        if '"next_node"' in chunk or '"reasoning"' in chunk:
                            try:
                                # Log the internal decision inside the status box instead of chat
                                route_log = json.loads(chunk)
                                st.write(f"Agent Action: `{route_log.get('next_node', 'Thinking')}`")
                                continue
                            except:
                                continue # Skip if it's a malformed JSON fragment
                        
                        # Accumulate clean text content for Markdown rendering
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                
                # Final render without the cursor
                response_placeholder.markdown(full_response)
                status.update(label="✅ Verified by ISA Audit", state="complete")
                
                # Store cleaned message in session history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                status.update(label="❌ Engine Error", state="error")
                st.error(f"Backend connection failed. Please ensure Docker is running.")

# Sidebar Metadata (Project Proof-of-Work)
with st.sidebar:
    st.header("Project Specs")
    st.info("Vector Store: FAISS (CPU Optimized)")
    st.metric("Library Chunks", "2,244")
    st.success("Target: Sydney (AU-SE1)")
    
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()