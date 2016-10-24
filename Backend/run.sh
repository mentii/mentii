#!/bin/bash
if [[ ! -d lib ]]; then
    pip install -r requirements.txt -t lib
fi
dev_appserver.py .
