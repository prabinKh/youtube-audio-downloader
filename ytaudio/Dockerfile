# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (change if necessary for your app)
EXPOSE 8000

# Command to run the application (change if needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
