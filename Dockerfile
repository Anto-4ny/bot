# ===========================
# Backend (Python)
# ===========================
FROM python:3.10 AS backend

WORKDIR /app

# Copy Python files first
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend files
COPY api.py /app/

# ===========================
# Frontend (Node.js)
# ===========================
FROM node:18 AS frontend

WORKDIR /app

# Copy package.json & package-lock.json first for caching
COPY package.json package-lock.json ./

# Set npm registry and install dependencies
RUN npm config set legacy-peer-deps true && npm cache clean --force
RUN npm install --force || npm install --legacy-peer-deps

# Copy the rest of the frontend files
COPY . .

# ===========================
# Final Stage - Run Both
# ===========================
# Use a minimal Python image for the final container
FROM python:3.10

WORKDIR /app

# Copy backend and frontend files from previous builds
COPY --from=backend /app /app
COPY --from=frontend /app /app

# Install Supervisor to manage both processes
RUN apt-get update && apt-get install -y supervisor

# Create Supervisor config file correctly
RUN echo '[supervisord]' > /etc/supervisord.conf && \
    echo 'nodaemon=true' >> /etc/supervisord.conf && \
    echo '[program:backend]' >> /etc/supervisord.conf && \
    echo 'command=python3 /app/api.py' >> /etc/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisord.conf && \
    echo 'stderr_logfile=/var/log/backend.err.log' >> /etc/supervisord.conf && \
    echo 'stdout_logfile=/var/log/backend.out.log' >> /etc/supervisord.conf && \
    echo '[program:frontend]' >> /etc/supervisord.conf && \
    echo 'command=node /app/server.js' >> /etc/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisord.conf && \
    echo 'stderr_logfile=/var/log/frontend.err.log' >> /etc/supervisord.conf && \
    echo 'stdout_logfile=/var/log/frontend.out.log' >> /etc/supervisord.conf

# Expose backend (5000) & frontend (3000)
EXPOSE 3000 5000

# Start Supervisor to run both services
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
