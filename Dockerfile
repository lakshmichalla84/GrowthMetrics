# Use Python 3.8 as the base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the Flask app
 CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--log-level=debug", "--timeout", "0", "--preload", "your_app:app"]


    


