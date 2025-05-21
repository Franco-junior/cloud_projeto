FROM python:3.11-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly install jose package
RUN pip install python-jose==3.4.0

# Copy the application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"] 