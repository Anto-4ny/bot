# ===========================
# Final Stage - Combine & Run
# ===========================
FROM python:3.10

WORKDIR /app

# Copy backend & frontend files
COPY --from=backend /app /app
COPY --from=frontend /app /app

# Install required dependencies again
RUN pip install --no-cache-dir -r /app/requirements.txt

# ✅ Install Node.js and npm manually in the final stage
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
