"""
GCP Configuration - This sets up authentication and project settings
We use Application Default Credentials which work automatically in Cloud Shell
"""
import os

class GCPConfig:
    # GCP Project ID - Cloud Shell automatically sets this
    PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id')
    
    # BigQuery settings
    DATASET_ID = "enterprise_rag"
    
    # GCS settings
    BUCKET_NAME = f"{PROJECT_ID}-rag-documents"
    
    # Vertex AI settings (we'll use Gemini API)
    VERTEX_AI_LOCATION = "us-central1"

# Service account keys for different services
SERVICE_ACCOUNTS = {
    "bigquery": "bigquery_service_account.json",
    "gcs": "storage_service_account.json",
    "gmail": "gmail_service_account.json"
}
