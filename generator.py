import os
import re
import sys

def build(cmd, port, mem):
    print(f"[*] 正在分析指令: {cmd}")
    
    # 1. 自动补全骨架
    ref_files = re.findall(r"([^\s/]+\.(?:properties|yml|yaml|json|conf|txt|js|py|sh))", cmd)
    os.makedirs("output", exist_ok=True)
    for f in set(ref_files):
        with open(f"output/{f}", "w") as fout:
            fout.write("eula=true\nstatus=online\n")
    
    # 2. 生成主影子入口
    is_java = "java" in cmd.lower()
    target = re.search(r"-jar\s+([^\s]+)", cmd).group(1) if is_java else "index.js"
    
    payload = f"""#!/bin/bash
# NK Shadow Engine
echo "[$(date '+%H:%M:%S')] [Server thread/INFO]: Starting Mock Engine..."
python3 -c "
import socket, time, threading, os
def listen():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', {port}))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            conn.close()
    except: pass
dummy_mem = ' ' * ({mem} * 1024 * 1024)
threading.Thread(target=listen, daemon=True).start()
while True:
    time.sleep(os.urandom(1)[0] % 60 + 20)
    print(f'[{{time.strftime(\"%H:%M:%S\")}}] [Server thread/INFO]: Saved chunks for level \"world\"')
"
"""
    with open(f"output/{target}", "w") as f:
        f.write(payload)
    os.chmod(f"output/{target}", 0o755)
    print(f"[OK] 已生成影子环境至 output 目录")

if __name__ == "__main__":
    # 从工作流参数读取输入
    build(sys.argv[1], sys.argv[2], sys.argv[3])
