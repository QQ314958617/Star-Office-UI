#!/usr/bin/env python3
"""快速设置蛋蛋状态"""
import sys
import urllib.request
import json

state = sys.argv[1] if len(sys.argv) > 1 else "idle"
detail = sys.argv[2] if len(sys.argv) > 2 else "待命中"

data = json.dumps({"state": state, "detail": detail}).encode('utf-8')
req = urllib.request.Request(
    "http://127.0.0.1:19000/local-agent-update",
    data=data,
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=5) as response:
    print(json.loads(response.read().decode('utf-8')))
