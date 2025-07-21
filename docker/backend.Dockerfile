FROM python:3.11-slim

# Set build arguments for pip configuration
ARG PIP_TIMEOUT=300
ARG PIP_RETRIES=10

# Set working directory
WORKDIR /app

# Install system dependencies first (this layer rarely changes)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
# This layer will be cached unless requirements.txt changes
COPY requirements.txt .

# Install Python dependencies with caching
# Use pip cache for faster subsequent builds
RUN pip install --progress-bar on --timeout ${PIP_TIMEOUT} --retries ${PIP_RETRIES} -r requirements.txt

# Copy only essential application files (exclude large directories)
COPY db/ ./db/
COPY modules/ ./modules/
COPY scan_history/ ./scan_history/
COPY app.py .
COPY scan.py .
COPY start_backend.sh .



# Create necessary directories
RUN mkdir -p backend/scan_history

# Install git and git-lfs for model downloading (models will be downloaded at runtime if needed)
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Copy startup script
COPY start_backend.sh /app/start_backend.sh
RUN chmod +x /app/start_backend.sh

# Run the application
CMD ["/app/start_backend.sh"]