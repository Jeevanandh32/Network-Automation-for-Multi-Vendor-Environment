from netmiko import ConnectHandler

# --------------------------------------
# Cisco Router (IOU1)
# --------------------------------------
router1 = {
    "device_type": "cisco_ios",
    "host": "192.168.122.10",
    "username": "admin",
    "password": "cisco",
    "secret": "cisco"
}

router1_cmds = [
    "enable",
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

# --------------------------------------
# Arista Router (IOU3)
# --------------------------------------
router2 = {
    "device_type": "arista_eos",
    "host": "192.168.122.30",
    "username": "admin",
    "password": "arista",
}

router2_cmds = [
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

# --------------------------------------
# Juniper Router (IOU2)
# --------------------------------------
router3 = {
    "device_type": "juniper",
    "host": "192.168.122.20",
    "username": "admin",
    "password": "juniper",
}

router3_cmds = [
    "set system host-name JuniperIOU2",
    "set interfaces ge-0/0/0 unit 0 family inet address 192.168.122.20/24",
    "set interfaces ge-0/0/1 unit 0 family inet address 20.0.0.2/24",
    "set routing-options static route 0.0.0.0/0 next-hop 192.168.122.1",
    "commit and-quit"
]

# --------------------------------------
# Cisco Switch (Switch1)
# --------------------------------------
switch = {
    "device_type": "cisco_ios",
    "host": "192.168.122.50",
    "username": "admin",
    "password": "cisco",
    "secret": "cisco"
}

switch_cmds = [
    "enable",
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

# --------------------------------------
# NAT1 Linux Guest (Debian/Ubuntu)
# --------------------------------------
nat1 = {
    "device_type": "linux",
    "host": "192.168.122.1",
    "username": "student",     
    "password": "student"     
}

nat1_cmds = [
    "sudo ip addr add 192.168.122.1/24 dev nat0",
    "sudo ip link set nat0 up",
    "sudo sysctl -w net.ipv4.ip_forward=1",
    "sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE"
]

# --------------------------------------
# Helper function
# --------------------------------------
def configure_device(device, commands, label):
    print(f"\n🔧 Connecting to {label} ({device['host']})...")
    try:
        conn = ConnectHandler(**device)
        if device["device_type"] == "cisco_ios":
            conn.enable()
        if device["device_type"] in ["linux", "juniper"]:
            output = conn.send_command('\n'.join(commands), expect_string=r"#")
        else:
            output = conn.send_config_set(commands)
        print(f"{label} configured successfully!\n")
        conn.disconnect()
    except Exception as e:
        print(f"Failed to configure {label}: {e}")

# --------------------------------------
# Run all configs
# --------------------------------------
configure_device(router1, router1_cmds, "CiscoIOU1")
configure_device(router2, router2_cmds, "AristaIOU3")
configure_device(router3, router3_cmds, "JuniperIOU2")
configure_device(switch, switch_cmds, "Switch1")
configure_device(nat1, nat1_cmds, "NAT1 Linux Guest")
