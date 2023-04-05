FROM registry.cn-shenzhen.aliyuncs.com/gindowcloud/node as build
WORKDIR /data
COPY . .
RUN yarn config set registry https://registry.npm.taobao.org
RUN yarn config get registry
RUN yarn && yarn build

FROM registry.cn-shenzhen.aliyuncs.com/gindowcloud/nginx
COPY --from=build /data/dist /data/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80