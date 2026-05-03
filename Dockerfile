FROM nginx:stable-alpine

# Copy your website files into the container
RUN rm -rf /usr/share/nginx/html/*
COPY index.html /usr/share/nginx/html/
COPY sgustyle.css /usr/share/nginx/html/
COPY sguscript.js /usr/share/nginx/html/

# Optional images/assets
#COPY grenada.jpeg /usr/share/nginx/html/
COPY grenada-updated.jpeg /usr/share/nginx/html/

# Use to copy the entire folder
#COPY ./html /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy custom Nginx config (optional)
# COPY ./nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
