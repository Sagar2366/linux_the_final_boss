# Day 16: Security, Firewalls & Hardening

## Learning Objectives
By the end of Day 16, you will:
- Understand Linux security fundamentals and threat landscape
- Configure and manage firewalls (ufw, iptables, firewalld)
- Implement system hardening best practices
- Set up intrusion detection and prevention (fail2ban)
- Monitor security events and analyze logs
- Apply encryption and secure authentication methods
- Perform security audits and vulnerability assessments

**Estimated Time:** 1 hour

---

## Why Security & Hardening Matter

| Aspect | Importance | Real-World Impact |
|--------|------------|-------------------|
| **Data Protection** | Prevent unauthorized access to sensitive data | Avoid data breaches, comply with regulations (GDPR, HIPAA) |
| **System Integrity** | Maintain system reliability and availability | Prevent downtime, maintain business continuity |
| **Attack Prevention** | Stop malicious activities before they succeed | Reduce incident response costs, protect reputation |
| **Compliance** | Meet security standards and regulations | Avoid fines, maintain certifications (SOC2, ISO27001) |
| **Access Control** | Ensure only authorized users access resources | Prevent insider threats, maintain audit trails |
| **Network Security** | Protect against network-based attacks | Stop DDoS, prevent lateral movement in breaches |

**Essential for:** DevOps engineers, SREs, System Administrators, Security teams, Cloud engineers

---

## Sample Environment Setup

```bash
# Create test directory structure
mkdir -p ~/day16_test/{configs,logs,scripts,keys,backups}

# Create sample sensitive files
echo "database_password=super_secret_123" > ~/day16_test/configs/app.conf
echo "api_key=sk-1234567890abcdef" > ~/day16_test/configs/api.conf
echo "Important business data" > ~/day16_test/sensitive.txt

# Create test users and files for permission testing
sudo useradd -m testuser1 2>/dev/null || true
sudo useradd -m testuser2 2>/dev/null || true

# Create scripts for testing
cat > ~/day16_test/scripts/security-check.sh << 'EOF'
#!/bin/bash
echo "Security check started at $(date)"
echo "Checking for failed login attempts..."
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -5 || echo "No auth.log found"
echo "Checking open ports..."
ss -tuln | grep LISTEN | head -5
echo "Security check completed"
EOF

cat > ~/day16_test/scripts/backup-secure.sh << 'EOF'
#!/bin/bash
echo "Creating secure backup at $(date)"
tar -czf ~/day16_test/backups/secure-backup-$(date +%Y%m%d).tar.gz ~/day16_test/configs/
echo "Backup completed"
EOF

chmod +x ~/day16_test/scripts/*.sh

# Create sample log entries for testing
mkdir -p ~/day16_test/logs
cat > ~/day16_test/logs/access.log << 'EOF'
192.168.1.100 - - [16/Oct/2025:10:00:01 +0000] "GET / HTTP/1.1" 200 1234
192.168.1.101 - - [16/Oct/2025:10:00:02 +0000] "POST /login HTTP/1.1" 401 567
192.168.1.102 - - [16/Oct/2025:10:00:03 +0000] "GET /admin HTTP/1.1" 403 234
10.0.0.50 - - [16/Oct/2025:10:00:04 +0000] "GET /api/data HTTP/1.1" 200 5678
192.168.1.101 - - [16/Oct/2025:10:00:05 +0000] "POST /login HTTP/1.1" 401 567
EOF

# Verify setup
ls -la ~/day16_test/
echo "Environment setup complete!"
```

---

## Part 1: Linux Security Fundamentals

### Understanding the Threat Landscape
The threat landscape is the set of potential attackers, their motives and methods, known vulnerabilities, and common attack vectors targeting systems. Understanding it helps prioritize defenses, patching, and monitoring.

**Common Linux Security Threats:**

| Threat Type | Description | Attack Vector | Impact |
|-------------|-------------|---------------|---------|
| **Brute Force** | Repeated login attempts | SSH, web logins, FTP | Account compromise, system access |
| **Privilege Escalation** | Gaining higher permissions | Exploiting SUID, sudo misconfig | Full system compromise |
| **Malware/Rootkits** | Malicious software | Downloads, email, USB | Data theft, system control |
| **DDoS Attacks** | Overwhelming system resources | Network flooding | Service unavailability |
| **Data Breaches** | Unauthorized data access | Weak permissions, SQL injection | Data loss, compliance violations |
| **Insider Threats** | Malicious internal users | Legitimate access abuse | Data theft, sabotage |
| **Zero-day Exploits** | Unknown vulnerabilities | Unpatched software | System compromise |
| **Social Engineering** | Human manipulation | Phishing, pretexting | Credential theft, access |

### Security Principles

**The CIA Triad:**
Core security principles like Confidentiality, Integrity, Availability, Defense in Depth, and the Principle of Least Privilege guide how you design and apply controls — for example, choosing encryption for confidentiality, checksums for integrity, redundancy for availability, and layered controls for resilience.

| Principle | Definition | Implementation |
|-----------|------------|----------------|
| **Confidentiality** | Information accessible only to authorized users | Encryption, access controls, authentication |
| **Integrity** | Information remains accurate and unaltered | Checksums, digital signatures, version control |
| **Availability** | Information accessible when needed | Redundancy, backups, monitoring |

**Defense in Depth:**

```
┌─────────────────────────────────────────┐
│  Physical Security (Data Center)        │
├─────────────────────────────────────────┤
│  Network Security (Firewalls, IDS)      │
├─────────────────────────────────────────┤
│  Host Security (OS Hardening, AV)       │
├─────────────────────────────────────────┤
│  Application Security (Input validation)│
├─────────────────────────────────────────┤
│  Data Security (Encryption, Backups)    │
└─────────────────────────────────────────┘
```

### Command Reference: Security Assessment

| Command | Usage | Description | Key Options |
|---------|-------|-------------|-------------|
| **ss** | `ss [options]` | Show network connections | `-tuln` = TCP/UDP listening<br>`-p` = show processes<br>`-s` = summary |
| **netstat** | `netstat [options]` | Network statistics (legacy) | `-tuln` = TCP/UDP listening<br>`-p` = show PIDs |
| **lsof** | `lsof [options]` | List open files/connections | `-i` = network connections<br>`-p PID` = by process<br>`-u USER` = by user |
| **ps** | `ps [options]` | Show running processes | `aux` = all processes<br>`-eo` = custom format |
| **systemctl** | `systemctl [action] [service]` | Manage services | `list-units` = show services<br>`status` = service status |
| **find** | `find [path] [options]` | Find files by criteria | `-perm` = by permissions<br>`-user` = by owner<br>`-type` = file type |
| **grep** | `grep [options] pattern file` | Search text patterns | `-r` = recursive<br>`-i` = case insensitive<br>`-v` = invert match |
| **last** | `last [options]` | Show login history | `-n NUM` = last N entries<br>`-f FILE` = specific log |
| **lastb** | `lastb [options]` | Show failed login attempts | `-n NUM` = last N entries |
| **who** | `who [options]` | Show logged in users | `-a` = all info<br>`-b` = boot time |
| **w** | `w [user]` | Show user activity | Shows load, uptime, user sessions |

### Security Assessment Commands

```bash
# 1. Check running services
systemctl list-units --type=service --state=running
systemctl list-units --type=service --state=enabled

# 2. Check listening ports
ss -tuln
sudo ss -tulnp  # With process names

# 3. Check network connections
ss -tun state established
sudo lsof -i  # All network connections

# 4. Check running processes
ps aux --sort=-%cpu | head -20
ps aux --sort=-%mem | head -20

# 5. Check user sessions
who -a
w
last -n 20

# 6. Check failed login attempts
sudo lastb -n 20
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10

# 7. Check file permissions
find /etc -type f -perm -002 2>/dev/null  # World-writable files
find /home -type f -perm -4000 2>/dev/null  # SUID files

# 8. Check system information
uname -a
cat /etc/os-release
uptime
```

### Hands-On: Security Assessment

```bash
# 1. Run our security check script
~/day16_test/scripts/security-check.sh

# 2. Check what services are running
systemctl list-units --type=service --state=running | grep -E "(ssh|http|ftp|telnet|mysql|postgres)"

# 3. Check listening ports
echo "=== Listening Ports ==="
sudo ss -tulnp | grep LISTEN

# 4. Check for suspicious processes
echo "=== Top CPU Processes ==="
ps aux --sort=-%cpu | head -10

# 5. Check recent logins
echo "=== Recent Logins ==="
last -n 10

# 6. Check for world-writable files in sensitive directories
echo "=== World-Writable Files ==="
find /etc /usr/bin /usr/sbin -type f -perm -002 2>/dev/null | head -10

# 7. Check SUID/SGID files
echo "=== SUID Files ==="
find /usr/bin /usr/sbin -type f -perm -4000 2>/dev/null | head -10
```

---

## Part 2: Firewall Configuration & Management

### Understanding Firewalls

**What is a Firewall?**
A firewall is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.

**Types of Firewalls:**

| Type | Description | Use Case | Examples |
|------|-------------|----------|----------|
| **Packet Filter** | Examines packets, allows/blocks based on rules | Basic protection, high performance | iptables, netfilter |
| **Stateful** | Tracks connection state, context-aware | Most common, good security/performance balance | ufw, firewalld |
| **Application** | Inspects application layer data | Deep packet inspection, advanced threats | Proxy firewalls, WAF |
| **Next-Gen** | AI/ML-based, threat intelligence | Enterprise, advanced persistent threats | Commercial solutions |

### Command Reference: Firewall Tools

| Tool | Distribution | Complexity | Description |
|------|-------------|------------|-------------|
| **ufw** | Ubuntu/Debian | Simple | Uncomplicated Firewall - easy to use |
| **firewalld** | RHEL/CentOS/Fedora | Medium | Zone-based firewall with dynamic rules |
| **iptables** | All Linux | Advanced | Low-level netfilter interface |
| **nftables** | Modern Linux | Advanced | Replacement for iptables |

### UFW (Uncomplicated Firewall)

**UFW Commands:**

| Command | Purpose | Example |
|---------|---------|---------|
| `ufw enable` | Enable firewall | `sudo ufw enable` |
| `ufw disable` | Disable firewall | `sudo ufw disable` |
| `ufw status` | Show firewall status | `ufw status verbose` |
| `ufw allow` | Allow traffic | `ufw allow 22/tcp` |
| `ufw deny` | Block traffic | `ufw deny 23` |
| `ufw delete` | Remove rule | `ufw delete allow 80` |
| `ufw reset` | Reset to defaults | `sudo ufw reset` |
| `ufw reload` | Reload rules | `sudo ufw reload` |

**UFW Rule Syntax:**

```bash
# Basic port rules
ufw allow 22                    # Allow port 22 (any protocol)
ufw allow 22/tcp               # Allow port 22 TCP only
ufw allow 80,443/tcp           # Allow multiple ports
ufw allow 8000:8010/tcp        # Allow port range

# Service-based rules
ufw allow ssh                  # Allow SSH service
ufw allow http                 # Allow HTTP service
ufw allow https                # Allow HTTPS service

# IP-based rules
ufw allow from 192.168.1.100   # Allow from specific IP
ufw allow from 192.168.1.0/24  # Allow from subnet
ufw deny from 10.0.0.50        # Block specific IP

# Advanced rules
ufw allow from 192.168.1.0/24 to any port 22  # SSH from local network only
ufw allow out 53               # Allow outgoing DNS
ufw deny out 25                # Block outgoing SMTP
```

### Hands-On: UFW Configuration

```bash
# 1. Check UFW status
sudo ufw status verbose

# 2. If not installed, install UFW (Ubuntu/Debian)
# sudo apt update && sudo apt install ufw

# 3. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 4. Allow essential services
sudo ufw allow ssh              # Allow SSH (port 22)
sudo ufw allow 80/tcp          # Allow HTTP
sudo ufw allow 443/tcp         # Allow HTTPS

# 5. Allow from specific networks
sudo ufw allow from 192.168.1.0/24 to any port 22  # SSH from local network only

# 6. Enable the firewall
sudo ufw enable

# 7. Check status
sudo ufw status numbered

# 8. Test a rule (allow temporary service)
sudo ufw allow 8080/tcp
curl -I http://localhost:8080 2>/dev/null || echo "Service not running on 8080"

# 9. Remove the test rule
sudo ufw delete allow 8080/tcp

# 10. View logs (if logging enabled)
sudo ufw logging on
sudo tail -f /var/log/ufw.log &
# Stop with: sudo pkill tail
```

### Iptables (Advanced)

**Iptables Concepts:**

| Concept | Description | Example |
|---------|-------------|---------|
| **Tables** | Different rule categories | filter, nat, mangle, raw |
| **Chains** | Rule sequences | INPUT, OUTPUT, FORWARD |
| **Targets** | Actions for packets | ACCEPT, DROP, REJECT, LOG |
| **Matches** | Packet criteria | -p tcp, --dport 80, -s IP |

**Common Iptables Commands:**

```bash
# View rules
iptables -L -n                 # List all rules (numeric)
iptables -L INPUT -n --line-numbers  # Numbered INPUT rules
iptables -t nat -L -n          # NAT table rules

# Basic rules
iptables -A INPUT -p tcp --dport 22 -j ACCEPT     # Allow SSH
iptables -A INPUT -p tcp --dport 80 -j ACCEPT     # Allow HTTP
iptables -A INPUT -j DROP                         # Drop everything else

# Source-based rules
iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT    # Allow from subnet
iptables -A INPUT -s 10.0.0.50 -j DROP           # Block specific IP

# State-based rules (stateful firewall)
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -m state --state NEW -p tcp --dport 22 -j ACCEPT

# Save rules (varies by distribution)
iptables-save > /etc/iptables/rules.v4           # Debian/Ubuntu
service iptables save                             # RHEL/CentOS
```

### Hands-On: Basic Iptables

```bash
# 1. View current rules
sudo iptables -L -n

# 2. Create a backup of current rules
sudo iptables-save > ~/day16_test/backups/iptables-backup.rules

# 3. Allow loopback traffic (essential)
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

# 4. Allow established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 5. Allow SSH (be careful not to lock yourself out!)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 6. Allow HTTP and HTTPS
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 7. Log dropped packets (optional)
sudo iptables -A INPUT -j LOG --log-prefix "DROPPED: "

# 8. Drop everything else
sudo iptables -A INPUT -j DROP

# 9. View the rules
sudo iptables -L -n --line-numbers

# 10. Test connectivity (in another terminal)
# ssh localhost  # Should work
# telnet localhost 23  # Should fail/timeout

# 11. To restore original rules (if needed)
# sudo iptables-restore < ~/day16_test/backups/iptables-backup.rules
```

### Firewalld (RHEL/CentOS/Fedora)

**Firewalld Concepts:**

| Concept | Description | Example |
|---------|-------------|---------|
| **Zones** | Network trust levels | public, internal, dmz, trusted |
| **Services** | Predefined service rules | ssh, http, https, mysql |
| **Rich Rules** | Complex rule definitions | Allow specific IP to specific port |
| **Runtime vs Permanent** | Temporary vs persistent rules | --permanent flag |

**Common Firewalld Commands:**

```bash
# Zone management
firewall-cmd --get-default-zone
firewall-cmd --list-all-zones
firewall-cmd --set-default-zone=public

# Service management
firewall-cmd --list-services
firewall-cmd --add-service=http --permanent
firewall-cmd --remove-service=dhcpv6-client --permanent

# Port management
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --remove-port=8080/tcp --permanent

# IP management
firewall-cmd --add-source=192.168.1.0/24 --zone=internal --permanent
firewall-cmd --remove-source=10.0.0.50 --permanent

# Apply changes
firewall-cmd --reload
```

---

## Part 3: System Hardening
System hardening is the process of reducing an operating system or application's attack surface by applying configuration, policy, and code controls so the system is more secure and resilient. It includes removing or disabling unnecessary services, applying secure configuration baselines, tightening file and network permissions, enforcing strong authentication, patching, encrypting sensitive data, and enabling auditing and monitoring.

### Command Reference: System Hardening

| Command | Purpose | Example |
|---------|---------|---------|
| `chmod` | Change file permissions | `chmod 600 sensitive_file` |
| `chown` | Change file ownership | `chown user:group file` |
| `umask` | Set default permissions | `umask 027` |
| `chage` | Manage password aging | `chage -M 90 username` |
| `passwd` | Change passwords | `passwd -l username` (lock) |
| `usermod` | Modify user accounts | `usermod -L username` (lock) |
| `systemctl` | Manage services | `systemctl disable telnet` |
| `update-alternatives` | Manage alternatives | `update-alternatives --config editor` |

### File Permissions & Ownership

**Understanding Linux Permissions:**

```
-rwxrw-r--  1 user group 1234 Oct 16 10:00 filename
 ↓↓↓↓↓↓↓↓↓
 ||||||||└─ Other permissions (read)
 |||||||└── Other permissions (write) - MISSING
 ||||||└─── Other permissions (execute) - MISSING
 |||||└──── Group permissions (read)
 ||||└───── Group permissions (write)
 |||└────── Group permissions (execute) - MISSING
 ||└─────── Owner permissions (read)
 |└──────── Owner permissions (write)
 └───────── Owner permissions (execute)
```

**Permission Values:**

| Permission | Numeric | Symbolic | Meaning |
|------------|---------|----------|---------|
| Read | 4 | r | View file contents / List directory |
| Write | 2 | w | Modify file / Create/delete in directory |
| Execute | 1 | x | Run file / Enter directory |

**Common Permission Patterns:**

| Permissions | Numeric | Use Case |
|-------------|---------|----------|
| `-rw-------` | 600 | Private files (SSH keys, passwords) |
| `-rw-r--r--` | 644 | Public readable files (configs, docs) |
| `-rwx------` | 700 | Private executables (user scripts) |
| `-rwxr-xr-x` | 755 | Public executables (system binaries) |
| `drwx------` | 700 | Private directories (user home) |
| `drwxr-xr-x` | 755 | Public directories |

### Secure File Permissions

```bash
# 1. Find world-writable files (security risk)
find /etc /usr/bin /usr/sbin -type f -perm -002 2>/dev/null

# 2. Find files with no owner (orphaned files)
find /home -nouser -o -nogroup 2>/dev/null

# 3. Find SUID/SGID files (potential privilege escalation)
find /usr/bin /usr/sbin -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null

# 4. Secure sensitive files
chmod 600 ~/day16_test/configs/app.conf
chmod 600 ~/day16_test/configs/api.conf
chmod 600 ~/day16_test/sensitive.txt

# 5. Secure directories
chmod 700 ~/day16_test/configs
chmod 700 ~/day16_test/keys

# 6. Set restrictive umask (new files created with secure permissions)
umask 027  # New files: 640, New directories: 750

# 7. Verify permissions
ls -la ~/day16_test/configs/
ls -la ~/day16_test/
```

### User Account Security

**Password Policies:**

```bash
# 1. View password aging info
chage -l $USER

# 2. Set password aging (requires root)
sudo chage -M 90 -m 7 -W 14 testuser1  # Max 90 days, min 7 days, warn 14 days before

# 3. Force password change on next login
sudo chage -d 0 testuser1

# 4. Lock user account
sudo usermod -L testuser2
# Or: sudo passwd -l testuser2

# 5. Unlock user account
sudo usermod -U testuser2
# Or: sudo passwd -u testuser2

# 6. Set account expiration
sudo chage -E 2025-12-31 testuser1

# 7. View locked accounts
sudo passwd -S testuser1
sudo passwd -S testuser2
```

**Sudo Configuration:**

```bash
# 1. View sudo configuration
sudo cat /etc/sudoers

# 2. Edit sudoers safely
sudo visudo

# 3. Common sudoers entries:
# Allow user to run specific commands:
# username ALL=(ALL) /usr/bin/systemctl restart nginx
# 
# Allow group to run commands without password:
# %admin ALL=(ALL) NOPASSWD: /usr/bin/apt update, /usr/bin/apt upgrade
#
# Restrict to specific hosts:
# username webserver=(ALL) /usr/bin/systemctl restart apache2

# 4. Check sudo access
sudo -l

# 5. View sudo logs
grep sudo /var/log/auth.log | tail -10
```

### Service Hardening

```bash
# 1. List all enabled services
systemctl list-unit-files --state=enabled

# 2. List running services
systemctl list-units --type=service --state=running

# 3. Disable unnecessary services
sudo systemctl disable telnet 2>/dev/null || echo "telnet not installed"
sudo systemctl disable rsh 2>/dev/null || echo "rsh not installed"
sudo systemctl disable rlogin 2>/dev/null || echo "rlogin not installed"

# 4. Stop and disable if running
sudo systemctl stop telnet 2>/dev/null || true
sudo systemctl stop rsh 2>/dev/null || true

# 5. Check for insecure services
systemctl list-units --type=service --state=running | grep -E "(telnet|rsh|rlogin|ftp)"

# 6. Secure SSH configuration (view only - don't modify)
grep -E "^(PermitRootLogin|PasswordAuthentication|Port)" /etc/ssh/sshd_config 2>/dev/null || echo "SSH config not accessible"
```

### Hands-On: System Hardening

```bash
# 1. Create a hardening checklist script
cat > ~/day16_test/scripts/hardening-check.sh << 'EOF'
#!/bin/bash
echo "=== SYSTEM HARDENING CHECKLIST ==="
echo ""

echo "1. Checking file permissions..."
echo "World-writable files in /etc:"
find /etc -type f -perm -002 2>/dev/null | head -5
echo ""

echo "2. Checking SUID files..."
echo "SUID files in /usr/bin:"
find /usr/bin -type f -perm -4000 2>/dev/null | head -5
echo ""

echo "3. Checking running services..."
echo "Active services:"
systemctl list-units --type=service --state=running | grep -v "systemd" | head -10
echo ""

echo "4. Checking listening ports..."
echo "Listening ports:"
ss -tuln | grep LISTEN | head -10
echo ""

echo "5. Checking user accounts..."
echo "User accounts:"
cut -d: -f1,3 /etc/passwd | grep -E ":[0-9]{4}:" | head -5
echo ""

echo "6. Checking password aging..."
if command -v chage >/dev/null; then
    echo "Password aging for current user:"
    chage -l $USER 2>/dev/null | head -5
else
    echo "chage command not available"
fi
echo ""

echo "=== HARDENING CHECK COMPLETE ==="
EOF

chmod +x ~/day16_test/scripts/hardening-check.sh

# 2. Run the hardening check
~/day16_test/scripts/hardening-check.sh

# 3. Secure our test files
echo "Securing test files..."
chmod 600 ~/day16_test/configs/*
chmod 700 ~/day16_test/configs
chmod 700 ~/day16_test/keys
ls -la ~/day16_test/configs/

# 4. Set secure umask
echo "Current umask: $(umask)"
umask 027
echo "New umask: $(umask)"

# 5. Test file creation with new umask
touch ~/day16_test/test-file
ls -la ~/day16_test/test-file
rm ~/day16_test/test-file

# 6. Check for unnecessary packages (example)
echo "Checking for potentially unnecessary packages..."
dpkg -l | grep -E "(telnet|rsh|ftp)" 2>/dev/null || echo "No insecure packages found"
```

---

## Part 4: Intrusion Detection & Prevention

### Command Reference: Security Monitoring

| Tool | Purpose | Installation | Key Commands |
|------|---------|-------------|--------------|
| **fail2ban** | Intrusion prevention | `apt install fail2ban` | `fail2ban-client status` |
| **auditd** | System call auditing | `apt install auditd` | `auditctl -l` |
| **rkhunter** | Rootkit detection | `apt install rkhunter` | `rkhunter --check` |
| **chkrootkit** | Rootkit scanner | `apt install chkrootkit` | `chkrootkit` |
| **lynis** | Security auditing | `apt install lynis` | `lynis audit system` |

### Fail2ban - Intrusion Prevention

**What is Fail2ban?**
Fail2ban monitors log files and automatically bans IP addresses that show malicious behavior (like repeated failed login attempts).

**Fail2ban Configuration:**

```bash
# 1. Install fail2ban (Ubuntu/Debian)
sudo apt update
sudo apt install fail2ban -y

# 2. Check status
sudo systemctl status fail2ban

# 3. View default configuration
sudo cat /etc/fail2ban/jail.conf | head -20

# 4. Create local configuration (don't edit jail.conf directly)
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# 5. Basic jail.local configuration
sudo tee /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
# Ban time in seconds (10 minutes)
bantime = 600

# Find time window in seconds (10 minutes)
findtime = 600

# Number of failures before ban
maxretry = 3

# Ignore local IPs
ignoreip = 127.0.0.1/8 ::1 192.168.1.0/24

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
EOF

# 6. Restart fail2ban
sudo systemctl restart fail2ban

# 7. Check jail status
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

**Fail2ban Commands:**

```bash
# Status commands
fail2ban-client status                    # List active jails
fail2ban-client status sshd              # SSH jail details
fail2ban-client status apache-auth       # Apache jail details

# Ban management
fail2ban-client set sshd banip 192.168.1.100    # Manual ban
fail2ban-client set sshd unbanip 192.168.1.100  # Manual unban
fail2ban-client get sshd banned                  # List banned IPs

# Configuration
fail2ban-client get sshd maxretry        # Get max retry count
fail2ban-client set sshd maxretry 5      # Set max retry count
```

### Log Analysis for Security

**Important Security Logs:**

| Log File | Purpose | Key Patterns |
|----------|---------|--------------|
| `/var/log/auth.log` | Authentication events | Failed password, sudo usage |
| `/var/log/syslog` | System messages | Service failures, errors |
| `/var/log/secure` | Security events (RHEL) | SSH, sudo, authentication |
| `/var/log/messages` | General system (RHEL) | System events, errors |
| `/var/log/apache2/access.log` | Web access | HTTP requests, IPs |
| `/var/log/nginx/access.log` | Nginx access | HTTP requests, status codes |

**Security Log Analysis Commands:**

```bash
# 1. Failed SSH login attempts
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10

# 2. Successful SSH logins
grep "Accepted password" /var/log/auth.log 2>/dev/null | tail -10

# 3. Sudo usage
grep "sudo:" /var/log/auth.log 2>/dev/null | tail -10

# 4. Root login attempts
grep "root" /var/log/auth.log 2>/dev/null | grep -i "failed" | tail -5

# 5. Analyze IP addresses from failed logins
grep "Failed password" /var/log/auth.log 2>/dev/null | awk '{print $11}' | sort | uniq -c | sort -rn | head -10

# 6. Check for privilege escalation attempts
grep -i "su:" /var/log/auth.log 2>/dev/null | tail -10

# 7. Monitor real-time authentication events
sudo tail -f /var/log/auth.log | grep --line-buffered -E "(Failed|Accepted|sudo)"
```

### Hands-On: Security Monitoring

```bash
# 1. Create a security monitoring script
cat > ~/day16_test/scripts/security-monitor.sh << 'EOF'
#!/bin/bash
echo "=== SECURITY MONITORING REPORT ==="
echo "Generated at: $(date)"
echo ""

echo "1. FAILED LOGIN ATTEMPTS (Last 10):"
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10 | awk '{print $1, $2, $3, $11}' || echo "No auth.log available"
echo ""

echo "2. TOP ATTACKING IPs:"
grep "Failed password" /var/log/auth.log 2>/dev/null | awk '{print $11}' | sort | uniq -c | sort -rn | head -5 || echo "No failed attempts found"
echo ""

echo "3. SUCCESSFUL LOGINS (Last 5):"
grep "Accepted password" /var/log/auth.log 2>/dev/null | tail -5 | awk '{print $1, $2, $3, $9, $11}' || echo "No successful logins found"
echo ""

echo "4. SUDO USAGE (Last 5):"
grep "sudo:" /var/log/auth.log 2>/dev/null | tail -5 | awk '{print $1, $2, $3, $5, $6}' || echo "No sudo usage found"
echo ""

echo "5. LISTENING PORTS:"
ss -tuln | grep LISTEN | head -10
echo ""

echo "6. ACTIVE CONNECTIONS:"
ss -tun state established | head -10
echo ""

echo "7. SYSTEM LOAD:"
uptime
echo ""

echo "=== END REPORT ==="
EOF

chmod +x ~/day16_test/scripts/security-monitor.sh

# 2. Run security monitoring
~/day16_test/scripts/security-monitor.sh

# 3. Simulate some log analysis with our test logs
echo "Analyzing test access logs..."
echo "Top IPs in access log:"
awk '{print $1}' ~/day16_test/logs/access.log | sort | uniq -c | sort -rn

echo "HTTP status codes:"
awk '{print $9}' ~/day16_test/logs/access.log | sort | uniq -c | sort -rn

echo "Failed requests (4xx, 5xx):"
awk '$9 >= 400 {print $1, $7, $9}' ~/day16_test/logs/access.log

# 4. Create a simple intrusion detection script
cat > ~/day16_test/scripts/simple-ids.sh << 'EOF'
#!/bin/bash
# Simple Intrusion Detection Script

THRESHOLD=5
LOGFILE="/var/log/auth.log"
ALERT_FILE="~/day16_test/logs/security-alerts.log"

echo "Checking for brute force attacks..."

if [ -f "$LOGFILE" ]; then
    # Check for IPs with more than THRESHOLD failed attempts
    grep "Failed password" "$LOGFILE" | awk '{print $11}' | sort | uniq -c | while read count ip; do
        if [ "$count" -gt "$THRESHOLD" ]; then
            echo "$(date): ALERT - IP $ip has $count failed login attempts" | tee -a "$ALERT_FILE"
        fi
    done
else
    echo "Auth log not available for analysis"
fi

echo "IDS check complete"
EOF

chmod +x ~/day16_test/scripts/simple-ids.sh

# 5. Run the simple IDS
~/day16_test/scripts/simple-ids.sh
```

---

## Part 5: Encryption & Secure Communication

### Command Reference: Encryption Tools

| Tool | Purpose | Common Usage |
|------|---------|--------------|
| **gpg** | File encryption/signing | `gpg -c file.txt` |
| **openssl** | SSL/TLS operations | `openssl enc -aes256 -in file -out file.enc` |
| **ssh-keygen** | SSH key generation | `ssh-keygen -t rsa -b 4096` |
| **age** | Modern encryption | `age -r recipient file.txt` |

### GPG Encryption

**GPG (GNU Privacy Guard) Basics:**

```bash
# 1. Generate GPG key pair
gpg --gen-key
# Follow prompts: name, email, passphrase

# 2. List keys
gpg --list-keys
gpg --list-secret-keys

# 3. Encrypt file with passphrase (symmetric)
gpg -c ~/day16_test/sensitive.txt
# Creates sensitive.txt.gpg

# 4. Decrypt file
gpg ~/day16_test/sensitive.txt.gpg
# Enter passphrase

# 5. Encrypt for specific recipient (asymmetric)
gpg -e -r "recipient@example.com" ~/day16_test/sensitive.txt

# 6. Sign file
gpg --sign ~/day16_test/sensitive.txt

# 7. Verify signature
gpg --verify ~/day16_test/sensitive.txt.gpg
```

### SSH Key Authentication

**SSH Key Management:**

```bash
# 1. Generate SSH key pair
ssh-keygen -t rsa -b 4096 -f ~/day16_test/keys/test_key -C "test@example.com"
# Don't use passphrase for testing (press Enter)

# 2. View public key
cat ~/day16_test/keys/test_key.pub

# 3. View private key (be careful!)
head -5 ~/day16_test/keys/test_key

# 4. Set correct permissions
chmod 600 ~/day16_test/keys/test_key
chmod 644 ~/day16_test/keys/test_key.pub

# 5. Copy public key to authorized_keys (for testing)
mkdir -p ~/.ssh
cat ~/day16_test/keys/test_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 6. Test SSH key authentication
ssh -i ~/day16_test/keys/test_key localhost whoami
```

### File Encryption Examples

```bash
# 1. Encrypt sensitive configuration
echo "database_password=super_secret_123" > ~/day16_test/configs/db.conf
gpg -c ~/day16_test/configs/db.conf
rm ~/day16_test/configs/db.conf  # Remove plaintext
ls -la ~/day16_test/configs/

# 2. Decrypt when needed
gpg -d ~/day16_test/configs/db.conf.gpg

# 3. OpenSSL encryption (alternative)
echo "api_key=sk-1234567890abcdef" | openssl enc -aes256 -base64 -out ~/day16_test/configs/api.enc
# Enter password when prompted

# 4. OpenSSL decryption
openssl enc -aes256 -d -base64 -in ~/day16_test/configs/api.enc

# 5. Create encrypted backup
tar -czf - ~/day16_test/configs/ | gpg -c > ~/day16_test/backups/configs-encrypted.tar.gz.gpg

# 6. Restore encrypted backup
gpg -d ~/day16_test/backups/configs-encrypted.tar.gz.gpg | tar -xzf - -C /tmp/
ls -la /tmp/home/*/day16_test/configs/ 2>/dev/null || echo "Backup test complete"
```

---

## Sample Exercises

### Exercise 1: Configure Basic Firewall
**Task:** Set up UFW to allow only SSH, HTTP, and HTTPS traffic, blocking everything else.

**Solution:**
```bash
# 1. Check current status
sudo ufw status

# 2. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. Allow essential services
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# 4. Enable firewall
sudo ufw enable

# 5. Verify configuration
sudo ufw status verbose

# 6. Test rules
sudo ufw status numbered
```

### Exercise 2: Implement Password Policies
**Task:** Configure password aging and complexity requirements for user accounts.

**Solution:**
```bash
# 1. View current password aging
chage -l $USER

# 2. Set password aging for test user (requires root)
sudo chage -M 90 -m 7 -W 14 testuser1

# 3. Force password change on next login
sudo chage -d 0 testuser1

# 4. View updated settings
sudo chage -l testuser1

# 5. Check password status
sudo passwd -S testuser1
```

### Exercise 3: Set Up Fail2ban for SSH Protection
**Task:** Configure fail2ban to protect SSH from brute force attacks.

**Solution:**
```bash
# 1. Install fail2ban
sudo apt update && sudo apt install fail2ban -y

# 2. Create local configuration
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# 3. Configure SSH jail
sudo tee -a /etc/fail2ban/jail.local << 'EOF'

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
EOF

# 4. Restart fail2ban
sudo systemctl restart fail2ban

# 5. Check status
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

### Exercise 4: Secure File Permissions
**Task:** Find and fix insecure file permissions in the test environment.

**Solution:**
```bash
# 1. Find world-writable files
find ~/day16_test -type f -perm -002 2>/dev/null

# 2. Find files with overly permissive permissions
find ~/day16_test -type f -perm -044 2>/dev/null

# 3. Secure sensitive files
chmod 600 ~/day16_test/configs/*
chmod 600 ~/day16_test/sensitive.txt

# 4. Secure directories
chmod 700 ~/day16_test/configs
chmod 700 ~/day16_test/keys

# 5. Verify permissions
ls -la ~/day16_test/
ls -la ~/day16_test/configs/
```

### Exercise 5: Encrypt Sensitive Data
**Task:** Encrypt configuration files containing sensitive information.

**Solution:**
```bash
# 1. Create test sensitive file
echo "database_password=super_secret_123" > ~/day16_test/sensitive-config.txt

# 2. Encrypt with GPG
gpg -c ~/day16_test/sensitive-config.txt

# 3. Remove plaintext
rm ~/day16_test/sensitive-config.txt

# 4. Verify encryption
ls -la ~/day16_test/sensitive-config.txt*

# 5. Test decryption
gpg -d ~/day16_test/sensitive-config.txt.gpg

# 6. Encrypt entire directory
tar -czf - ~/day16_test/configs/ | gpg -c > ~/day16_test/backups/encrypted-configs.tar.gz.gpg
```

### Exercise 6: Security Audit and Monitoring
**Task:** Perform a comprehensive security audit of the system.

**Solution:**
```bash
# 1. Create comprehensive audit script
cat > ~/day16_test/scripts/security-audit.sh << 'EOF'
#!/bin/bash
echo "=== COMPREHENSIVE SECURITY AUDIT ==="
echo "Date: $(date)"
echo ""

echo "1. SYSTEM INFORMATION:"
echo "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "Kernel: $(uname -r)"
echo "Uptime: $(uptime -p)"
echo ""

echo "2. USER ACCOUNTS:"
echo "Total users: $(wc -l < /etc/passwd)"
echo "Users with UID 0 (root privileges):"
awk -F: '$3 == 0 {print $1}' /etc/passwd
echo ""

echo "3. LISTENING SERVICES:"
ss -tuln | grep LISTEN | wc -l | xargs echo "Listening ports:"
ss -tuln | grep LISTEN | head -10
echo ""

echo "4. FIREWALL STATUS:"
if command -v ufw >/dev/null; then
    echo "UFW Status:"
    sudo ufw status 2>/dev/null || echo "UFW not configured"
elif command -v firewall-cmd >/dev/null; then
    echo "Firewalld Status:"
    firewall-cmd --state 2>/dev/null || echo "Firewalld not running"
else
    echo "No firewall management tool found"
fi
echo ""

echo "5. FAILED LOGIN ATTEMPTS (Last 24 hours):"
if [ -f /var/log/auth.log ]; then
    grep "Failed password" /var/log/auth.log | grep "$(date +%b\ %d)" | wc -l | xargs echo "Failed attempts today:"
    grep "Failed password" /var/log/auth.log | tail -5
else
    echo "Auth log not available"
fi
echo ""

echo "6. WORLD-WRITABLE FILES:"
find /etc /usr/bin /usr/sbin -type f -perm -002 2>/dev/null | head -5
echo ""

echo "7. SUID/SGID FILES:"
find /usr/bin /usr/sbin -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null | wc -l | xargs echo "SUID/SGID files found:"
echo ""

echo "8. DISK USAGE:"
df -h | grep -E "(/$|/home|/var)"
echo ""

echo "=== AUDIT COMPLETE ==="
EOF

chmod +x ~/day16_test/scripts/security-audit.sh

# 2. Run the audit
~/day16_test/scripts/security-audit.sh

# 3. Save audit results
~/day16_test/scripts/security-audit.sh > ~/day16_test/logs/security-audit-$(date +%Y%m%d).log

# 4. Review audit log
cat ~/day16_test/logs/security-audit-$(date +%Y%m%d).log
```

---

## Sample Interview Questions

| # | Question | Difficulty | Focus Area |
|---|----------|------------|------------|
| 1 | How do you secure SSH access on a Linux server? | Intermediate | SSH Security |
| 2 | What's the difference between UFW and iptables? | Basic | Firewall Tools |
| 3 | How do you implement the principle of least privilege? | Intermediate | Access Control |
| 4 | What is fail2ban and how does it work? | Intermediate | Intrusion Prevention |
| 5 | How do you encrypt files on Linux? | Basic | Encryption |
| 6 | What are SUID files and why are they a security concern? | Advanced | File Permissions |
| 7 | How do you monitor for security incidents? | Intermediate | Security Monitoring |
| 8 | What's the difference between symmetric and asymmetric encryption? | Intermediate | Cryptography |
| 9 | How do you perform a security audit on Linux? | Advanced | Security Assessment |
| 10 | What are the key components of defense in depth? | Advanced | Security Strategy |

---

## Interview Question Answers

| Question | Answer | Example |
|----------|--------|---------|
| **1. SSH Security** | **Key methods:** Use SSH keys instead of passwords, disable root login, change default port, use fail2ban, configure firewall rules, enable 2FA if possible<br>**Config changes:** `PermitRootLogin no`, `PasswordAuthentication no`, `Port 2222` | Edit `/etc/ssh/sshd_config`:<br>`PermitRootLogin no`<br>`PasswordAuthentication no`<br>`AllowUsers specificuser`<br>Then: `systemctl restart sshd` |
| **2. UFW vs iptables** | **UFW:** Simple, user-friendly frontend for iptables. Good for basic rules, easy syntax<br>**iptables:** Low-level, powerful, complex. Direct netfilter interface, fine-grained control<br>**UFW uses iptables** underneath | **UFW:** `ufw allow 22/tcp`<br>**iptables:** `iptables -A INPUT -p tcp --dport 22 -j ACCEPT`<br>UFW is easier, iptables is more flexible |
| **3. Least Privilege** | **Principle:** Grant minimum permissions necessary for function<br>**Implementation:** Use sudo instead of root, specific command permissions, role-based access, regular permission audits<br>**File level:** Restrictive permissions (600, 700) | **User:** `usermod -G webadmin john` (specific group)<br>**Sudo:** `john ALL=(ALL) /usr/bin/systemctl restart nginx`<br>**Files:** `chmod 600 sensitive.conf` |
| **4. fail2ban** | **Purpose:** Monitors logs for malicious patterns, automatically bans IPs<br>**How:** Reads log files, counts failures, adds iptables rules to block IPs<br>**Components:** Jails (rules), filters (patterns), actions (ban methods) | **Config:** `/etc/fail2ban/jail.local`<br>**SSH jail:** monitors auth.log, bans after 3 failed attempts<br>**Commands:** `fail2ban-client status sshd` |
| **5. File Encryption** | **GPG:** `gpg -c file.txt` (symmetric), `gpg -e -r user file.txt` (asymmetric)<br>**OpenSSL:** `openssl enc -aes256 -in file -out file.enc`<br>**Full disk:** LUKS/dm-crypt for disk encryption | **GPG:** `gpg -c secrets.txt` → creates secrets.txt.gpg<br>**Decrypt:** `gpg secrets.txt.gpg`<br>**Backup:** `tar czf - data/ | gpg -c > backup.tar.gz.gpg` |
| **6. SUID Files** | **SUID:** Set User ID bit allows file to run with owner's privileges<br>**Security risk:** If compromised, attacker gains owner privileges<br>**Common:** passwd, sudo, ping<br>**Find:** `find / -perm -4000 -type f 2>/dev/null` | **Example:** `/usr/bin/passwd` has SUID root<br>**Risk:** If passwd has vulnerability, attacker gets root<br>**Audit:** Regularly check for new/unexpected SUID files |
| **7. Security Monitoring** | **Log analysis:** Monitor auth.log, syslog for suspicious activity<br>**Tools:** fail2ban, auditd, SIEM systems<br>**Metrics:** Failed logins, privilege escalation, unusual processes<br>**Automation:** Scripts, alerts, dashboards | **Commands:** `grep "Failed password" /var/log/auth.log`<br>**Real-time:** `tail -f /var/log/auth.log | grep Failed`<br>**Tools:** fail2ban, OSSEC, ELK stack |
| **8. Encryption Types** | **Symmetric:** Same key for encrypt/decrypt. Fast, good for large data<br>**Asymmetric:** Key pair (public/private). Slower, good for key exchange<br>**Hybrid:** Use asymmetric to exchange symmetric keys | **Symmetric:** AES, used for file encryption<br>**Asymmetric:** RSA, used for SSH keys, SSL certificates<br>**Example:** HTTPS uses both (RSA for handshake, AES for data) |
| **9. Security Audit** | **Steps:** Inventory systems, check configurations, scan vulnerabilities, review logs, test controls<br>**Tools:** Lynis, OpenVAS, Nessus<br>**Areas:** Users, permissions, services, network, patches | **Manual:** `lynis audit system`<br>**Network:** `nmap -sS target`<br>**Permissions:** `find / -perm -002 -type f`<br>**Services:** `systemctl list-units --state=running` |
| **10. Defense in Depth** | **Layers:** Physical, network, host, application, data<br>**Principle:** Multiple security controls, if one fails others protect<br>**Components:** Firewalls, IDS/IPS, antivirus, encryption, access controls | **Network:** Firewall + IDS<br>**Host:** Antivirus + hardening<br>**Application:** Input validation + authentication<br>**Data:** Encryption + backups |

---

## Completion Checklist

**Use this to verify your Day 16 mastery:**

### Security Fundamentals
- [ ] Understand common Linux security threats and attack vectors
- [ ] Know the CIA triad (Confidentiality, Integrity, Availability)
- [ ] Can perform basic security assessment with ss, ps, systemctl
- [ ] Understand defense in depth strategy
- [ ] Can identify security risks in system configuration

### Firewall Management
- [ ] Can configure UFW for basic firewall rules
- [ ] Understand iptables concepts (tables, chains, targets)
- [ ] Can create and manage firewall rules for common services
- [ ] Know how to allow/deny traffic by IP, port, and service
- [ ] Can troubleshoot firewall connectivity issues

### System Hardening
- [ ] Can secure file permissions with chmod/chown
- [ ] Understand SUID/SGID files and their security implications
- [ ] Can implement password policies with chage
- [ ] Know how to disable unnecessary services
- [ ] Can configure secure umask settings
- [ ] Understand sudo configuration and best practices

### Intrusion Detection & Prevention
- [ ] Can install and configure fail2ban
- [ ] Know how to analyze security logs (/var/log/auth.log)
- [ ] Can identify failed login attempts and attack patterns
- [ ] Understand how to monitor system for suspicious activity
- [ ] Can create basic security monitoring scripts

### Encryption & Authentication
- [ ] Can encrypt files with GPG (symmetric and asymmetric)
- [ ] Know how to generate and manage SSH keys
- [ ] Understand the difference between symmetric and asymmetric encryption
- [ ] Can create encrypted backups
- [ ] Know how to secure SSH configuration

### Security Monitoring & Auditing
- [ ] Can analyze log files for security events
- [ ] Know how to identify brute force attacks
- [ ] Can perform basic vulnerability assessment
- [ ] Understand how to create security audit scripts
- [ ] Can monitor system for unauthorized changes

---

## Command Quick Reference Card

### Security Assessment
```bash
# System overview
systemctl list-units --type=service --state=running
ss -tuln                           # Listening ports
ps aux --sort=-%cpu | head -10     # Top processes
last -n 20                         # Recent logins
who -a                             # Current users

# Security checks
find /etc -type f -perm -002 2>/dev/null        # World-writable files
find /usr/bin -type f -perm -4000 2>/dev/null   # SUID files
grep "Failed password" /var/log/auth.log | tail -10  # Failed logins
```

### Firewall Management
```bash
# UFW (Ubuntu/Debian)
sudo ufw enable                    # Enable firewall
sudo ufw allow 22/tcp             # Allow SSH
sudo ufw deny 23                  # Deny telnet
sudo ufw status verbose           # Show rules
sudo ufw delete allow 80          # Remove rule

# iptables (Advanced)
sudo iptables -L -n               # List rules
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT  # Allow HTTP
sudo iptables-save > rules.backup # Save rules
```

### System Hardening
```bash
# File permissions
chmod 600 sensitive_file          # Owner read/write only
chmod 700 private_directory       # Owner full access only
find /home -type f -perm -002     # Find world-writable files

# User management
sudo chage -M 90 -m 7 -W 14 user  # Password aging
sudo usermod -L username          # Lock account
sudo passwd -S username           # Check password status

# Service management
systemctl disable telnet          # Disable service
systemctl list-unit-files --state=enabled  # List enabled services
```

### Security Monitoring
```bash
# Log analysis
grep "Failed password" /var/log/auth.log | tail -10
grep "sudo:" /var/log/auth.log | tail -10
journalctl -u ssh --since "1 hour ago"

# fail2ban
sudo fail2ban-client status       # List jails
sudo fail2ban-client status sshd  # SSH jail status
sudo fail2ban-client set sshd unbanip IP  # Unban IP
```

### Encryption
```bash
# GPG encryption
gpg -c file.txt                   # Encrypt with passphrase
gpg file.txt.gpg                  # Decrypt file
gpg -e -r user@example.com file   # Encrypt for recipient

# SSH keys
ssh-keygen -t rsa -b 4096         # Generate key pair
ssh-copy-id user@server           # Copy public key
chmod 600 ~/.ssh/id_rsa           # Secure private key
```

---

## Best Practices Summary

### Security Hardening Checklist
- [ ] Keep system and packages updated
- [ ] Use strong, unique passwords with aging policies
- [ ] Implement principle of least privilege
- [ ] Disable unnecessary services and ports
- [ ] Configure firewall with default deny policy
- [ ] Use SSH keys instead of passwords
- [ ] Enable fail2ban for intrusion prevention
- [ ] Encrypt sensitive data at rest
- [ ] Monitor logs for suspicious activity
- [ ] Regular security audits and vulnerability scans
- [ ] Backup configurations and test recovery
- [ ] Document security policies and procedures

### Common Security Mistakes to Avoid
- [ ] Running services as root unnecessarily
- [ ] Using default passwords or weak authentication
- [ ] Leaving unnecessary ports open
- [ ] Not monitoring security logs
- [ ] Ignoring security updates
- [ ] Overly permissive file permissions
- [ ] Not backing up security configurations
- [ ] Disabling security features for convenience
- [ ] Not testing security controls
- [ ] Lack of incident response planning

---

## Next Steps
Proceed to [Day 17: Package Management](../Day_17/notes_and_exercises.md) to learn software installation and management.
