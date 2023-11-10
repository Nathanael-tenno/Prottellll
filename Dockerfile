# Start with a base image containing Java runtime (for Node.js)
FROM node:16-slim

# The application's port (if it's different, change it)
EXPOSE 5000

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Node.js application files
COPY server.js .
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Install Python and the Python dependencies
# Python is not included in the Node image, so we need to install it
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Copy the Python script and requirements.txt into the container
COPY app.py .
COPY requirements.txt .

# Install any needed Python packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the Node.js application on container startup
CMD [ "node", "server.js" ]