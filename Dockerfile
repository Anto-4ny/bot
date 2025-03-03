# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the application files
COPY api.py requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Python API
EXPOSE 5000

# Command to run the Python API
CMD ["python", "api.py"]
