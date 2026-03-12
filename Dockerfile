FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required for psycopg2 and other packages
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY backend/requirements.txt ./backend/requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the entire backend and root config to the container
COPY . .

# Install the app as an editable package to resolve the absolute imports
RUN pip install -e .

# Expose the port Railway expects
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
