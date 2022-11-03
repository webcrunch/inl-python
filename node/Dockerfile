FROM node:18
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
WORKDIR /backend
COPY ./node/package.json ./
RUN npm install 
COPY /node /node 
CMD ["npm", "run", "start"]