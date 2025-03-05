# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run (Cloud Run expects the service to listen on $PORT, default 8080)
ENV PORT 8080

# Set environment variable for Flask
ENV FLASK_APP main.py

# Run the Flask app. Note: Cloud Run will pass the PORT environment variable.
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
