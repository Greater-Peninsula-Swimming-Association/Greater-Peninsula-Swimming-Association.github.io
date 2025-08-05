# Use an official, slim Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all the files from your local directory (the script and the source HTML)
# into the container's working directory
COPY . /app/

# Install the only Python dependency needed: BeautifulSoup
RUN pip install --no-cache-dir beautifulsoup4

# Set the entrypoint to execute the Python script
ENTRYPOINT ["python", "./generate_archive.py"]

# The arguments (input file and year) will be provided when you run the container.
