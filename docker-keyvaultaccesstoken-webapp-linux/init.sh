#!/bin/bash
set -e

# Start SSH service
/usr/sbin/sshd
echo "Starting SSH ..."
service ssh start

# Start Flask app
python3 /app/app.py
