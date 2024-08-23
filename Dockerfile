# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install streamlit-option-menu

# Copy the project files into the container
COPY Database /app/Database
COPY resources /app/resources
COPY utils /app/utils
COPY views /app/views

# COPY .env /app/.env
COPY app.py /app/app.py
COPY isrgrootx1.pem /app/isrgrootx1.pem

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]
