FROM python:3.9-slim

# Set environment variables
ENV SSH_PASSWD=root:Docker!
##ARG SSH_PASSWD
##while building docker image:
##docker build --build-arg SSH_PASSWD=root:Docker! --platform linux/amd64 --tag appsvc-keyvaultaccesstoken-custom-image .

##via terminal how to build, tag, and push in Azure Container Registry:
##docker build --platform linux/amd64 --tag appsvc-keyvaultaccesstoken-custom-image .
##docker tag appsvc-keyvaultaccesstoken-custom-image containerregistryfc01.azurecr.io/appsvc-keyvaultaccesstoken-custom-image:latest
##docker push containerregistryfc01.azurecr.io/appsvc-keyvaultaccesstoken-custom-image:latest

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Install SSH server and other required packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "$SSH_PASSWD" | chpasswd

##RUN others
RUN apt-get update \
    && apt-get install -y curl
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
RUN apt-get update 

# Copy SSH configuration and init script
COPY sshd_config /etc/ssh/sshd_config
COPY init.sh /usr/local/bin/init.sh
RUN chmod u+x /usr/local/bin/init.sh

# Expose ports for Flask and SSH
EXPOSE 8000 2222

# Set entrypoint to init script
ENTRYPOINT ["/usr/local/bin/init.sh"]
