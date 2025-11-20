# **Enterprise RAG & Workflow Automation Hub**  
### **AI + MCP + GCP + Workflow Orchestration**

A production-grade enterprise AI system integrating **Google Cloud**, **BigQuery**, **Cloud Storage**, intelligent **AI Agents**, and **MCP servers** for workflow automation, document intelligence, and enterprise reasoning.

---

##  **System Status (Verified)**

✔️ Backend API running on GCP Cloud Shell  
✔️ MCP Servers active (BigQuery + GCS)  
✔️ Router Agent performing intent detection  
✔️ RAG Agent performing document Q&A  
✔️ Workflow automation functioning end-to-end  
✔️ Ready for Cloud Run deployment  

---

##  **Demo Commands**

### **1. Create sample enterprise data**
```bash
python scripts/generate_demo_data.py
```

### **2. Start Backend FastAPI Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### **3. Trigger Workflow**
```bash
curl -X POST "http://localhost:8080/run_workflow" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "demo_1.pdf"}'
```

---

##  **Architecture Overview**

### **Core Components**
- **FastAPI Backend**  
  REST API layer coordinating workflow, routing, and agent responses.

- **MCP Servers**  
  - **BigQuery MCP** → enterprise structured data retrieval  
  - **GCS MCP** → file/document management & metadata  

- **AI Router Agent**  
  Performs intent detection to route tasks intelligently.

- **RAG Agent**  
  Executes hybrid retrieval + generative reasoning.

- **Workflow Orchestrator**  
  Manages multi-step business workflows (summaries, extraction, classification).

---

##  **Deployment Options**

### **Docker**
```bash
docker build -t enterprise-rag .
docker run -p 8080:8080 enterprise-rag
```

### **Kubernetes (GKE)**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### **Google Cloud Run**
```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/enterprise-rag
gcloud run deploy enterprise-rag \
  --image gcr.io/$PROJECT_ID/enterprise-rag \
  --region us-central1 \
  --platform managed
```

---

##  **Project Structure**
```
enterprise-rag-automation/
│
├── app/
│   ├── main.py               # FastAPI backend
│   ├── router_agent.py       # Intent router agent
│   ├── rag_agent.py          # RAG pipeline agent
│   ├── workflow.py           # Workflow orchestrator
│   └── utils/
│
├── mcp_servers/
│   ├── bigquery_mcp/
│   └── gcs_mcp/
│
├── docker/
│   ├── Dockerfile
│   └── entrypoint.sh
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── scripts/
│   └── generate_demo_data.py
│
└── README.md
```

---

##  **Technologies Used**
- **FastAPI** — high-performance backend framework  
- **Google Cloud Run / GKE** — scalable serverless compute  
- **BigQuery** — analytical enterprise data warehouse  
- **Cloud Storage** — file and document management  
- **MCP Protocol** — standardized interface for AI tools  
- **Docker** — consistent portable containerization  
- **Python** — flexible enterprise logic layer  

---

##  **Why FastAPI?**
FastAPI is used because it provides:

- Extremely fast performance (thanks to **ASGI + Uvicorn**)  
- Automatic Swagger UI (`/docs`)  
- Seamless async support for parallel workflows  
- Perfect for microservices in **Cloud Run / GKE**  
- Cleaner structure compared to Flask for enterprise apps  

---

##  **Use Cases**
✔️ Automated enterprise document workflows  
✔️ Financial/BFSI document intelligence  
✔️ Contract summarization and compliance checks  
✔️ Retrieval-augmented analytics using BigQuery  
✔️ Multi-step business logic powered by AI agents  

---

