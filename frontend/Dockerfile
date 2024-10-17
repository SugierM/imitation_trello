FROM node:20-alpine
# NOW IT IS FOR DEVELOPMENT
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173 5174

CMD ["npm", "run", "dev"]