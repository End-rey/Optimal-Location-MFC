# Use an official Python runtime as the base image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies required by your Python script
# For example, if you have a requirements.txt file, uncomment the next line
RUN pip install pandas osmium

# Define the command to run your Python script
CMD ["python", "osm_ids_geocoding.py"]
