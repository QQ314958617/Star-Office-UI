#!/usr/bin/env python3
"""Update Star Office UI state (for testing or agent-driven sync).

For automatic state sync from OpenClaw: add a rule in your agent SOUL.md or AGENTS.md:
  Before starting a task: run `python3 set_state.py writing "doing XYZ"`.
  After finishing: run `python3 set_state.py idle "ready"`.
The office UI reads state from the same state.json this script writes.
"""

import json
import os
import sys
from datetime import datetime

STATE_FILE = os.environ.get(
    "STAR_OFFICE_STATE_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json"),
)

VALID_STATES = [
    "idle",
    "writing",
    "receiving",
    "replying",
    "researching",
    "executing",
    "syncing",
    "error"
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "state": "idle",
        "detail": "待命中...",
        "progress": 0,
        "updated_at": datetime.now().isoformat()
    }

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python set_state.py <state> [detail]")
        print(f"状态选项: {', '.join(VALID_STATES)}")
        print("\n例子:")
        print("  python set_state.py idle")
        print("  python set_state.py researching \"在查 Godot MCP...\"")
        print("  python set_state.py writing \"在写热点日报模板...\"")
        sys.exit(1)
    
    state_name = sys.argv[1]
    detail = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if state_name not in VALID_STATES:
        print(f"无效状态: {state_name}")
        print(f"有效选项: {', '.join(VALID_STATES)}")
        sys.exit(1)
    
    state = load_state()
    state["state"] = state_name
    state["detail"] = detail
    state["updated_at"] = datetime.now().isoformat()
    
    save_state(state)
    print(f"状态已更新: {state_name} - {detail}")

# Also update dandan agent in agents-state.json
def update_dandan_in_agents(state_name, detail):
    agents_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents-state.json")
    if os.path.exists(agents_file):
        with open(agents_file, 'r') as f:
            agents = json.load(f)
        for agent in agents:
            if agent.get("agentId") == "dandan":
                agent["state"] = state_name
                agent["detail"] = detail
                agent["updated_at"] = datetime.now().isoformat()
                agent["lastPushAt"] = datetime.now().isoformat()
        with open(agents_file, 'w') as f:
            json.dump(agents, f, ensure_ascii=False, indent=2)

# Call after saving main state
update_dandan_in_agents(state_name, detail)
