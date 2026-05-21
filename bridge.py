import socket
import threading
import sys
import os
import json
import time

# Default configuration blueprint
DEFAULT_CONFIG = {
    "vps_ip": "123.123.123.123",
    "control_port": 9000,
    "minecraft_port": 25565
}

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    else:
        with open("config.json", "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print("[!] Created config.json. Please configure your VPS IP inside it.")
        return DEFAULT_CONFIG

def pipe(src, dst):
    """Pipes raw bytes from one socket to another seamlessly"""
    try:
        while True:
            data = src.recv(8192)
            if not data:
                break
            dst.sendall(data)
    except Exception:
        pass
    finally:
        try:
            src.close()
        except Exception:
            pass
        try:
            dst.close()
        except Exception:
            pass

def run_server(c_port, m_port):
    print(f"=== VPS SERVER MODE INITIALIZED ===")
    print(f"[*] Public port for players: {m_port}")
    print(f"[*] Internal control port for Home PC: {c_port}")
    
    vps_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vps_control.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    vps_control.bind(('0.0.0.0', c_port))
    vps_control.listen(1)

    vps_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vps_game.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    vps_game.bind(('0.0.0.0', m_port))
    vps_game.listen(20)

    while True:
        print("\n[Listening] Waiting for Home PC to link up on port {}...".format(c_port))
        pc_conn, pc_addr = vps_control.accept()
        print(f"[Success] Home PC successfully bridged from IP: {pc_addr[0]}")

        while True:
            try:
                player_conn, player_addr = vps_game.accept()
                print(f"[Player Connection] Inbound user from {player_addr[0]}. Routing traffic to Home PC...")
                
                # Fire up the bidirectional bridge
                threading.Thread(target=pipe, args=(player_conn, pc_conn), daemon=True).start()
                threading.Thread(target=pipe, args=(pc_conn, player_conn), daemon=True).start()
                break # Break inner loop to reset the control bridge link for subsequent actions
            except Exception as e:
                print(f"[Connection Lost] Link broke down: {e}")
                break

def run_client(vps_ip, c_port, m_port):
    print(f"=== HOME PC CLIENT MODE INITIALIZED ===")
    print(f"[*] Targeted Remote VPS: {vps_ip}:{c_port}")
    print(f"[*] Bound Local Minecraft Instance: 127.0.0.1:{m_port}")
    
    while True:
        try:
            vps_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            vps_sock.connect((vps_ip, c_port))
            
            mc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mc_sock.connect(('127.0.0.1', m_port))
            
            t1 = threading.Thread(target=pipe, args=(vps_sock, mc_sock), daemon=True)
            t2 = threading.Thread(target=pipe, args=(mc_sock, vps_sock), daemon=True)
            t1.start()
            t2.start()
            
            t1.join()
            t2.join()
        except ConnectionRefusedError:
            print("[!] Connection refused. Ensure your Minecraft Server is running locally and the VPS script is active.")
            time.sleep(4)
        except Exception:
            time.sleep(4)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ['server', 'client']:
        print("Usage:")
        print("  python bridge.py server  - Run this syntax on your remote VPS")
        print("  python bridge.py client  - Run this syntax on your home gaming PC")
        sys.exit(1)

    mode = sys.argv[1]
    config = load_config()

    if mode == 'server':
        run_server(config["control_port"], config["minecraft_port"])
    elif mode == 'client':
        if config["vps_ip"] == "123.123.123.123":
            print("[!] Error: You must replace the template placeholder IP in config.json with your actual VPS IP address!")
            sys.exit(1)
        run_client(config["vps_ip"], config["control_port"], config["minecraft_port"])
