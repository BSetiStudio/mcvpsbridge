# ⛏️ Easy Minecraft VPS Tunnel

A lightweight, clean Python script designed to establish an automatic reverse TCP tunnel. It allows you to host a Minecraft server right on your domestic computer behind a **Strict Private IP/Carrier-Grade NAT (CGNAT)** by using your own remote VPS as a public gateway.

### Why use this?
* **Zero Dependencies:** Uses only standard built-in Python libraries. No `pip install` required.
* **Coexists Safely:** Does not interfere with existing software like 3x-ui, Xray, or web servers running on your VPS.
* **Completely Free:** No reliance on third-party limitations (like Ngrok or Playit.gg premium tiers).

---

## 🚀 Quick Start Guide

### 1. Remote VPS Setup (Server-side)
curl -sL [https://raw.githubusercontent.com/BSetiStudio/mcvpsbridge/main/bridge.py](https://raw.githubusercontent.com/BSetiStudio/mcvpsbridge/main/bridge.py) -o bridge.py

Launch the server routing component:

python3 bridge.py server
(Make sure ports 25565 and 9000 are allowed through your VPS firewall/UFW rules).

### 2. Domestic Machine Setup (Client-side)
Download this exact bridge.py file to your local computer running the Minecraft server.

Open your terminal/command prompt in that directory and initialize the client configuration setup:

python bridge.py client

3. The script will generate a template `config.json` file. Open it up and update the `"vps_ip"` field, replacing `123.123.123.123` with your actual VPS public IP address.

4. Execute the command once more:
python bridge.py client
   
That's it! Launch your local Minecraft server instance. Your friends can now connect seamlessly using your VPS's public IP address as the server address!
