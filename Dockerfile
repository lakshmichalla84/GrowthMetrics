# Use Python 3.8 as the base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the application (modify based on your project)
CMD ["python", "app.py"]
