# Use Python for backend
FROM python:3.10 AS backend

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY api.py requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Use Node.js for frontend
FROM node:18 AS frontend

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy all files (including views, public, etc.)
COPY . .

# Expose ports for both services
EXPOSE 3000 5000

# Start both services
CMD ["sh", "-c", "python api.py & node server.js"]
