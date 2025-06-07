FROM node:14-alpine

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to /app
COPY package*.json ./

# Install app dependencies
RUN npm install

# Bundle app source
COPY . .

# Expose the port dynamically based on the PORT environment variable
ENV PORT=3000
EXPOSE $PORT

# Define the command to run your app
CMD ["npm", "start"]