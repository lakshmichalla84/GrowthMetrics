cat Dockerfile
# Use Python 3.8 as the base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy project files to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
