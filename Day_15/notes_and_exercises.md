# Day 15: Networking Basics & Troubleshooting

## Learning Objectives
By the end of Day 15, you will:
- Understand basic TCP/IP and networking concepts
- View and interpret network interface configuration
- Use essential network diagnostic tools (ping, traceroute, netstat, ss)
- Perform DNS lookups and troubleshooting
- Follow systematic network troubleshooting methodology
- Check which processes are using network ports

**Estimated Time:** 1 hour

---

## Why Basic Networking Matters

| Skill | Why It Matters | Real Example |
|-------|----------------|--------------|
| **View IP Configuration** | Know your system's network identity | What's my IP address? Gateway? |
| **Test Connectivity** | Verify system can reach others | Can I ping Google? My database server? |
| **Troubleshoot DNS** | Most issues are DNS-related | Website unreachable? Check DNS first |
| **Check Open Ports** | Security and service availability | Is web server listening on port 80? |
| **Trace Network Path** | Find where connection fails | Where does packet get lost? |

**Essential for:** Anyone working with Linux servers, cloud instances, containerized apps, or networked services

---

## Sample Environment Setup

```bash
# Create test directory
mkdir -p ~/day15_test/{logs,scripts}
```

## Part 1: Basic Networking Concepts

### TCP/IP Layers

| Layer | What It Does | Example | Tools |
|-------|--------------|---------|-------|
| **Application** | Services users interact with | HTTP (web), SSH (remote), DNS (names) | `curl`, `dig`, `telnet` |
| **Transport** | Port-to-port delivery | TCP (reliable), UDP (fast) | `netstat`, `ss` |
| **Network** | IP addressing & routing | Sends packets between networks | `ping`, `traceroute`, `ip route` |
| **Link** | Physical network connection | Ethernet, Wi-Fi | `ip link`, `ethtool` |

### TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| **Reliable?** | Yes (checks delivery) | No (fire and forget) |
| **Ordered?** | Yes (packets arrive in order) | No (may arrive out of order) |
| **Speed** | Slower (more overhead) | Faster (less overhead) |
| **Use When** | Data must arrive correctly | Speed more important than reliability |
| **Examples** | Web (HTTP), Email (SMTP), SSH | DNS lookups, Video streaming, Gaming |

### IP Addresses

**IPv4 Format:** 4 numbers (0-255) separated by dots
- Example: `192.168.1.10`
- Total: 32 bits (about 4 billion addresses)

**Special IP Addresses:**
| IP Address | Meaning |
|------------|---------|
| `127.0.0.1` | **Loopback** - refers to this computer (localhost) |
| `192.168.x.x` | **Private network** - home/office networks |
| `10.x.x.x` | **Private network** - large corporate networks |
| `0.0.0.0` | **All interfaces** or "not set yet" |
| `255.255.255.255` | **Broadcast** - send to everyone on network |

**What's a Subnet?**
- Network divided into smaller segments
- `/24` means first 3 numbers are network, last number is host
- Example: `192.168.1.0/24` = addresses from `192.168.1.1` to `192.168.1.254`

### Common Network Ports

| Port | Service | What It's For |
|------|---------|---------------|
| **22** | SSH | Remote login (secure) |
| **80** | HTTP | Websites (not encrypted) |
| **443** | HTTPS | Websites (encrypted/secure) |
| **53** | DNS | Converts names to IP addresses |
| **25** | SMTP | Sending email |
| **3306** | MySQL | Database connections |
| **5432** | PostgreSQL | Database connections |
| **6379** | Redis | Cache database |
| **8080** | HTTP-Alt | Alternative web server port |

---

## Part 2: Viewing Network Configuration

### Command Reference: Network Info

| Command | What It Shows | Example |
|---------|---------------|---------|
| `ip addr` or `ip a` | All network interfaces and IP addresses | `ip a` |
| `ip link` | Interface status (up/down) | `ip link show` |
| `ip route` | Where packets go (routing table) | `ip route show` |
| `hostname` | Computer's name | `hostname` |
| `hostname -I` | All IP addresses of this machine | `hostname -I` |
| `cat /etc/resolv.conf` | DNS servers being used | `cat /etc/resolv.conf` |
| `cat /etc/hosts` | Static name-to-IP mappings | `cat /etc/hosts` |

### View Your Network Configuration

```bash
# Show all your network info (use our script)
~/day15_test/scripts/show-network.sh

# Show all interfaces and IPs
ip addr show
# Shorter version:
ip a

# Brief format (easier to read)
ip -br addr show

# Show only IPv4
ip -4 addr show

# Show specific interface
ip addr show dev eth0

# Show interface status (up/down)
ip link show

# Show routing table (where packets go)
ip route show
# Or shorter:
ip r

# Find your default gateway
ip route | grep default

# Show your hostname
hostname

# Show all your IP addresses
hostname -I

# Show DNS servers
cat /etc/resolv.conf

# Show static name mappings
cat /etc/hosts
```

**Understanding `ip addr` Output:**
```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 00:11:22:33:44:55
    inet 192.168.1.10/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::211:22ff:fe33:4455/64 scope link
```

- `eth0` - Interface name
- `UP` - Interface is active
- `192.168.1.10/24` - IP address and subnet
- `00:11:22:33:44:55` - MAC address (hardware address)

**Understanding `ip route` Output:**
```
default via 192.168.1.1 dev eth0 
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.10
```

- `default via 192.168.1.1` - Default gateway (where to send internet traffic)
- `dev eth0` - Use eth0 interface
- `192.168.1.0/24` - Local network directly connected

### Hands-On: View Your Network

```bash
# 1. Run our network info script
~/day15_test/scripts/show-network.sh

# 2. Show all interfaces in brief format
ip -br addr show

# 3. Find your main IP address
hostname -I | awk '{print $1}'

# 4. Find your default gateway
ip route | grep default | awk '{print $3}'

# 5. Check DNS servers
grep nameserver /etc/resolv.conf

# 6. Check if interface is up
ip link show | grep "state UP"

# 7. Show only active interfaces
ip -br link show | grep UP
```

---

## Part 3: Testing Network Connectivity

### Command Reference: Connectivity Testing

| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `ping HOST` | Test if host is reachable | First step in troubleshooting |
| `ping -c 4 HOST` | Send 4 packets only | Quick test |
| `traceroute HOST` | Show path packets take | Find where connection fails |
| `tracepath HOST` | Like traceroute (no root) | Alternative to traceroute |
| `mtr HOST` | Continuous traceroute | Monitor connection quality |

### Ping - Test Connectivity

**What it does:** Sends ICMP "echo request" packets to check if host is alive

```bash
# Basic ping (runs forever, press Ctrl+C to stop)
ping google.com

# Send only 4 packets
ping -c 4 google.com

# Faster pings (every 0.2 seconds)
ping -c 10 -i 0.2 google.com

# Quiet mode (only show summary)
ping -c 10 -q google.com

# Test loopback (always works if network stack is OK)
ping 127.0.0.1

# Test your own IP
ping $(hostname -I | awk '{print $1}')

# Test your gateway
ping $(ip route | grep default | awk '{print $3}')

# Test internet (Google's DNS)
ping 8.8.8.8

# Test with name (checks DNS too)
ping google.com
```

**Understanding Ping Output:**
```
PING google.com (172.217.14.206) 56(84) bytes of data.
64 bytes from lga25s61-in-f14.1e100.net (172.217.14.206): icmp_seq=1 ttl=117 time=10.2 ms
64 bytes from lga25s61-in-f14.1e100.net (172.217.14.206): icmp_seq=2 ttl=117 time=10.5 ms

--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 10.200/10.350/10.500/0.150 ms
```

- `time=10.2 ms` - **Latency** (how long round-trip took)
  - < 20ms: Excellent (local network)
  - 20-100ms: Good (same country)
  - 100-200ms: Acceptable (international)
  - > 200ms: Slow
- `0% packet loss` - **All packets received** (good!)
  - 0%: Perfect
  - 1-5%: Minor issues
  - > 5%: Serious problems
- `ttl=117` - Hops remaining (started at ~128)

**Common Ping Errors:**
- `Destination Host Unreachable` - Can't reach host (routing issue)
- `Network is unreachable` - No route to network
- `Name or service not known` - DNS resolution failed
- `Request timeout` - No response (firewall blocking, or host down)

### Traceroute - Trace Network Path

**What it does:** Shows each hop (router) packets pass through

```bash
# Basic traceroute
traceroute google.com

# Faster (no DNS lookups)
traceroute -n google.com

# Alternative (doesn't need root)
tracepath google.com

# Continuous traceroute (better for monitoring)
mtr google.com

# MTR with no DNS (faster)
mtr -n google.com

# MTR report mode (run 10 cycles and show summary)
mtr -r -c 10 google.com
```

**Understanding Traceroute Output:**
```
traceroute to google.com (172.217.14.206), 30 hops max
 1  192.168.1.1 (192.168.1.1)  1.234 ms  1.123 ms  1.056 ms
 2  10.0.0.1 (10.0.0.1)  5.432 ms  5.234 ms  5.123 ms
 3  * * *
 4  172.217.14.206 (172.217.14.206)  10.234 ms  10.123 ms  10.056 ms
```

- **Line 1:** Your home router/gateway (usually fastest)
- **Line 2:** ISP's router
- **Line 3:** `* * *` means router didn't respond (common, not necessarily bad)
- **Line 4:** Destination reached
- **Three times:** Shows latency variance (three tests per hop)

**What to look for:**
- **Sudden latency jump:** Congested link
- **Consistent timeouts at one hop:** Problem at that router
- **High packet loss:** Connection quality issues

### Hands-On: Test Connectivity

```bash
# 1. Run our connectivity test script
~/day15_test/scripts/test-network.sh

# 2. Test loopback (yourself)
ping -c 4 127.0.0.1

# 3. Test your gateway
GATEWAY=$(ip route | grep default | awk '{print $3}')
echo "Testing gateway: $GATEWAY"
ping -c 4 $GATEWAY

# 4. Test internet (IP address - bypasses DNS)
ping -c 4 8.8.8.8

# 5. Test with DNS
ping -c 4 google.com

# 6. Trace route to see path
traceroute -n google.com

# 7. Or use MTR for better view
mtr -r -c 10 google.com

# 8. If ping fails, which step fails?
# Loopback → Gateway → Internet IP → Internet Name
```

---

## Part 4: Checking Ports and Services

### Command Reference: Port Checking

| Command | What It Shows | Common Usage |
|---------|---------------|--------------|
| `ss -tuln` | All TCP/UDP listening ports | `ss -tuln` |
| `ss -tulnp` | Include process info (needs root) | `sudo ss -tulnp` |
| `ss -t` | All TCP connections | `ss -t` |
| `netstat -tuln` | Legacy version of ss | `netstat -tuln` |
| `lsof -i :PORT` | What's using specific port | `sudo lsof -i :80` |

### Understanding Ports

**What's a port?** Like apartment numbers for a building (IP address)
- IP address = building address
- Port = apartment number
- Each service listens on specific port

### View Open Ports

```bash
# Modern command: ss (faster than netstat)
ss -tuln

# With process names (needs root)
sudo ss -tulnp

# Show only listening ports
ss -tuln | grep LISTEN

# Show only TCP
ss -tln

# Show only UDP
ss -uln

# Show all connections (not just listening)
ss -tun

# Legacy command: netstat (slower but works everywhere)
netstat -tuln
sudo netstat -tulnp

# Find what's using a specific port
sudo ss -tulnp | grep :80
sudo lsof -i :80
sudo lsof -i :443

# Find all ports used by a process
sudo lsof -p PID
sudo lsof -c nginx
```

**Understanding `ss -tuln` Output:**
```
State    Recv-Q Send-Q  Local Address:Port   Peer Address:Port
LISTEN   0      128     0.0.0.0:22           0.0.0.0:*
LISTEN   0      128     0.0.0.0:80           0.0.0.0:*
ESTAB    0      0       192.168.1.10:22      192.168.1.5:54321
```

**Columns explained:**
- **State:** Connection status
  - `LISTEN` - Waiting for connections (server)
  - `ESTAB` - Active connection
  - `TIME-WAIT` - Connection just closed
- **Local Address:Port** - This machine's IP and port
  - `0.0.0.0:22` - Listening on all interfaces, port 22 (SSH)
  - `192.168.1.10:22` - Specific IP, port 22
- **Peer Address:Port** - Remote machine's IP and port

**Common States:**
| State | Meaning |
|-------|---------|
| `LISTEN` | Server waiting for connections |
| `ESTAB` | Active connection |
| `SYN-SENT` | Trying to connect |
| `SYN-RECV` | Received connection request |
| `FIN-WAIT` | Closing connection |
| `TIME-WAIT` | Connection closed, waiting |
| `CLOSE-WAIT` | Remote closed, local not yet |

### Check If Port Is Open

```bash
# Method 1: Using netcat (nc)
nc -zv localhost 80
nc -zv google.com 443

# Method 2: Using telnet
telnet localhost 80
telnet google.com 443
# (Press Ctrl+] then type 'quit' to exit)

# Method 3: Check if process is listening
sudo ss -tulnp | grep :80

# Method 4: Using lsof
sudo lsof -i :80
```

**Output interpretation:**
- `Connection refused` - Nothing listening on that port
- `No route to host` - Can't reach the host
- `Connection successful` or `Connected` - Port is open!
- `Connection timed out` - Firewall blocking or host down

### Hands-On: Check Ports

```bash
# 1. Show all listening ports
ss -tuln

# 2. Show with process names (needs root)
sudo ss -tulnp

# 3. Find what's using port 22 (SSH)
sudo ss -tulnp | grep :22

# 4. Check if port 80 is open locally
nc -zv localhost 80
# Or
sudo ss -tuln | grep :80

# 5. Check if common services are listening
echo "Checking common ports..."
for port in 22 80 443 3306 5432; do
    if sudo ss -tuln | grep -q ":$port "; then
        echo "Port $port: OPEN"
    else
        echo "Port $port: CLOSED"
    fi
done

# 6. Count total connections
ss -tun | wc -l

# 7. Show only established connections
ss -tun state established
```

---

## Part 5: DNS Troubleshooting

### Command Reference: DNS Tools

| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `dig DOMAIN` | Detailed DNS lookup | Troubleshooting, see all details |
| `dig +short DOMAIN` | Quick answer only | Just need the IP |
| `nslookup DOMAIN` | Simple DNS lookup | Quick checks |
| `host DOMAIN` | Basic DNS lookup | Simplest option |
| `cat /etc/resolv.conf` | Show DNS servers | Check what DNS you're using |

### DNS Basics

**What is DNS?** Converts names to IP addresses
- You type: `google.com`
- DNS converts to: `142.250.185.46`
- Your computer then connects to that IP

**DNS Records Types:**
| Type | What It Is | Example |
|------|------------|---------|
| **A** | IPv4 address | `example.com → 93.184.216.34` |
| **AAAA** | IPv6 address | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | Alias (points to another name) | `www.example.com → example.com` |
| **MX** | Mail server | `example.com → mail.example.com` |
| **NS** | Nameserver | `example.com → ns1.example.com` |
| **TXT** | Text info | Used for verification, SPF, etc. |

### Perform DNS Lookups

```bash
# Quick lookup - just show IP
dig +short google.com

# Detailed lookup
dig google.com

# Query specific DNS server
dig @8.8.8.8 google.com
dig @1.1.1.1 google.com

# Query specific record type
dig google.com A        # IPv4 address
dig google.com AAAA     # IPv6 address
dig google.com MX       # Mail servers
dig google.com NS       # Nameservers
dig google.com TXT      # Text records

# Reverse lookup (IP to name)
dig -x 8.8.8.8

# Trace DNS resolution path
dig +trace google.com

# Simple lookup with nslookup
nslookup google.com
nslookup google.com 8.8.8.8  # Use specific DNS server

# Simplest lookup with host
host google.com
host -t MX google.com    # Mail servers
host -t NS google.com    # Nameservers
host 8.8.8.8             # Reverse lookup

# Check your DNS configuration
cat /etc/resolv.conf
```

**Understanding `dig` Output:**
```
; <<>> DiG 9.16.1 <<>> google.com
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             300     IN      A       142.250.185.46

;; Query time: 10 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Tue Oct 17 10:30:00 UTC 2025
;; MSG SIZE  rcvd: 55
```

- **QUESTION:** What we asked for (A record for google.com)
- **ANSWER:** The result (IP is 142.250.185.46)
- **300:** TTL (Time To Live) - cache for 300 seconds
- **Query time:** How long DNS lookup took
- **SERVER:** Which DNS server answered

### Troubleshoot DNS Issues

```bash
# 1. Check DNS servers configured
cat /etc/resolv.conf

# 2. Test if DNS server is reachable
ping -c 2 8.8.8.8
ping -c 2 $(grep nameserver /etc/resolv.conf | head -1 | awk '{print $2}')

# 3. Test DNS resolution
dig +short google.com

# 4. Compare different DNS servers
echo "Your DNS:"
dig +short google.com
echo "Google DNS:"
dig @8.8.8.8 +short google.com
echo "Cloudflare DNS:"
dig @1.1.1.1 +short google.com

# 5. Check if it's DNS or network
ping -c 2 8.8.8.8        # If this works but next fails, it's DNS
ping -c 2 google.com     # This needs DNS

# 6. Check /etc/hosts for static entries
grep google /etc/hosts

# 7. Flush DNS cache (systemd systems)
sudo systemd-resolve --flush-caches
# Check if it helped:
dig +short google.com
```

**Common DNS Problems:**

| Problem | Symptom | Solution |
|---------|---------|----------|
| **No DNS configured** | `/etc/resolv.conf` empty | Add `nameserver 8.8.8.8` |
| **DNS server down** | Can ping IPs but not names | Change to `8.8.8.8` or `1.1.1.1` |
| **Stale cache** | Old IP returned | Flush cache |
| **Network issue** | Can't reach DNS server | Check network connectivity first |
| **Wrong DNS** | Company sites don't resolve | Use company DNS server |

### Hands-On: DNS Troubleshooting

```bash
# 1. Check your DNS configuration
cat /etc/resolv.conf

# 2. Quick DNS test
dig +short google.com

# 3. Detailed DNS lookup
dig google.com

# 4. Test different DNS servers
echo "Testing Google DNS..."
dig @8.8.8.8 +short google.com
echo "Testing Cloudflare DNS..."
dig @1.1.1.1 +short google.com

# 5. Check if DNS is the problem
echo -n "Ping by IP (8.8.8.8): "
ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1 && echo "OK" || echo "FAILED"
echo -n "Ping by name (google.com): "
ping -c 1 -W 2 google.com > /dev/null 2>&1 && echo "OK" || echo "FAILED"

# 6. Lookup different record types
echo "A record:"
dig +short google.com A
echo "MX record:"
dig +short google.com MX
echo "NS record:"
dig +short google.com NS

# 7. Reverse lookup
dig +short -x 8.8.8.8
```

---

## Part 6: Network Troubleshooting Methodology

### Step-by-Step Troubleshooting

**Follow this order** (bottom-up approach):

```
1. Physical Layer: Is cable plugged in? Interface up?
   ↓
2. Network Layer: Can I ping gateway? Internet?
   ↓
3. DNS Layer: Can I resolve names?
   ↓
4. Transport Layer: Is port open?
   ↓
5. Application Layer: Is service responding correctly?
```

### Quick Troubleshooting Script

```bash
# Create comprehensive test script
cat > ~/day15_test/scripts/diagnose.sh << 'EOF'
#!/bin/bash
echo "========================================="
echo "   NETWORK DIAGNOSTIC TOOL"
echo "========================================="
echo ""

# 1. Check interface status
echo "1. Interface Status:"
if ip link show | grep -q "state UP"; then
    echo "   ✓ At least one interface is UP"
    ip -br link show | grep UP | head -3
else
    echo "   ✗ No interfaces are UP!"
fi
echo ""

# 2. Check IP configuration
echo "2. IP Configuration:"
IP=$(hostname -I | awk '{print $1}')
if [ -n "$IP" ]; then
    echo "   ✓ IP Address: $IP"
else
    echo "   ✗ No IP address assigned!"
fi
echo ""

# 3. Check gateway
echo "3. Gateway Connectivity:"
GW=$(ip route | grep default | awk '{print $3}')
if [ -n "$GW" ]; then
    echo "   Gateway: $GW"
    if ping -c 2 -W 2 $GW > /dev/null 2>&1; then
        echo "   ✓ Gateway is reachable"
    else
        echo "   ✗ Cannot reach gateway!"
    fi
else
    echo "   ✗ No default gateway configured!"
fi
echo ""

# 4. Check internet connectivity
echo "4. Internet Connectivity:"
if ping -c 2 -W 2 8.8.8.8 > /dev/null 2>&1; then
    echo "   ✓ Internet is reachable (8.8.8.8)"
else
    echo "   ✗ Cannot reach internet!"
fi
echo ""

# 5. Check DNS
echo "5. DNS Resolution:"
DNS=$(grep nameserver /etc/resolv.conf | head -1 | awk '{print $2}')
if [ -n "$DNS" ]; then
    echo "   DNS Server: $DNS"
    if dig +short +time=2 google.com @$DNS > /dev/null 2>&1; then
        echo "   ✓ DNS is working"
    else
        echo "   ✗ DNS resolution failed!"
    fi
else
    echo "   ✗ No DNS server configured!"
fi
echo ""

# 6. Summary
echo "========================================="
echo "RECOMMENDATION:"
if [ -z "$IP" ]; then
    echo "• Check network cable/Wi-Fi"
    echo "• Run: sudo dhclient"
elif [ -z "$GW" ]; then
    echo "• No gateway configured"
    echo "• Check network configuration"
elif ! ping -c 1 -W 2 $GW > /dev/null 2>&1; then
    echo "• Gateway unreachable"
    echo "• Check router/switch"
elif ! ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
    echo "• No internet connectivity"
    echo "• Check ISP connection"
elif ! dig +short +time=2 google.com > /dev/null 2>&1; then
    echo "• DNS not working"
    echo "• Add 'nameserver 8.8.8.8' to /etc/resolv.conf"
else
    echo "• Network appears to be working correctly!"
fi
echo "========================================="
EOF

chmod +x ~/day15_test/scripts/diagnose.sh
```

### Common Network Problems & Solutions

| Problem | Symptoms | Solution |
|---------|----------|----------|
| **No IP address** | `ip a` shows no IP | Check cable, run `sudo dhclient`, check DHCP server |
| **Can't reach gateway** | Ping gateway fails | Check cable, check router, verify gateway IP |
| **Can ping IPs but not names** | `ping 8.8.8.8` works, `ping google.com` fails | DNS issue - check `/etc/resolv.conf` |
| **Port not open** | Service not accessible | Check if service running, firewall rules |
| **Slow connection** | High ping times | Check `mtr`, look for packet loss, congested link |
| **Connection timeout** | Service doesn't respond | Firewall blocking, service down, wrong port |

### Hands-On: Full Troubleshooting

```bash
# 1. Run diagnostic script
~/day15_test/scripts/diagnose.sh

# 2. Manual step-by-step check
echo "Step 1: Check interfaces"
ip -br link show

echo "Step 2: Check IP addresses"
ip -br addr show

echo "Step 3: Check gateway"
ip route | grep default

echo "Step 4: Ping tests"
echo -n "  Loopback: "
ping -c 1 -W 1 127.0.0.1 > /dev/null 2>&1 && echo "OK" || echo "FAIL"

GW=$(ip route | grep default | awk '{print $3}')
if [ -n "$GW" ]; then
    echo -n "  Gateway ($GW): "
    ping -c 1 -W 1 $GW > /dev/null 2>&1 && echo "OK" || echo "FAIL"
fi

echo -n "  Internet (8.8.8.8): "
ping -c 1 -W 1 8.8.8.8 > /dev/null 2>&1 && echo "OK" || echo "FAIL"

echo -n "  DNS (google.com): "
ping -c 1 -W 1 google.com > /dev/null 2>&1 && echo "OK" || echo "FAIL"

echo "Step 5: Check DNS configuration"
cat /etc/resolv.conf

echo "Step 6: Check listening services"
sudo ss -tulnp | grep LISTEN | head -5
```

---

## Sample Exercises

### Exercise 1: View Network Configuration
**Task:** Display your network interfaces, IP addresses, gateway, and DNS servers.

**Solution:**
```bash
# Option 1: Use our script
~/day15_test/scripts/show-network.sh

# Option 2: Manual commands
echo "=== Interfaces and IPs ==="
ip -br addr show

echo ""
echo "=== Default Gateway ==="
ip route | grep default

echo ""
echo "=== DNS Servers ==="
grep nameserver /etc/resolv.conf

echo ""
echo "=== Hostname ==="
hostname
hostname -I
```

### Exercise 2: Test Connectivity to Remote Server
**Task:** Test connectivity to google.com and trace the route.

**Solution:**
```bash
# 1. Simple ping test
ping -c 4 google.com

# 2. Trace route (see path packets take)
traceroute google.com
# Or faster with no DNS:
traceroute -n google.com

# 3. Continuous monitoring with mtr
mtr -r -c 10 google.com

# 4. Test specific things
echo "Testing DNS resolution..."
dig +short google.com

echo "Testing by IP (bypasses DNS)..."
ping -c 2 $(dig +short google.com | head -1)

echo "Testing by name (uses DNS)..."
ping -c 2 google.com
```

### Exercise 3: List All Open Ports
**Task:** Show all TCP and UDP ports that are listening on your system.

**Solution:**
```bash
# Method 1: Modern command (ss)
ss -tuln

# Method 2: With process information (needs root)
sudo ss -tulnp

# Method 3: Only show listening ports
ss -tuln | grep LISTEN

# Method 4: Group by port number
ss -tuln | grep LISTEN | awk '{print $5}' | cut -d: -f2 | sort -n

# Method 5: Show what's using common ports
echo "Common ports in use:"
for port in 22 80 443 3306 5432 8080; do
    echo -n "Port $port: "
    if sudo ss -tulnp | grep -q ":$port "; then
        echo "LISTENING - $(sudo ss -tulnp | grep ":$port " | awk '{print $7}' | head -1)"
    else
        echo "not in use"
    fi
done
```

### Exercise 4: Perform DNS Lookup
**Task:** Query DNS records for a domain (google.com) using different tools.

**Solution:**
```bash
# Method 1: Quick answer only
dig +short google.com

# Method 2: Detailed information
dig google.com

# Method 3: Query specific DNS server
dig @8.8.8.8 google.com

# Method 4: Different record types
echo "A record (IPv4):"
dig +short google.com A

echo "AAAA record (IPv6):"
dig +short google.com AAAA

echo "MX record (Mail servers):"
dig +short google.com MX

echo "NS record (Nameservers):"
dig +short google.com NS

# Method 5: Using nslookup (simpler)
nslookup google.com

# Method 6: Using host (simplest)
host google.com
```

### Exercise 5: Troubleshoot Network Issue
**Task:** Systematically diagnose a network connectivity problem.

**Solution:**
```bash
# Use our diagnostic script
~/day15_test/scripts/diagnose.sh

# Or manual step-by-step:

# Step 1: Check interface is up
echo "Step 1: Interface Status"
ip link show | grep "state UP"

# Step 2: Check IP address assigned
echo "Step 2: IP Address"
ip -br addr show | grep UP

# Step 3: Check gateway configured
echo "Step 3: Gateway"
ip route | grep default

# Step 4: Ping gateway
echo "Step 4: Ping Gateway"
GW=$(ip route | grep default | awk '{print $3}')
ping -c 2 $GW

# Step 5: Ping internet
echo "Step 5: Ping Internet"
ping -c 2 8.8.8.8

# Step 6: Check DNS
echo "Step 6: DNS Check"
cat /etc/resolv.conf
dig +short google.com

# Step 7: Trace route to find where it fails
echo "Step 7: Trace Route"
traceroute -n -m 10 google.com
```

### Exercise 6: Check Web Server Port
**Task:** Verify if web server is listening on port 80 and test connectivity.

**Solution:**
```bash
# 1. Check if port 80 is listening
sudo ss -tulnp | grep :80

# 2. If nothing, check 8080 (common alternative)
sudo ss -tulnp | grep :8080

# 3. Check what process is using the port
sudo lsof -i :80

# 4. Test if port is accessible locally
nc -zv localhost 80
# Or
telnet localhost 80

# 5. If web server running, test with curl
curl -I http://localhost

# 6. Check from external IP
curl -I http://$(hostname -I | awk '{print $1}')

# 7. If not working, check if service is running
systemctl status nginx  # or apache2
```

---

## Sample Interview Questions

| # | Question | Difficulty | Topic |
|---|----------|------------|-------|
| 1 | How do you check your IP address and network interfaces? | Basic | Configuration |
| 2 | What's the difference between TCP and UDP? | Basic | Concepts |
| 3 | How do you test if a remote host is reachable? | Basic | Troubleshooting |
| 4 | What command shows which ports are listening? | Basic | Ports |
| 5 | How do you perform a DNS lookup? | Basic | DNS |
| 6 | What's the purpose of a default gateway? | Intermediate | Routing |
| 7 | How do you troubleshoot "can ping IP but not hostname"? | Intermediate | DNS |
| 8 | What does "connection refused" vs "connection timeout" mean? | Intermediate | Troubleshooting |
| 9 | How do you find which process is using port 80? | Intermediate | Ports |
| 10 | Walk me through diagnosing a network connectivity issue. | Advanced | Methodology |

---

## Interview Question Answers

| Question | Answer | Example |
|----------|--------|---------|
| **1. Check IP/Interfaces** | **Modern:** `ip addr show` or `ip a`<br>**Brief:** `ip -br addr show`<br>**Legacy:** `ifconfig`<br>**Just IPs:** `hostname -I` | `ip a` shows all interfaces, IPs, MAC addresses<br>`ip -br addr` shows brief format:<br>`eth0 UP 192.168.1.10/24` |
| **2. TCP vs UDP** | **TCP:** Connection-oriented, reliable, ordered, slower. Use when data integrity matters (HTTP, SSH, email)<br>**UDP:** Connectionless, fast, no guarantees. Use when speed matters (DNS, streaming, gaming) | TCP = phone call (establishes connection)<br>UDP = sending postcards (fire and forget) |
| **3. Test Reachability** | **Basic:** `ping hostname` or `ping IP`<br>**Count:** `ping -c 4 host`<br>**Trace path:** `traceroute host`<br>**Monitor:** `mtr host` | `ping -c 4 google.com`<br>`ping -c 4 8.8.8.8` (by IP)<br>`traceroute google.com` (see route) |
| **4. Show Listening Ports** | **Modern:** `ss -tuln` (all TCP/UDP listening)<br>**With process:** `sudo ss -tulnp`<br>**Legacy:** `netstat -tuln`<br>**Specific port:** `sudo lsof -i :80` | `ss -tuln` shows:<br>`LISTEN 0 128 0.0.0.0:22`<br>means SSH listening on port 22, all interfaces |
| **5. DNS Lookup** | **Quick:** `dig +short domain.com`<br>**Detailed:** `dig domain.com`<br>**Specific DNS:** `dig @8.8.8.8 domain.com`<br>**Simple:** `nslookup domain.com`<br>**Basic:** `host domain.com` | `dig +short google.com` returns just the IP<br>`dig google.com` shows full DNS response |
| **6. Default Gateway** | **Purpose:** Router that forwards traffic to other networks (including internet)<br>**View:** `ip route | grep default`<br>**Format:** `default via 192.168.1.1 dev eth0` | Without gateway, you can only reach local network.<br>Gateway is the "exit door" to outside world |
| **7. Can Ping IP Not Name** | **Problem:** DNS resolution failing<br>**Steps:**<br>1. Check DNS config: `cat /etc/resolv.conf`<br>2. Test DNS server: `ping DNS_IP`<br>3. Try different DNS: `dig @8.8.8.8 google.com`<br>4. Check /etc/hosts<br>5. Flush cache: `sudo systemd-resolve --flush-caches` | `ping 8.8.8.8` works ✓<br>`ping google.com` fails ✗<br>→ DNS problem!<br>Solution: Add `nameserver 8.8.8.8` to `/etc/resolv.conf` |
| **8. Connection Refused vs Timeout** | **Connection Refused:**<br>• Host reachable but nothing listening on port<br>• Fast response (immediate)<br>• Service not running or wrong port<br><br>**Connection Timeout:**<br>• Host unreachable OR firewall blocking<br>• Slow (waits for timeout)<br>• Network issue, firewall, or host down | **Refused:** SSH not running on server<br>`nc -zv server 22` → "Connection refused"<br><br>**Timeout:** Firewall blocking port<br>`nc -zv server 22` → waits... then timeout |
| **9. Find Process on Port** | **Method 1:** `sudo ss -tulnp | grep :80`<br>**Method 2:** `sudo lsof -i :80`<br>**Method 3:** `sudo netstat -tulnp | grep :80`<br>Shows PID and process name | `sudo lsof -i :80` shows:<br>`nginx 1234 root 6u IPv4 TCP *:80 (LISTEN)`<br>→ nginx with PID 1234 using port 80 |
| **10. Troubleshooting Steps** | **Layer-by-layer approach:**<br>1. Check interface: `ip link`<br>2. Check IP: `ip addr`<br>3. Check gateway: `ip route`, `ping gateway`<br>4. Check internet: `ping 8.8.8.8`<br>5. Check DNS: `ping google.com`, `dig google.com`<br>6. Check port: `ss -tuln`, `nc -zv host port`<br>7. Check service: `systemctl status service` | **Example:**<br>`ip link` → UP ✓<br>`ping gateway` → OK ✓<br>`ping 8.8.8.8` → OK ✓<br>`ping google.com` → FAIL ✗<br>→ DNS issue! Check `/etc/resolv.conf` |

---

## Completion Checklist

**Use this to verify your Day 15 mastery:**

### Basic Networking Concepts
- [ ] Understand TCP vs UDP differences
- [ ] Know what IP addresses are and private ranges (192.168.x.x, 10.x.x.x)
- [ ] Understand what a default gateway is
- [ ] Know what DNS does (converts names to IPs)
- [ ] Understand common ports (22, 80, 443, 3306, etc.)
- [ ] Know what localhost/127.0.0.1 means

### Viewing Network Configuration
- [ ] Can view network interfaces with `ip a` or `ip link`
- [ ] Can find your IP address with `hostname -I`
- [ ] Can view routing table with `ip route`
- [ ] Can find default gateway from routing table
- [ ] Can check DNS servers in `/etc/resolv.conf`
- [ ] Can check hostname with `hostname`

### Testing Connectivity
- [ ] Can ping a host to test connectivity
- [ ] Understand ping output (latency, packet loss, TTL)
- [ ] Know when to use `ping -c` to limit packets
- [ ] Can use traceroute to see packet path
- [ ] Can use `mtr` for continuous monitoring
- [ ] Can test loopback, gateway, internet, and DNS separately

### Checking Ports and Services
- [ ] Can list listening ports with `ss -tuln`
- [ ] Can find process using a port with `sudo ss -tulnp` or `lsof`
- [ ] Understand port states (LISTEN, ESTAB, etc.)
- [ ] Can check if specific port is open with `nc` or `telnet`
- [ ] Know difference between TCP and UDP ports
- [ ] Can identify common services by port number

### DNS Troubleshooting
- [ ] Can perform DNS lookup with `dig` or `nslookup`
- [ ] Can query specific DNS server with `dig @8.8.8.8`
- [ ] Can lookup different record types (A, MX, NS)
- [ ] Can diagnose DNS vs network issues
- [ ] Know where DNS configuration is stored
- [ ] Can test different DNS servers

### Network Troubleshooting
- [ ] Have systematic troubleshooting methodology
- [ ] Can distinguish between network and DNS problems
- [ ] Can trace where connection fails (gateway, internet, DNS)
- [ ] Know difference between "connection refused" and "timeout"
- [ ] Can check interface status
- [ ] Can verify service is listening on expected port

---

## Command Quick Reference Card

### View Network Configuration
```bash
# Show IP addresses
ip addr show                    # All interfaces
ip -br addr show                # Brief format
hostname -I                     # Just IP addresses

# Show interfaces
ip link show                    # Interface status

# Show routing
ip route show                   # Routing table
ip route | grep default         # Default gateway

# Show DNS
cat /etc/resolv.conf            # DNS servers

# Show hostname
hostname                        # Computer name
```

### Test Connectivity
```bash
# Ping
ping host                       # Basic ping (Ctrl+C to stop)
ping -c 4 host                  # Send 4 packets
ping -c 2 -W 2 host            # 2 packets, 2 sec timeout

# Trace route
traceroute host                 # Show packet path
traceroute -n host              # No DNS (faster)
mtr host                        # Continuous traceroute
```

### Check Ports
```bash
# List listening ports
ss -tuln                        # All TCP/UDP listening
sudo ss -tulnp                  # With process names

# Check specific port
sudo ss -tulnp | grep :80       # What's on port 80
sudo lsof -i :80                # Alternative

# Test if port is open
nc -zv host 80                  # Test port 80
telnet host 80                  # Alternative
```

### DNS Lookups
```bash
# Quick lookup
dig +short google.com           # Just the IP

# Detailed lookup
dig google.com                  # Full details

# Query specific DNS
dig @8.8.8.8 google.com        # Use Google DNS

# Different record types
dig google.com A                # IPv4
dig google.com MX               # Mail servers

# Simple tools
nslookup google.com             # Simple lookup
host google.com                 # Basic lookup
```

### Troubleshooting
```bash
# Quick health check
ping -c 2 127.0.0.1            # Loopback
ping -c 2 $(ip route | grep default | awk '{print $3}')  # Gateway
ping -c 2 8.8.8.8              # Internet
ping -c 2 google.com           # DNS

# Network info all at once
ip a && ip route && cat /etc/resolv.conf

# Port check
sudo ss -tulnp | grep LISTEN
```

---


## Common Scenarios & Solutions

### Scenario 1: "Can't reach website"

```bash
# Step 1: Can you reach internet?
ping -c 2 8.8.8.8
# If fails: Network problem (check gateway)
# If works: Continue...

# Step 2: Is DNS working?
ping -c 2 google.com
# If fails: DNS problem
dig +short google.com
cat /etc/resolv.conf

# Step 3: Is specific site down?
dig +short thewebsite.com
# If no answer: Site might be down
# If has answer: Try ping that IP
```

### Scenario 2: "Service won't start - address already in use"

```bash
# Find what's using the port
sudo ss -tulnp | grep :80

# Example output:
# tcp LISTEN 0 128 *:80 users:(("nginx",pid=1234))

# Options:
# 1. Stop the other service
sudo systemctl stop nginx

# 2. Change your service to use different port

# 3. Kill the process (last resort)
sudo kill 1234
```

### Scenario 3: "Slow network performance"

```bash
# Check for packet loss and high latency
mtr -r -c 20 google.com

# Look for:
# - Packet loss (Loss% column)
# - High latency (Avg column)
# - Jitter (large difference between Avg and Worst)

# Check interface errors
ip -s link show

# Check current connections
ss -s

# Monitor bandwidth (if iftop installed)
sudo iftop -i eth0
```

### Scenario 4: "Cannot resolve hostname"

```bash
# Check DNS configuration
cat /etc/resolv.conf
# Should have at least one nameserver

# If empty or wrong, add Google DNS:
echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf

# Test DNS resolution
dig +short google.com

# Check if it's cached locally
grep hostname /etc/hosts

# Flush DNS cache (systemd)
sudo systemd-resolve --flush-caches
```

---

## Next Steps
**Move to Day 16 when ready!**
