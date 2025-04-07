import paramiko
import time

def send_commands(ip, username, password, commands, label):
    print(f"\n Connecting to {label} ({ip})...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        shell = client.invoke_shell()
        time.sleep(1)
        shell.recv(1000)

        for cmd in commands:
            shell.send(cmd + '\n')
            time.sleep(1)

        output = shell.recv(9999).decode()
        print(f"{label} configured.\n")
        client.close()

    except Exception as e:
        print(f"Failed to configure {label}: {e}")

# =============================
# 1. Cisco Router (IOU1)
# =============================
cisco_commands = [
    "enable",
    "cisco",
    "configure terminal",
    "hostname CiscoIOU1",
    "interface Ethernet0/0",
    "ip address 192.168.122.10 255.255.255.0",
    "no shutdown",
    "interface Ethernet0/1",
    "ip address 10.0.0.1 255.255.255.0",
    "no shutdown",
    "ip route 0.0.0.0 0.0.0.0 192.168.122.1",
    "end",
    "write memory"
]

send_commands("192.168.122.10", "admin", "cisco", cisco_commands, "CiscoIOU1")

# =============================
# 2. Arista Router (IOU3)
# =============================
arista_commands = [
    "enable",
    "configure terminal",
    "hostname AristaIOU3",
    "interface Ethernet0",
    "ip address 192.168.122.30/24",
    "no shutdown",
    "interface Ethernet1",
    "ip address 10.0.0.2/24",
    "no shutdown",
    "interface Ethernet2",
    "ip address 20.0.0.1/24",
    "no shutdown",
    "ip route 0.0.0.0/0 192.168.122.1",
    "end",
    "write memory"
]

send_commands("192.168.122.30", "admin", "arista", arista_commands, "AristaIOU3")

# =============================
# 3. Juniper Router (IOU2)
# =============================
juniper_commands = [
    "cli",
    "configure",
    "set system host-name JuniperIOU2",
    "set interfaces ge-0/0/0 unit 0 family inet address 192.168.122.20/24",
    "set interfaces ge-0/0/1 unit 0 family inet address 20.0.0.2/24",
    "set routing-options static route 0.0.0.0/0 next-hop 192.168.122.1",
    "commit and-quit"
]

send_commands("192.168.122.20", "admin", "juniper", juniper_commands, "JuniperIOU2")

# =============================
# 4. Cisco Switch
# =============================
switch_commands = [
    "enable",
    "cisco",
    "configure terminal",
    "hostname Switch1",
    "interface Ethernet0",
    "switchport mode access",
    "switchport access vlan 1",
    "no shutdown",
    "interface Ethernet1",
    "switchport mode access",
    "switchport access vlan 1",
    "no shutdown",
    "interface Ethernet2",
    "switchport mode access",
    "switchport access vlan 1",
    "no shutdown",
    "interface Ethernet3",
    "switchport mode access",
    "switchport access vlan 1",
    "no shutdown",
    "end",
    "write memory"
]

send_commands("192.168.122.50", "admin", "cisco", switch_commands, "Switch1")

# =============================
# 5. NAT1 Linux (via paramiko)
# =============================
linux_commands = [
    "sudo ip addr add 192.168.122.1/24 dev nat0",
    "sudo ip link set nat0 up",
    "sudo sysctl -w net.ipv4.ip_forward=1",
    "sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE"
]

def send_linux_commands(ip, username, password, commands, label):
    print(f"\n🔌 Connecting to {label} ({ip})...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=username, password=password)
        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
        print(f"{label} configured.\n")
        client.close()
    except Exception as e:
        print(f"Failed to configure {label}: {e}")

send_linux_commands("192.168.122.1", "user", "password", linux_commands, "NAT1 Linux Guest")
