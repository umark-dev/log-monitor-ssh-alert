#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# ------------------------
# Colors for output
# ------------------------
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# ------------------------
# Check virtual environment
# ------------------------
if [ -d "venv" ]; then
    echo -e "${GREEN}[INFO] Activating Python virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}[WARN] No virtual environment found. Running with system Python...${NC}"
fi

# ------------------------
# Ensure required folders exist
# ------------------------
if [ ! -d "logs" ]; then
    echo -e "${GREEN}[INFO] Creating logs/ directory...${NC}"
    mkdir logs
fi

# ------------------------
# Check Python dependencies
# ------------------------
echo -e "${GREEN}[INFO] Installing required Python packages...${NC}"
pip install -r requirements.txt

# ------------------------
# Start the monitoring tool
# ------------------------
echo -e "${GREEN}[INFO] Starting Log Monitoring Tool...${NC}"
python3 src/monitor.py
