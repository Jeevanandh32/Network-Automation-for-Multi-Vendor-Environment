# Multi-Vendor Network Automation with Paramiko, Netmiko, NAPALM, and Ansible
![image](https://github.com/user-attachments/assets/faf267a8-33b4-4a6f-b246-3d72391dcf4b)


## 🔧 Tools Overview

### 🔹 Paramiko – Low-level SSH automation
**How it works:**
- Uses Python to establish a raw SSH connection (`SSHClient()`)
- Opens a shell session (`invoke_shell()`)
- Sends commands as if you’re typing them manually, line by line
- Requires manual timing (e.g., `time.sleep`) and careful prompt handling

**Why use it:**
- Full control of SSH, useful when:
  - Devices don’t support Netmiko/NAPALM
  - You need to emulate real user input
  - Automating Linux systems or non-network devices

**Deep insight:**
- Paramiko is like remote-controlling a terminal.
- Doesn’t parse output — you must know exactly what the device will return.
- No abstraction. You manually handle prompts, delays, and formatting.

### 🔹 Netmiko – Network CLI automation
**How it works:**
- Built on top of Paramiko
- Adds device-type support (`cisco_ios`, `juniper`, etc.)
- Handles login, enable mode, config mode, command prompts automatically
- Provides `send_command()` and `send_config_set()` helpers

**Why use it:**
- Automate CLI-based network devices safely and quickly
- Reliable command execution without writing timing logic
- Ideal for one-time setups or scripting lab configs

**Deep insight:**
- Netmiko is like CLI with training wheels.
- Great for engineers familiar with CLI — use same commands, just automated.

### 🔹 NAPALM – Structured API-style config for routers
**How it works:**
- Uses vendor-specific APIs (NETCONF, RESTCONF, SSH)
- Loads config as structured blocks (like `set interfaces ...`)
- Shows config diffs before committing
- Supports rollback and multi-vendor support

**Why use it:**
- Safe, repeatable, and structured configuration
- Enables config comparison, preview, commit like Git
- Great for production, CI/CD, or version-controlled environments

**Deep insight:**
- NAPALM isn’t about command execution — it’s about **state configuration**
- You describe what you want; NAPALM makes it happen **safely and consistently**

### 🔹 Ansible – Agentless, YAML-based automation framework
**How it works:**
- Uses SSH (or APIs) to push configuration or run modules
- Reads from inventory files and YAML playbooks
- Uses collections like `cisco.ios`, `arista.eos`, etc.
- Stateless execution – every run enforces the desired state

**Why use it:**
- Manage multiple devices at once
- Readable, reusable, scalable automation
- Excellent for infrastructure-as-code, compliance, GitOps

**Deep insight:**
- Ansible is **declarative** — describe what the device should look like
- Not limited to networking — automate cloud, Linux, containers, and more
- Best for large environments or teams needing repeatability and auditability


This project demonstrates full network automation for a **multi-vendor lab** using three Python libraries: **Paramiko**, **Netmiko**, and **NAPALM**. The network topology includes:

- **3 Routers**:
  - Cisco IOS
  - Arista EOS
  - Juniper JunOS
- **1 Cisco Layer 2 Switch**
- **1 Linux-based NAT Gateway (NAT1)**

Each device is configured via a dedicated script that matches its capabilities.

---

## 📈 Network Topology

```
+----------+        +----------+        +----------+
| Cisco R1 |<----->| Arista R2 |<----->| Juniper R3|
+----------+        +----------+        +----------+
     |                   |                  |
     |                   |                  |
     +--------+   +------+-------+   +------+
              |   | Cisco Switch |   |           
              +---+   VLAN Core  +---+             
                  +-------------+   
                         |
                    +---------+
                    |  NAT1   |
                    +---------+
```

---

## 📅 Folder Structure

```
network-automation-project/
├── paramiko_config.py         # Arista + Juniper + Cisco via Paramiko
├── netmiko_config.py          # Cisco + Switch + NAT via Netmiko
├── napalm_config.py           # Cisco + Arista + Juniper via NAPALM
├── ansible/
│   ├── hosts.yaml             # Ansible inventory for switch
│   └── vlan_config.yaml       # Ansible playbook for VLAN config
├── requirements.txt           # Python dependencies
├── network_topology.png       # (Optional) Visual Diagram
└── README.md                  # This file
```

---

## 📖 Tools & Libraries Used

| Tool      | Purpose                         |
|-----------|----------------------------------|
| Paramiko  | SSH automation (low-level)      |
| Netmiko   | Simplified CLI automation       |
| NAPALM    | Multi-vendor, API-style config  |
| Ansible   | YAML-based config management   |

---

## 🔧 Configuration Summary

| Device        | OS           | IP               | Library Used |
|---------------|--------------|------------------|---------------|
| Cisco Router  | Cisco IOS    | 192.168.122.10   | Netmiko / NAPALM / Paramiko |
| Arista Router | Arista EOS   | 192.168.122.30   | Paramiko / NAPALM |
| Juniper Router| Juniper OS   | 192.168.122.20   | Paramiko / NAPALM |
| Switch        | Cisco IOS    | 192.168.122.50   | Netmiko / Ansible |
| NAT1 Gateway  | Linux        | 192.168.122.1    | Netmiko       |

---

## 💡 What Each Script Does

### 1. **`paramiko_config.py`**
- Sends CLI commands to:
  - Cisco (if required)
  - Arista
  - Juniper
- Uses `invoke_shell()` to simulate human SSH interaction
- Example: IP addressing, hostname, static routes

### 2. **`netmiko_config.py`**
- Automates:
  - Cisco IOS router interfaces and routing
  - Cisco Switch VLANs and port settings
  - NAT1 IP configuration and IP forwarding (Linux CLI)

### 3. **`napalm_config.py`**
- API-style configuration for:
  - Cisco IOS (interface + route)
  - Arista EOS (multi-interface + static route)
  - Juniper JunOS (interface + static route)
- Shows config differences and commits only changes

### 4. **`ansible/vlan_config.yaml`**
- Uses Ansible + `cisco.ios` collection to:
  - Create VLANs (10 = HR, 20 = TECH, 30 = FIN)
  - Assign access ports on Cisco Switch (Ethernet0–2)

---

## 🔁 Command Execution

### Python scripts:
```bash
python3 paramiko_config.py
python3 netmiko_config.py
python3 napalm_config.py
```

### Ansible Playbook:
```bash
ansible-playbook -i ansible/hosts.yaml ansible/vlan_config.yaml
```

---

## 📦 Expected Results
- **Routers**: Hostname, IPs, and routes to NAT1
- **Switch**:
  - VLAN 10 → Ethernet0 → Cisco
  - VLAN 20 → Ethernet1 → Arista
  - VLAN 30 → Ethernet2 → Juniper
- **NAT1**: IP set, IP forwarding enabled, NAT active

---

## ⚠️ Troubleshooting Tips
- Use `ping`, `show ip route`, `show vlan brief`, or `show run`
- On Linux NAT, check with `ip a` and `iptables -t nat -L`
- Use `-vvv` in Ansible for verbose debugging

---

## 🌟 Future Improvements
- VLAN trunking automation
- DHCP configuration via Netmiko/Ansible
- YAML-driven modular configs
- Inventory-driven dynamic templates

---

## 📚 References
- [Netmiko Docs](https://ktbyers.github.io/netmiko/)
- [NAPALM Docs](https://napalm.readthedocs.io)
- [Paramiko Docs](http://docs.paramiko.org/)
- [Ansible Cisco IOS](https://docs.ansible.com/ansible/latest/collections/cisco/ios/)

---

## 🚀 Author
**Jeevanandh Ravi** – Network Engineer & Automation Enthusiast

---

Happy Automating! 🚀📊
