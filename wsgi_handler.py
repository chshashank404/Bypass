import serverless_wsgi
from app import app  # Assuming your Flask app is defined in app.py

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
