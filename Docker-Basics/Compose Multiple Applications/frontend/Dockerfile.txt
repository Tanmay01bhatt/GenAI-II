FROM node:12-alpine AS base

WORKDIR /app
COPY package*.json yarn.lock ./

RUN NODE_ENV=dev yarn 
COPY . /app

CMD ["yarn", "serve"]

FROM base as build
RUN yarn build

# Make final image
FROM nginx:1.13.12-alpine as production

WORKDIR /app
COPY package*.json ./
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]