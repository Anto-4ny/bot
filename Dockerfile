# ===========================
# Backend (Python)
# ===========================
FROM python:3.10 AS backend

WORKDIR /app

# Copy Python dependencies first
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY api.py /app/

# ===========================
# Frontend (Node.js)
# ===========================
FROM node:18 AS frontend

WORKDIR /app

# Copy package.json & package-lock.json first for caching
COPY package.json package-lock.json ./

# Fix: Set npm registry and install dependencies
RUN npm config set legacy-peer-deps true && npm cache clean --force
RUN npm install --force || npm install --legacy-peer-deps

# Copy frontend files
COPY . .

# ===========================
# Final Stage - Combine & Run
# ===========================
FROM python:3.10

WORKDIR /app

# Copy backend & frontend files
COPY --from=backend /app /app
COPY --from=frontend /app /app

# Install dependencies again for safety
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install Supervisor to manage both processes
RUN apt-get update && apt-get install -y supervisor

# Copy Supervisor configuration file
COPY supervisord.conf /etc/supervisord.conf

# Create log files & set permissions
RUN mkdir -p /var/log && touch /var/log/backend.out.log /var/log/backend.err.log \
    /var/log/frontend.out.log /var/log/frontend.err.log \
    && chmod 777 /var/log/*

# Expose backend (5000) & frontend (3000)
EXPOSE 3000 5000

# Start Supervisor to run both services
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
