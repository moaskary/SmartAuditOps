FROM node:18-alpine AS builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .

RUN npm run build

FROM nginx:1.25-alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY infrastructure/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]