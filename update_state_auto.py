#!/usr/bin/env python3
"""
蛋蛋状态自动推送脚本 - 智能版
检测聊天活动自动更新状态
"""
import json
import os
from datetime import datetime, timedelta

def get_conversation_state():
    """检测最近聊天活动"""
    now = datetime.now()
    
    # 检查最近的消息文件
    # OpenClaw的消息通常记录在session相关文件
    recent_activity = False
    last_activity_time = None
    
    # 检查 /root/.openclaw 下的最近修改
    sessions_dir = "/root/.openclaw/sessions"
    if os.path.exists(sessions_dir):
        for f in os.listdir(sessions_dir):
            if f.endswith('.json'):
                filepath = os.path.join(sessions_dir, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if (now - mtime).total_seconds() < 60:  # 1分钟内修改过
                    recent_activity = True
                    last_activity_time = mtime
    
    # 判断状态
    if recent_activity or (now.hour >= 9 and now.hour <= 21):
        # 有活动或工作时间 -> 显示工作中
        return "researching", "思考/回复中"
    else:
        # 无活动 -> 待命
        return "idle", "待命中"

def main():
    state, detail = get_conversation_state()
    
    import urllib.request
    
    data = json.dumps({
        "state": state,
        "detail": detail
    }).encode('utf-8')
    
    req = urllib.request.Request(
        "http://127.0.0.1:19000/local-agent-update",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {state} - {detail}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
