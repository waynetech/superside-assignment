FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional development tools
RUN pip install --no-cache-dir uvicorn watchdog

# Copy the rest of the application
COPY . .

# Set environment variable for development
ENV FASTAPI_ENV=development

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application with auto-reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
