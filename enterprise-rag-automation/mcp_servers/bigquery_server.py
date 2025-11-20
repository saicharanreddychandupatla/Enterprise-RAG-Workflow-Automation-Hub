"""
BigQuery MCP Server - Handles all BigQuery operations
This demonstrates real enterprise data warehouse integration
"""
from google.cloud import bigquery
import json
from configs.gcp_config import GCPConfig

class BigQueryMCPServer:
    def __init__(self):
        # BigQuery client automatically uses Cloud Shell credentials
        self.client = bigquery.Client(project=GCPConfig.PROJECT_ID)
        print(f"✅ BigQuery MCP Server initialized for project: {GCPConfig.PROJECT_ID}")
    
    def run_query(self, sql):
        """Execute SQL query - showcases data analysis capabilities"""
        try:
            print(f"📊 Executing query: {sql}")
            query_job = self.client.query(sql)
            results = []
            
            for row in query_job:
                results.append(dict(row))
            
            print(f"✅ Query returned {len(results)} rows")
            return {"success": True, "data": results, "row_count": len(results)}
            
        except Exception as e:
            error_msg = f"❌ Query failed: {str(e)}"
            print(error_msg)
            return {"success": False, "error": error_msg}
    
    def list_datasets(self):
        """List all datasets in the project - shows data discovery"""
        try:
            datasets = list(self.client.list_datasets())
            dataset_names = [dataset.dataset_id for dataset in datasets]
            print(f"📁 Found {len(dataset_names)} datasets")
            return {"success": True, "datasets": dataset_names}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_sample_table(self):
        """Create a sample table for demonstration - shows schema management"""
        try:
            dataset_ref = f"{GCPConfig.PROJECT_ID}.{GCPConfig.DATASET_ID}"
            
            # Create dataset if it doesn't exist
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            self.client.create_dataset(dataset, exists_ok=True)
            print(f"✅ Dataset {GCPConfig.DATASET_ID} ready")
            
            # Create sample table
            table_id = f"{dataset_ref}.sample_claims"
            schema = [
                bigquery.SchemaField("claim_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("amount", "FLOAT", mode="REQUIRED"),
                bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("date_submitted", "DATE", mode="REQUIRED"),
            ]
            
            table = bigquery.Table(table_id, schema=schema)
            self.client.create_table(table, exists_ok=True)
            print(f"✅ Table sample_claims created")
            
            # Insert sample data
            rows_to_insert = [
                {"claim_id": "CLM001", "amount": 1500.0, "status": "APPROVED", "customer_id": "CUST001", "date_submitted": "2024-01-15"},
                {"claim_id": "CLM002", "amount": 2750.0, "status": "PENDING", "customer_id": "CUST002", "date_submitted": "2024-01-16"},
                {"claim_id": "CLM003", "amount": 500.0, "status": "REJECTED", "customer_id": "CUST001", "date_submitted": "2024-01-17"},
            ]
            
            errors = self.client.insert_rows_json(table_id, rows_to_insert)
            if errors:
                print(f"❌ Error inserting data: {errors}")
                return {"success": False, "error": str(errors)}
            
            print("✅ Sample table created with demo data")
            return {"success": True, "message": "Sample table created successfully"}
            
        except Exception as e:
            print(f"❌ Error creating sample table: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_claim_analytics(self):
        """Get analytics on claims data - shows business intelligence capabilities"""
        # First ensure the table exists
        self.create_sample_table()
        
        query = f"""
        SELECT 
            status,
            COUNT(*) as claim_count,
            AVG(amount) as avg_amount,
            SUM(amount) as total_amount
        FROM `{GCPConfig.PROJECT_ID}.{GCPConfig.DATASET_ID}.sample_claims`
        GROUP BY status
        """
        return self.run_query(query)

def handle_bigquery_request(method, params=None):
    """Handle BigQuery requests with proper parameter handling"""
    server = BigQueryMCPServer()
    
    # Ensure params is always a dictionary
    if params is None:
        params = {}
    
    if method == "run_query":
        return server.run_query(params.get("sql", "SELECT 1"))
    elif method == "list_datasets":
        return server.list_datasets()
    elif method == "create_sample_table":
        return server.create_sample_table()
    elif method == "get_claim_analytics":
        return server.get_claim_analytics()
    else:
        return {"success": False, "error": f"Unknown method: {method}"}

if __name__ == "__main__":
    # Test the server
    server = BigQueryMCPServer()
    print(server.list_datasets())
