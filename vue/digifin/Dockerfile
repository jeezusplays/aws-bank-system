# Use the official Node.js 14 image as the base image
FROM node:16

# install simple http server for serving static content
RUN npm install -g http-server

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the project files to the working directory, excluding .env
COPY . ./
RUN rm -f .env

RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]