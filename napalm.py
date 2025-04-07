from napalm import get_network_driver

# Cisco IOS Router
cisco_driver = get_network_driver("ios")
cisco_device = cisco_driver("192.168.122.10", "admin", "cisco")
cisco_config = """
hostname CiscoIOU1
interface Ethernet0/0
 ip address 192.168.122.10 255.255.255.0
 no shutdown
!
interface Ethernet0/1
 ip address 10.0.0.1 255.255.255.0
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 192.168.122.1
"""

# Arista EOS Router
arista_driver = get_network_driver("eos")
arista_device = arista_driver("192.168.122.30", "admin", "arista")
arista_config = """
hostname AristaIOU3
interface Ethernet0
 ip address 192.168.122.30/24
 no shutdown
!
interface Ethernet1
 ip address 10.0.0.2/24
 no shutdown
!
interface Ethernet2
 ip address 20.0.0.1/24
 no shutdown
!
ip route 0.0.0.0/0 192.168.122.1
"""

# Juniper JunOS Router
juniper_driver = get_network_driver("junos")
juniper_device = juniper_driver("192.168.122.20", "admin", "juniper")
juniper_config = """
set system host-name JuniperIOU2
set interfaces ge-0/0/0 unit 0 family inet address 192.168.122.20/24
set interfaces ge-0/0/1 unit 0 family inet address 20.0.0.2/24
set routing-options static route 0.0.0.0/0 next-hop 192.168.122.1
"""

# Function to apply config
def configure_napalm(device, config, label):
    print(f"\n🔧 Connecting to {label}...")
    device.open()
    device.load_merge_candidate(config=config)
    diffs = device.compare_config()
    if diffs:
        print(f"Changes for {label}:\n{diffs}")
        device.commit_config()
        print(f"{label} configured and committed.\n")
    else:
        print(f"No changes needed on {label}.")
    device.close()

# Deploy
configure_napalm(cisco_device, cisco_config, "CiscoIOU1")
configure_napalm(arista_device, arista_config, "AristaIOU3")
configure_napalm(juniper_device, juniper_config, "JuniperIOU2")
