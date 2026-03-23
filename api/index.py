import os
import sys

# Add the root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main app logic
# Note: Streamlit won't run fully as a serverless function, 
# but this provides the entry point Vercel expects.
try:
    from app import main
except ImportError:
    pass

def handler(event, context):
    return {
        "statusCode": 200,
        "body": "Face Recognition App is active. To view the full Streamlit UI, please ensure the project is correctly linked to a Streamlit-compatible host or use the experimental Vercel-Streamlit bridge."
    }
