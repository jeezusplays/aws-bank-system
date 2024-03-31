# Use an official Node runtime as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in package.json
RUN yarn install

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Serve the app
CMD ["yarn", "serve"]
