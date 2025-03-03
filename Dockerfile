# Use Python for backend
FROM python:3.10 AS backend

WORKDIR /app

# Copy Python dependencies
COPY api.py requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Use Node.js for frontend
FROM node:18 AS frontend

WORKDIR /app

# Ensure package.json is copied first to improve caching
COPY package.json package-lock.json ./

# Fix: Set npm registry and permissions before install
RUN npm config set legacy-peer-deps true && npm cache clean --force

# Fix: Use alternative npm install to avoid failures
RUN npm install --force || npm install --legacy-peer-deps

# Copy all files (views, public, etc.)
COPY . .

# Expose backend (5000) & frontend (3000)
EXPOSE 3000 5000

# Start both services
CMD ["sh", "-c", "python api.py & node server.js"]
