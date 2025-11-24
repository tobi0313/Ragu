# Use the official OWASP ZAP image (contains ZAP and Java)
FROM owasp/zap2docker-stable:latest

# Switch to root so we can install python
USER root

# Install Python3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Create app dir
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy scripts
COPY run_zap_scan.sh /app/run_zap_scan.sh
COPY zap_scan.py /app/zap_scan.py

# Make sure the wrapper is executable
RUN chmod +x /app/run_zap_scan.sh

# Optional: expose the ZAP API port (daemon will run on 8090 in the script)
EXPOSE 8090

# Default entrypoint will start ZAP (daemon) and run the python scanner
ENTRYPOINT ["/app/run_zap_scan.sh"]