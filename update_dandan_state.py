#!/usr/bin/env python3
"""
更新蛋蛋在Star Office UI中的状态
"""
import json
import os
from datetime import datetime

STATE_FILE = "/root/Star-Office-UI/agents-state.json"

def update_dandan_state(state="idle", detail="待命分析市场"):
    """更新蛋蛋状态"""
    if not os.path.exists(STATE_FILE):
        print(f"State file not found: {STATE_FILE}")
        return False
    
    with open(STATE_FILE, 'r') as f:
        agents = json.load(f)
    
    now = datetime.now().isoformat()
    updated = False
    
    for agent in agents:
        if agent.get("agentId") == "dandan":
            agent["state"] = state
            agent["detail"] = detail
            agent["updated_at"] = now
            agent["lastPushAt"] = now
            agent["authStatus"] = "approved"
            updated = True
    
    if updated:
        with open(STATE_FILE, 'w') as f:
            json.dump(agents, f, ensure_ascii=False, indent=2)
        print(f"Updated dandan state at {now}")
        return True
    else:
        print("Dandan agent not found")
        return False

if __name__ == "__main__":
    import sys
    state = sys.argv[1] if len(sys.argv) > 1 else "idle"
    detail = sys.argv[2] if len(sys.argv) > 2 else "待命"
    update_dandan_state(state, detail)
