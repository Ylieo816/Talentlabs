FROM node:18-alpine

WORKDIR /app

# copy package.json and package-lock.json
COPY package*.json ./

# install dependencies
RUN npm install

# copy the rest of the project
COPY . .

# expose port
EXPOSE 3000

# run the app
CMD ["npm", "start"] 