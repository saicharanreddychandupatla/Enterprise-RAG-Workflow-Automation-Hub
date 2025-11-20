"""
RAG Agent - Retrieval Augmented Generation for document intelligence
This demonstrates advanced AI capabilities with enterprise data
"""
import json
import re

class RAGAgent:
    def __init__(self):
        self.knowledge_base = {}
        print("✅ RAG Agent initialized")
    
    def process_documents(self, documents):
        """Process documents and build knowledge base - shows AI understanding"""
        print(f"📄 Processing {len(documents)} documents for RAG")
        
        for doc in documents:
            if doc.get("success") and doc.get("content"):
                content = doc["content"]
                self._extract_knowledge(doc.get("name", "unknown"), content)
        
        return {"success": True, "processed_documents": len(documents)}
    
    def _extract_knowledge(self, doc_name, content):
        """Extract structured knowledge from documents"""
        # Simple pattern matching for demonstration
        # In production, you'd use Vertex AI embeddings
        
        patterns = {
            "contracts": {
                "amount": r"\$([0-9,]+)",
                "parties": r"Parties:\s*(.+)",
                "term": r"Term:\s*([0-9]+\s*(months|years))",
                "risk": r"Risk Level:\s*(\w+)"
            },
            "reports": {
                "revenue": r"Revenue:\s*\$?([0-9,.]+[MK]?)",
                "profit": r"Profit:\s*\$?([0-9,.]+[MK]?)",
                "growth": r"growth.*?([0-9]+)%"
            }
        }
        
        doc_type = "general"
        if "contract" in doc_name.lower():
            doc_type = "contracts"
        elif "report" in doc_name.lower():
            doc_type = "reports"
        
        extracted_data = {"type": doc_type, "entities": {}}
        
        if doc_type in patterns:
            for entity, pattern in patterns[doc_type].items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    extracted_data["entities"][entity] = matches[0] if isinstance(matches[0], tuple) else matches
        
        self.knowledge_base[doc_name] = extracted_data
        print(f"🧠 Extracted knowledge from {doc_name}: {len(extracted_data['entities'])} entities")
    
    def answer_question(self, question, context_docs=None):
        """Answer questions using retrieved knowledge - shows AI reasoning"""
        print(f"❓ Answering question: {question}")
        
        # Simple Q&A logic for demonstration
        # In production, you'd use Vertex AI Gemini
        
        question_lower = question.lower()
        answer = "I've analyzed the available information. "
        
        if any(word in question_lower for word in ["contract", "agreement"]):
            contract_data = self.knowledge_base.get("contracts/contract_001.txt", {})
            if contract_data.get("entities"):
                entities = contract_data["entities"]
                answer += f"Based on the contract: Value: {entities.get('amount', ['Unknown'])[0]}, "
                answer += f"Parties: {entities.get('parties', ['Unknown'])[0]}, "
                answer += f"Risk Level: {entities.get('risk', ['Unknown'])[0]}"
            else:
                answer += "I found contract documents but need more specific information."
        
        elif any(word in question_lower for word in ["report", "revenue", "profit"]):
            report_data = self.knowledge_base.get("reports/q4_2024_report.txt", {})
            if report_data.get("entities"):
                entities = report_data["entities"]
                answer += f"Based on the financial report: Revenue: ${entities.get('revenue', ['Unknown'])[0]}, "
                answer += f"Profit: ${entities.get('profit', ['Unknown'])[0]}, "
                answer += f"Growth: {entities.get('growth', ['Unknown'])[0]}%"
            else:
                answer += "I found financial reports but need more specific information."
        
        elif any(word in question_lower for word in ["risk", "compliance"]):
            policy_data = self.knowledge_base.get("policies/security_policy.txt", {})
            answer += "Based on security policies, the organization follows ISO 27001 compliance standards."
        
        else:
            answer += "I can help you analyze contracts, financial reports, and security policies. Please ask specific questions about these documents."
        
        return {
            "success": True,
            "question": question,
            "answer": answer,
            "sources_used": list(self.knowledge_base.keys())[:3]  # Show top 3 sources
        }
    
    def get_knowledge_summary(self):
        """Get summary of current knowledge - shows AI's understanding"""
        summary = {
            "total_documents": len(self.knowledge_base),
            "document_types": {},
            "key_entities": []
        }
        
        for doc_name, data in self.knowledge_base.items():
            doc_type = data.get("type", "unknown")
            if doc_type not in summary["document_types"]:
                summary["document_types"][doc_type] = 0
            summary["document_types"][doc_type] += 1
            
            for entity, value in data.get("entities", {}).items():
                summary["key_entities"].append(f"{entity}: {value}")
        
        return summary

if __name__ == "__main__":
    rag = RAGAgent()
    print("🧠 RAG Agent Demo Ready")
