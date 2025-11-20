"""
GCS MCP Server - Handles cloud storage operations
Demonstrates file management and document storage capabilities
"""
from google.cloud import storage
import json
from configs.gcp_config import GCPConfig

class GCSMCPServer:
    def __init__(self):
        self.client = storage.Client(project=GCPConfig.PROJECT_ID)
        self.bucket_name = GCPConfig.BUCKET_NAME
        self._ensure_bucket_exists()
        print(f"✅ GCS MCP Server initialized. Bucket: {self.bucket_name}")
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist - shows infrastructure management"""
        try:
            bucket = self.client.bucket(self.bucket_name)
            if not bucket.exists():
                bucket = self.client.create_bucket(self.bucket_name, location="us")
                print(f"✅ Created new bucket: {self.bucket_name}")
            else:
                print(f"✅ Using existing bucket: {self.bucket_name}")
        except Exception as e:
            print(f"⚠️  Bucket setup: {str(e)}")
    
    def list_files(self, prefix=""):
        """List files in bucket - shows document discovery"""
        try:
            bucket = self.client.bucket(self.bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)
            
            files = []
            for blob in blobs:
                files.append({
                    "name": blob.name,
                    "size": blob.size,
                    "updated": blob.updated.isoformat() if blob.updated else None
                })
            
            print(f"📂 Found {len(files)} files in bucket")
            return {"success": True, "files": files}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def upload_file(self, file_name, content):
        """Upload file to GCS - shows document ingestion"""
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(file_name)
            
            blob.upload_from_string(content)
            
            print(f"✅ Uploaded file: {file_name}")
            return {"success": True, "message": f"File {file_name} uploaded successfully"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def download_file(self, file_name):
        """Download file from GCS - shows document retrieval"""
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(file_name)
            
            if not blob.exists():
                return {"success": False, "error": f"File {file_name} not found"}
            
            content = blob.download_as_text()
            print(f"✅ Downloaded file: {file_name} ({len(content)} chars)")
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_sample_documents(self):
        """Create sample documents for demonstration"""
        sample_docs = {
            "contracts/contract_001.txt": "CONTRACT AGREEMENT\nParties: Company A & Vendor B\nValue: $50,000\nTerm: 12 months\nRisk Level: Medium",
            "reports/q4_2024_report.txt": "Q4 2024 FINANCIAL REPORT\nRevenue: $1.2M\nExpenses: $800K\nProfit: $400K\nKey Metric: 15% growth",
            "policies/security_policy.txt": "SECURITY POLICY DOCUMENT\nCompliance: ISO 27001\nLast Review: 2024-01-15\nStatus: Active"
        }
        
        results = []
        for file_name, content in sample_docs.items():
            result = self.upload_file(file_name, content)
            results.append({"file": file_name, "success": result["success"]})
        
        return {"success": True, "uploaded_files": results}

def handle_gcs_request(method, params=None):
    """Handle GCS requests with proper parameter handling"""
    server = GCSMCPServer()
    
    # Ensure params is always a dictionary
    if params is None:
        params = {}
    
    if method == "list_files":
        return server.list_files(params.get("prefix", ""))
    elif method == "upload_file":
        return server.upload_file(params.get("file_name", ""), params.get("content", ""))
    elif method == "download_file":
        return server.download_file(params.get("file_name", ""))
    elif method == "create_sample_documents":
        return server.create_sample_documents()
    else:
        return {"success": False, "error": f"Unknown method: {method}"}

if __name__ == "__main__":
    # Test the server
    server = GCSMCPServer()
    print(server.list_files())
