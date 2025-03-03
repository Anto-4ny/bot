# ===========================
# Backend (Python)
# ===========================
FROM python:3.10 AS backend

WORKDIR /app

# Install system dependencies for Chrome & Selenium
RUN apt-get update && apt-get install -y wget curl unzip \
    libx11-xcb1 libxcomposite1 libxcursor1 libxi6 libxrandr2 libasound2 \
    libatk1.0-0 libgtk-3-0 libnss3 libdrm2 libgbm1 && \
    wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > /tmp/chrome.deb && \
    apt-get install -y /tmp/chrome.deb && \
    rm /tmp/chrome.deb

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

# Set npm registry and install dependencies
RUN npm config set legacy-peer-deps true && npm cache clean --force
RUN npm install --force || npm install --legacy-peer-deps

# Copy frontend files
COPY . .

# ===========================
# Final Stage - Combine & Run
# ===========================
FROM python:3.10 AS final

WORKDIR /app

# ✅ Copy backend & frontend from the correct build stages
COPY --from=backend /app /app
COPY --from=frontend /app /app

# Reinstall dependencies for safety
RUN pip install --no-cache-dir -r /app/requirements.txt

# ✅ Install Node.js in the final stage
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Install Supervisor to manage both processes
RUN apt-get install -y supervisor

# Copy Supervisor configuration file
COPY supervisord.conf /etc/supervisord.conf

# Create log files & set permissions
RUN mkdir -p /var/log && touch /var/log/backend.out.log /var/log/backend.err.log \
    /var/log/frontend.out.log /var/log/frontend.err.log \
    && chmod 777 /var/log/*

# Install Gunicorn for Flask backend
RUN pip install gunicorn

# Expose backend (5000) & frontend (3000)
EXPOSE 3000 5000

# Start Supervisor to run both services
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
