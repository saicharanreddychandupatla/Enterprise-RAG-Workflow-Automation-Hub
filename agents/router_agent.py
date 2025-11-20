"""
Router Agent - Intelligently routes requests to appropriate services
This demonstrates multi-agent orchestration and intent recognition
"""
import json
import re

class RouterAgent:
    def __init__(self):
        self.patterns = {
            "bigquery": [
                r"query", r"select", r"analyze", r"data", r"table", r"dataset",
                r"claims", r"fraud", r"report", r"analytics", r"sample", r"demo"
            ],
            "gcs": [
                r"file", r"document", r"upload", r"download", r"storage",
                r"contract", r"report", r"pdf", r"retrieve", r"sample", r"demo"
            ],
            "workflow": [
                r"send", r"email", r"notify", r"workflow", r"automate",
                r"pipeline", r"process"
            ]
        }
        print("✅ Router Agent initialized")
    
    def analyze_intent(self, user_input):
        """Analyze user input to determine intent and required services"""
        user_input_lower = user_input.lower()
        
        # Determine required services
        required_services = []
        for service, patterns in self.patterns.items():
            if any(re.search(pattern, user_input_lower) for pattern in patterns):
                required_services.append(service)
        
        # Determine primary intent
        if any(word in user_input_lower for word in ["query", "select", "analyze", "report"]):
            primary_intent = "data_analysis"
        elif any(word in user_input_lower for word in ["file", "document", "upload", "storage"]):
            primary_intent = "document_management"
        elif any(word in user_input_lower for word in ["send", "email", "workflow"]):
            primary_intent = "workflow_automation"
        else:
            primary_intent = "general_query"
        
        # Generate reasoning
        reasoning = self._generate_reasoning(user_input, required_services, primary_intent)
        
        return {
            "primary_intent": primary_intent,
            "required_services": required_services,
            "reasoning": reasoning,
            "confidence": "high" if required_services else "medium"
        }
    
    def _generate_reasoning(self, user_input, services, intent):
        """Generate human-readable reasoning for routing decision"""
        service_names = ", ".join(services) if services else "general processing"
        
        reasoning_map = {
            "data_analysis": f"User wants to analyze data using {service_names}",
            "document_management": f"User wants to manage documents using {service_names}",
            "workflow_automation": f"User wants to automate workflows using {service_names}",
            "general_query": f"User has a general query that may require {service_names}"
        }
        
        return reasoning_map.get(intent, "Processing user request")
    
    def route_to_services(self, user_input, intent_analysis):
        """Route the request to appropriate services based on analysis"""
        actions = []
        user_input_lower = user_input.lower()
        
        if "bigquery" in intent_analysis["required_services"]:
            if "sample" in user_input_lower or "demo" in user_input_lower:
                actions.append({"service": "bigquery", "action": "create_sample_table", "params": {}})
            elif "analyze" in user_input_lower or "report" in user_input_lower:
                actions.append({"service": "bigquery", "action": "get_claim_analytics", "params": {}})
            elif "list" in user_input_lower or "show" in user_input_lower:
                actions.append({"service": "bigquery", "action": "list_datasets", "params": {}})
            else:
                actions.append({"service": "bigquery", "action": "list_datasets", "params": {}})
        
        if "gcs" in intent_analysis["required_services"]:
            if "sample" in user_input_lower or "demo" in user_input_lower:
                actions.append({"service": "gcs", "action": "create_sample_documents", "params": {}})
            elif "list" in user_input_lower or "show" in user_input_lower:
                actions.append({"service": "gcs", "action": "list_files", "params": {}})
            else:
                actions.append({"service": "gcs", "action": "list_files", "params": {}})
        
        return actions

# Example usage
if __name__ == "__main__":
    router = RouterAgent()
    
    test_queries = [
        "Show me my datasets in BigQuery",
        "Upload a contract document to storage",
        "Analyze claims data and generate report",
        "Create sample data for demonstration"
    ]
    
    for query in test_queries:
        print(f"\n🧠 Query: '{query}'")
        analysis = router.analyze_intent(query)
        actions = router.route_to_services(query, analysis)
        print(f"📡 Routing: {analysis}")
        print(f"🎯 Actions: {actions}")
