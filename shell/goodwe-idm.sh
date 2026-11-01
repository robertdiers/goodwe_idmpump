#!/bin/bash
# random wait between 1 and 10 seconds after the cron trigger
sleep $((RANDOM % 10 + 1))
cd /app/python
python3 goodwe-idm.py