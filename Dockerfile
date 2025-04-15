# # Use an official Python runtime as a parent image
# FROM python:3.9

# # Set the working directory
# WORKDIR /usr/src/app

# # Copy requirements.txt
# COPY requirements.txt ./

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# # Expose the port your app runs on (if applicable)
# EXPOSE 8000

# # Define the command to run the app
# CMD ["python", "workflow_parallelExecution.py"]


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py","worker"]
