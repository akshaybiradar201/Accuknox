# Use a slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project code
COPY . .

# Expose port for Django app (usually 8000)
EXPOSE 8003

# Set command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]
