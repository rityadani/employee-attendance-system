FROM nginx:alpine

COPY advanced_christmas_dashboard.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]