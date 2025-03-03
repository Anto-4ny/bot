# ===========================
# Backend (Python)
# ===========================
FROM python:3.10 AS backend

WORKDIR /app

# Copy Python files
COPY api.py requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

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
# Use a minimal image for the final container
FROM python:3.10

WORKDIR /app

# Copy files from previous builds
COPY --from=backend /app /app
COPY --from=frontend /app /app

# Install Supervisor to manage both processes
RUN apt-get update && apt-get install -y supervisor

# Create a Supervisor config file
RUN echo '[supervisord]\nnodaemon=true\n' > /etc/supervisord.conf && \
    echo '[program:backend]\ncommand=python3 /app/api.py\nautostart=true\nrestart=always\n' >> /etc/supervisord.conf && \
    echo '[program:frontend]\ncommand=node /app/server.js\nautostart=true\nrestart=always\n' >> /etc/supervisord.conf

# Expose backend (5000) & frontend (3000)
EXPOSE 3000 5000

# Start Supervisor to run both processes
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
