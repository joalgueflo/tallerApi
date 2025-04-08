from flask import Flask, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/test-connection', methods=['GET'])
def test_connection():
    try:
        # Print connection details (don't expose the key in production)
        print(f"URL: {url}")
        print(f"Key exists: {bool(key)}")
        
        # Test a simple query
        response = supabase.table('peliculas').select('count').execute()
        return jsonify({"connection": "success", "response": response.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)