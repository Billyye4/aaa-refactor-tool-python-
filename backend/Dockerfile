# 1. Use a lightweight version of Python
FROM python:3.11-slim

# 2. Create a folder inside the container
WORKDIR /app

# 3. Copy only the requirements first (for caching speed)
COPY requirements.txt .

# 4. Install dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the backend code
COPY . .

# 6. Tell Docker we need port 8000
EXPOSE 8000

# 7. The command to run when the container starts
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]