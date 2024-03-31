# Use the official Python slim 3.10 image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all the files from the current directory to the working directory inside the container
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the setup.py file
CMD ["python", "setup.py"]