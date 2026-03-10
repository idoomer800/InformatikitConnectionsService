FROM nginx:latest

# Install stuff
RUN apt-get update && \
    apt-get install -y acl apache2-utils && \
    rm -rf /var/lib/apt/lists/*

# Create directories for DB network files
# Create directories for DB network files
RUN mkdir -p /oracle/network/admin && \
    mkdir -p /odbc && \
    echo "OK" > /health.txt

# Create the user during the build
RUN htpasswd -bc /etc/nginx/.htpasswd informatikit password

# Copy your specific configuration
# Note: Ensure your local nginx.conf has the 'http' and 'events' blocks!
COPY nginx.conf /etc/nginx/nginx.conf
COPY tnsnames.ora /oracle/network/admin/tnsnames.ora
COPY odbc.ini /odbc/odbc.ini

# Setup write permissions AND ownership for nginx user
RUN chown -R nginx:nginx /oracle/network/admin && \
    chown -R nginx:nginx /odbc && \
    setfacl -R -m u:nginx:rwx /oracle/network/admin && \
    setfacl -dR -m u:nginx:rwx /oracle/network/admin && \
    setfacl -R -m u:nginx:rwx /odbc && \
    setfacl -dR -m u:nginx:rwx /odbc

# Add a health check
# This tells Docker to check if Nginx is alive every 30 seconds
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f -u informatikit:password http://localhost/health.txt || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]