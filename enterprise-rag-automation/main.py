"""
Enterprise RAG & Workflow Automation Hub
Main application that orchestrates MCP servers and AI agents
This demonstrates production-level system architecture
"""
from flask import Flask, request, jsonify, render_template
import json
import sys
import os

# Add our modules to path
sys.path.append('mcp_servers')
sys.path.append('agents')
sys.path.append('configs')

# Import our components
from mcp_servers.bigquery_server import handle_bigquery_request
from mcp_servers.gcs_server import handle_gcs_request
from agents.router_agent import RouterAgent
from agents.rag_agent import RAGAgent

app = Flask(__name__)

# Initialize agents
router_agent = RouterAgent()
rag_agent = RAGAgent()

print("🚀 Enterprise RAG & Workflow Automation Hub Starting...")
print("✅ MCP Servers: BigQuery, GCS")
print("✅ AI Agents: Router, RAG")
print("✅ GCP Integration: Active")

class EnterpriseAutomationHub:
    def __init__(self):
        self.workflow_history = []
        print("🏢 Enterprise Automation Hub Initialized")
    
    def process_user_request(self, user_input):
        """Main processing pipeline - demonstrates enterprise workflow orchestration"""
        print(f"\n🎯 Processing: {user_input}")
        
        # Step 1: Route intent
        intent_analysis = router_agent.analyze_intent(user_input)
        print(f"📡 Intent Analysis: {intent_analysis}")
        
        # Step 2: Route to services
        actions = router_agent.route_to_services(user_input, intent_analysis)
        print(f"🎯 Actions: {actions}")
        
        # Step 3: Execute actions
        results = []
        for action in actions:
            service = action["service"]
            action_name = action["action"]
            params = action.get("params", {})
            
            print(f"⚡ Executing: {service}.{action_name}")
            
            if service == "bigquery":
                result = handle_bigquery_request(action_name, params)
                results.append({"service": service, "action": action_name, "result": result})
            
            elif service == "gcs":
                result = handle_gcs_request(action_name, params)
                results.append({"service": service, "action": action_name, "result": result})
                
                # If we got documents, process them with RAG
                if action_name == "create_sample_documents" and result.get("success"):
                    print("📚 Processing documents with RAG...")
                    # Simulate document processing for RAG
                    sample_docs = [
                        {"name": "contracts/contract_001.txt", "content": "CONTRACT AGREEMENT\nParties: Company A & Vendor B\nValue: $50,000\nTerm: 12 months\nRisk Level: Medium"},
                        {"name": "reports/q4_2024_report.txt", "content": "Q4 2024 FINANCIAL REPORT\nRevenue: $1.2M\nExpenses: $800K\nProfit: $400K\nKey Metric: 15% growth"},
                        {"name": "policies/security_policy.txt", "content": "SECURITY POLICY DOCUMENT\nCompliance: ISO 27001\nLast Review: 2024-01-15\nStatus: Active"}
                    ]
                    rag_result = rag_agent.process_documents(sample_docs)
                    print(f"🧠 RAG processed {rag_result['processed_documents']} documents")
        
        # Step 4: Generate response
        response = self._generate_response(user_input, intent_analysis, results)
        
        # Log workflow
        workflow_entry = {
            "input": user_input,
            "intent": intent_analysis,
            "actions": actions,
            "results": results,
            "response": response
        }
        self.workflow_history.append(workflow_entry)
        
        return response
    
    def _generate_response(self, user_input, intent_analysis, results):
        """Generate human-readable response from results"""
        
        if "analyze" in user_input.lower() or "report" in user_input.lower():
            # Use RAG for analytical questions
            rag_response = rag_agent.answer_question(user_input)
            return {
                "type": "analysis",
                "input": user_input,
                "intent": intent_analysis,
                "rag_response": rag_response,
                "service_results": results,
                "summary": f"Analysis complete. Processed {len(results)} services."
            }
        else:
            # General response
            return {
                "type": "general",
                "input": user_input,
                "intent": intent_analysis,
                "service_results": results,
                "summary": f"Request processed successfully. Executed {len(results)} actions.",
                "next_steps": "You can ask me to analyze data, manage documents, or create reports."
            }
    
    def get_system_status(self):
        """Get system status - shows operational monitoring"""
        return {
            "status": "operational",
            "components": {
                "bigquery_mcp": "active",
                "gcs_mcp": "active", 
                "router_agent": "active",
                "rag_agent": "active"
            },
            "workflows_processed": len(self.workflow_history),
            "rag_knowledge": rag_agent.get_knowledge_summary()
        }

# Initialize the hub
hub = EnterpriseAutomationHub()

# Flask Routes
@app.route('/')
def home():
    """Main dashboard - shows enterprise UI capabilities"""
    return """
    <html>
        <head>
            <title>Enterprise RAG & Workflow Hub</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .card { background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 8px; }
                .success { color: green; }
                .error { color: red; }
            </style>
        </head>
        <body>
            <h1>🏢 Enterprise RAG & Workflow Automation Hub</h1>
            <div class="card">
                <h3>🚀 System Status: Operational</h3>
                <p>MCP Servers: BigQuery ✅, GCS ✅</p>
                <p>AI Agents: Router ✅, RAG ✅</p>
            </div>
            
            <div class="card">
                <h3>💬 Chat Interface</h3>
                <form action="/process" method="post">
                    <input type="text" name="query" style="width: 300px; padding: 10px;" 
                           placeholder="Ask me to analyze data, manage documents, or create reports...">
                    <button type="submit" style="padding: 10px 20px;">Send</button>
                </form>
            </div>
            
            <div class="card">
                <h3>🎯 Example Queries</h3>
                <ul>
                    <li>"Create sample data for demonstration"</li>
                    <li>"Show me my datasets in BigQuery"</li>
                    <li>"Analyze claims data and generate report"</li>
                    <li>"Upload sample documents to storage"</li>
                </ul>
            </div>
            
            <div class="card">
                <h3>🔧 System Controls</h3>
                <p><a href="/status">System Status</a> | <a href="/api/demo">Run Demo</a></p>
            </div>
        </body>
    </html>
    """

@app.route('/process', methods=['POST'])
def process_query():
    """Process user queries - main interaction endpoint"""
    user_input = request.form.get('query', '')
    
    if not user_input:
        return jsonify({"error": "No query provided"})
    
    try:
        result = hub.process_user_request(user_input)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/status')
def system_status():
    """System status endpoint - shows monitoring capabilities"""
    status = hub.get_system_status()
    return jsonify(status)

@app.route('/api/demo')
def run_demo():
    """Run a complete demo - showcases all capabilities"""
    demo_queries = [
        "Create sample data for demonstration",
        "Show me what documents are available",
        "Analyze claims data and generate report"
    ]
    
    demo_results = []
    for query in demo_queries:
        print(f"\n🎯 Running demo query: {query}")
        result = hub.process_user_request(query)
        demo_results.append({
            "query": query,
            "result": result
        })
    
    return jsonify({
        "demo": "complete",
        "results": demo_results,
        "system_status": hub.get_system_status()
    })

if __name__ == '__main__':
    print("\n🌐 Starting Flask server on http://localhost:8080")
    print("💡 Try these commands:")
    print("   - Create sample data for demonstration")
    print("   - Analyze claims data and generate report") 
    print("   - Show me my datasets in BigQuery")
    print("\n🚀 Server starting...")
    app.run(host='0.0.0.0', port=8080, debug=False)  # Set debug=False to avoid PIN prompt
