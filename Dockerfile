FROM python:3.10-slim

# prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

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

# Expose the port FastAPI runs on
EXPOSE 9000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000", "--reload", "--timeout-keep-alive", "300"]
