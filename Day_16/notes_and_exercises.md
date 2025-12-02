# Day 16: Security, Firewalls & Hardening

## Overview
**Estimated Time:** 1 hour

Master Linux security fundamentals, firewall configuration, system hardening, and intrusion prevention to protect systems from threats and maintain compliance with security standards.

### Why Security Matters
Security isn't optional—it's essential for protecting data, maintaining system integrity, preventing costly breaches, and meeting regulatory requirements (GDPR, HIPAA, SOC2).

---

## Quick Start: Test Environment Setup

```bash
# Create test environment
mkdir -p ~/security-lab/{configs,logs,scripts,keys,backups}

# Create sample sensitive files
cat > ~/security-lab/configs/app.conf << 'EOF'
database_password=super_secret_123
api_key=sk-1234567890abcdef
EOF

# Create security check script
cat > ~/security-lab/scripts/quick-check.sh << 'EOF'
#!/bin/bash
echo "=== Quick Security Check ==="
echo "Listening ports:"; ss -tuln | grep LISTEN | head -5
echo "Recent failed logins:"; grep "Failed password" /var/log/auth.log 2>/dev/null | tail -3 || echo "No auth.log access"
echo "Running services:"; systemctl list-units --type=service --state=running | wc -l | xargs echo "Active services:"
EOF

chmod +x ~/security-lab/scripts/quick-check.sh
~/security-lab/scripts/quick-check.sh
```

---

## Part 1: Security Fundamentals

### The Threat Landscape

**Common Threats:**

| Threat | Attack Vector | Impact | Mitigation |
|--------|---------------|---------|------------|
| **Brute Force** | Repeated login attempts | Account compromise | fail2ban, strong passwords, key auth |
| **Privilege Escalation** | SUID exploits, sudo misconfig | Full system control | Least privilege, audit SUID files |
| **Malware/Rootkits** | Downloads, compromised packages | Data theft, backdoors | Verify signatures, use trusted repos |
| **DDoS** | Network flooding | Service unavailability | Rate limiting, firewall rules |
| **Data Breach** | Weak permissions, injection | Data loss, fines | Encryption, access controls |
| **Insider Threats** | Legitimate access abuse | Data theft, sabotage | Audit logs, least privilege |

### Security Principles: CIA Triad

```
┌─────────────────────────────────────────┐
│  CONFIDENTIALITY                        │
│  → Encryption, access controls, auth   │
├─────────────────────────────────────────┤
│  INTEGRITY                              │
│  → Checksums, signatures, version ctrl │
├─────────────────────────────────────────┤
│  AVAILABILITY                           │
│  → Redundancy, backups, monitoring     │
└─────────────────────────────────────────┘
```

### Essential Security Assessment Commands

```bash
# System Overview
systemctl list-units --type=service --state=running    # Running services
ss -tuln                                                # Listening ports
ps aux --sort=-%cpu | head -10                         # Top CPU processes
df -h                                                   # Disk usage

# User Activity
who -a                                                  # Current users
last -n 20                                             # Recent logins
lastb -n 10                                            # Failed logins
w                                                       # User activity

# Security Checks
find /etc -type f -perm -002 2>/dev/null               # World-writable files
find /usr/bin -type f -perm -4000 2>/dev/null          # SUID files
grep "Failed password" /var/log/auth.log | tail -10    # Failed SSH attempts

# Network Analysis
sudo ss -tulnp                                          # Listening with processes
sudo lsof -i                                           # Network connections
netstat -tuln 2>/dev/null                              # Alternative (if available)
```

### Hands-On: Security Assessment

```bash
# Create comprehensive security audit script
cat > ~/security-lab/scripts/security-audit.sh << 'EOF'
#!/bin/bash
echo "=== SECURITY AUDIT REPORT ==="
echo "Generated: $(date)"
echo ""

echo "1. SYSTEM INFO:"
echo "   OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "   Kernel: $(uname -r)"
echo "   Uptime: $(uptime -p)"
echo ""

echo "2. LISTENING PORTS (Top 10):"
ss -tuln | grep LISTEN | head -10
echo ""

echo "3. RUNNING SERVICES (Count):"
systemctl list-units --type=service --state=running | grep -c "\.service"
echo ""

echo "4. FAILED LOGIN ATTEMPTS (Last 5):"
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -5 | awk '{print $1, $2, $11}' || echo "   No auth.log access"
echo ""

echo "5. WORLD-WRITABLE FILES (First 5):"
find /etc /usr/bin -type f -perm -002 2>/dev/null | head -5 || echo "   None found"
echo ""

echo "6. SUID FILES (Count):"
find /usr/bin /usr/sbin -type f -perm -4000 2>/dev/null | wc -l | xargs echo "   SUID files:"
echo ""

echo "7. DISK USAGE:"
df -h / /home 2>/dev/null | tail -n +2
echo ""

echo "=== AUDIT COMPLETE ==="
EOF

chmod +x ~/security-lab/scripts/security-audit.sh
~/security-lab/scripts/security-audit.sh
```

---

## Part 2: Firewall Configuration

### Firewall Tools Comparison

| Tool | Distribution | Difficulty | Best For |
|------|-------------|------------|----------|
| **ufw** | Ubuntu/Debian | ⭐ Easy | Quick setup, simple rules |
| **firewalld** | RHEL/CentOS/Fedora | ⭐⭐ Medium | Zone-based management |
| **iptables** | All Linux | ⭐⭐⭐ Advanced | Fine-grained control |
| **nftables** | Modern Linux | ⭐⭐⭐ Advanced | iptables replacement |

### UFW (Uncomplicated Firewall)

**Essential UFW Commands:**

```bash
# Basic Management
sudo ufw status verbose            # Show current rules
sudo ufw enable                    # Enable firewall
sudo ufw disable                   # Disable firewall
sudo ufw reload                    # Reload rules

# Set Default Policies
sudo ufw default deny incoming     # Block incoming by default
sudo ufw default allow outgoing    # Allow outgoing by default

# Simple Rules
sudo ufw allow 22                  # Allow SSH (any protocol)
sudo ufw allow 22/tcp             # Allow SSH (TCP only)
sudo ufw allow ssh                # Allow SSH (by service name)
sudo ufw allow 80,443/tcp         # Allow HTTP and HTTPS
sudo ufw deny 23                  # Deny telnet

# Advanced Rules
sudo ufw allow from 192.168.1.0/24                           # Allow entire subnet
sudo ufw allow from 192.168.1.0/24 to any port 22           # SSH from local network
sudo ufw deny from 10.0.0.50                                 # Block specific IP
sudo ufw allow proto tcp from any to any port 8080:8090     # Port range

# Rule Management
sudo ufw status numbered          # Show numbered rules
sudo ufw delete 3                 # Delete rule number 3
sudo ufw delete allow 80          # Delete by rule definition

# Logging
sudo ufw logging on               # Enable logging
sudo ufw logging medium           # Set log level
sudo tail -f /var/log/ufw.log    # Monitor logs
```

### Complete UFW Setup Example

```bash
# 1. Check current status
sudo ufw status

# 2. Reset to defaults (if needed)
# sudo ufw --force reset

# 3. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 4. Allow essential services
sudo ufw allow ssh                # SSH (port 22)
sudo ufw allow http               # HTTP (port 80)
sudo ufw allow https              # HTTPS (port 443)

# 5. Allow from trusted network only
sudo ufw allow from 192.168.1.0/24 to any port 3306  # MySQL from local network

# 6. Rate limiting (prevent brute force)
sudo ufw limit ssh                # Rate limit SSH connections

# 7. Enable firewall
sudo ufw enable

# 8. Verify configuration
sudo ufw status numbered
```

### Iptables (Advanced)

**Iptables Concepts:**

```
Tables:  filter (default), nat, mangle, raw
Chains:  INPUT (incoming), OUTPUT (outgoing), FORWARD (routing)
Targets: ACCEPT (allow), DROP (silent block), REJECT (block with response)
```

**Common Iptables Commands:**

```bash
# View Rules
sudo iptables -L -n                              # List all rules (numeric)
sudo iptables -L INPUT -n --line-numbers        # Show INPUT chain with numbers
sudo iptables -t nat -L -n                      # Show NAT table

# Accept Established Connections (Essential!)
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow Loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow Specific Services
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT     # SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT     # HTTP
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT    # HTTPS

# Allow from Specific IP/Subnet
sudo iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -s 10.0.0.50 -j DROP

# Drop All Other Incoming
sudo iptables -A INPUT -j DROP

# Save Rules (Debian/Ubuntu)
sudo iptables-save > /etc/iptables/rules.v4

# Save Rules (RHEL/CentOS)
sudo service iptables save

# Restore Rules
sudo iptables-restore < /etc/iptables/rules.v4
```

### Firewalld (RHEL/CentOS/Fedora)

**Zone-Based Management:**

```bash
# Zone Management
firewall-cmd --get-default-zone                # Show default zone
firewall-cmd --list-all-zones                  # List all zones
firewall-cmd --set-default-zone=public         # Set default zone

# Service Management
firewall-cmd --list-services                   # List allowed services
firewall-cmd --add-service=http --permanent    # Add service
firewall-cmd --remove-service=dhcpv6-client --permanent

# Port Management
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --list-ports

# Source Management
firewall-cmd --add-source=192.168.1.0/24 --zone=internal --permanent

# Apply Changes
firewall-cmd --reload

# Rich Rules (Advanced)
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port=22 protocol=tcp accept' --permanent
```

---

## Part 3: System Hardening

### File Permissions Security

**Understanding Linux Permissions:**

```
-rwxrw-r--  1 user group size date filename
 │││││││││
 │││└┴┴┴┴┴─ Others: read only (r--)
 ││└┴┴┴──── Group: read, write (rw-)
 │└┴┴┴───── Owner: read, write, execute (rwx)
 └────────── File type: - (regular file)
```

**Permission Values:**

| Permission | Numeric | Symbolic | Meaning for Files | Meaning for Directories |
|------------|---------|----------|-------------------|-------------------------|
| Read | 4 | r | View contents | List contents |
| Write | 2 | w | Modify contents | Create/delete files |
| Execute | 1 | x | Run as program | Enter directory |

**Secure Permission Patterns:**

| Permissions | Numeric | Use Case | Example |
|-------------|---------|----------|---------|
| `-rw-------` | 600 | Private files | SSH keys, passwords |
| `-rw-r--r--` | 644 | Public readable | Config files, docs |
| `-rwx------` | 700 | Private scripts | User executables |
| `-rwxr-xr-x` | 755 | Public programs | System binaries |
| `drwx------` | 700 | Private folders | ~/.ssh directory |
| `drwxr-xr-x` | 755 | Public folders | /usr/local/bin |

### Secure File Permissions Practice

```bash
# 1. Find security vulnerabilities
echo "=== Finding Security Issues ==="

# World-writable files (dangerous!)
find /etc /usr/bin -type f -perm -002 2>/dev/null | head -5

# SUID files (potential privilege escalation)
find /usr/bin /usr/sbin -type f -perm -4000 2>/dev/null

# Files with no owner (orphaned)
find /home -nouser -o -nogroup 2>/dev/null

# 2. Secure sensitive files
echo "=== Securing Files ==="
chmod 600 ~/security-lab/configs/app.conf          # Owner read/write only
chmod 700 ~/security-lab/configs                   # Owner full access only
chmod 700 ~/security-lab/keys                      # Private key directory

# 3. Set secure umask (default permissions for new files)
umask 027                                           # New files: 640, Directories: 750
echo "umask 027" >> ~/.bashrc                      # Make permanent

# 4. Verify permissions
ls -la ~/security-lab/configs/

# 5. Create test file with new umask
touch ~/security-lab/test-file.txt
ls -l ~/security-lab/test-file.txt
rm ~/security-lab/test-file.txt
```

### User Account Security

**Password Policies:**

```bash
# View password aging information
chage -l $USER

# Set password policies (requires root)
sudo chage -M 90 -m 7 -W 14 username    # Max 90 days, min 7 days, warn 14 days
sudo chage -d 0 username                # Force password change on next login
sudo chage -E 2025-12-31 username       # Set account expiration

# Lock/Unlock accounts
sudo usermod -L username                # Lock account
sudo passwd -l username                 # Lock password
sudo usermod -U username                # Unlock account
sudo passwd -u username                 # Unlock password

# Check account status
sudo passwd -S username                 # Show password status

# View locked accounts
sudo passwd -S -a | grep " L "
```

**Sudo Configuration:**

```bash
# Edit sudoers file safely
sudo visudo

# Common sudoers patterns:
# Allow user to run specific commands:
# username ALL=(ALL) /usr/bin/systemctl restart nginx

# Allow group without password:
# %admin ALL=(ALL) NOPASSWD: /usr/bin/apt update, /usr/bin/apt upgrade

# Restrict to specific hosts:
# username webserver=(ALL) /usr/bin/systemctl restart apache2

# Check sudo access
sudo -l

# View sudo logs
grep sudo /var/log/auth.log | tail -10
```

### Service Hardening

```bash
# 1. List all enabled services
systemctl list-unit-files --state=enabled

# 2. List running services
systemctl list-units --type=service --state=running

# 3. Disable insecure services
sudo systemctl disable telnet 2>/dev/null || echo "telnet not installed (good!)"
sudo systemctl disable rsh 2>/dev/null || echo "rsh not installed (good!)"
sudo systemctl disable rlogin 2>/dev/null || echo "rlogin not installed (good!)"

# 4. Check for insecure services
systemctl list-units --type=service | grep -E "(telnet|rsh|rlogin|ftp)"

# 5. Stop unnecessary services
sudo systemctl stop bluetooth.service 2>/dev/null || true
sudo systemctl disable bluetooth.service 2>/dev/null || true

# 6. Secure SSH (view only - don't modify unless you know what you're doing)
sudo cat /etc/ssh/sshd_config | grep -E "^(PermitRootLogin|PasswordAuthentication|Port)"
```

### Hardening Checklist Script

```bash
cat > ~/security-lab/scripts/hardening-checklist.sh << 'EOF'
#!/bin/bash
echo "=== SYSTEM HARDENING CHECKLIST ==="
echo ""

# File Permissions
echo "✓ File Permission Checks:"
echo "  World-writable files: $(find /etc /usr/bin -type f -perm -002 2>/dev/null | wc -l)"
echo "  SUID files: $(find /usr/bin /usr/sbin -type f -perm -4000 2>/dev/null | wc -l)"

# Services
echo ""
echo "✓ Service Checks:"
echo "  Running services: $(systemctl list-units --type=service --state=running | grep -c "\.service")"
echo "  Enabled services: $(systemctl list-unit-files --state=enabled | grep -c "\.service")"

# Network
echo ""
echo "✓ Network Checks:"
echo "  Listening ports: $(ss -tuln | grep -c LISTEN)"
echo "  Established connections: $(ss -tun state established | grep -c ESTAB)"

# Firewall
echo ""
echo "✓ Firewall Status:"
if command -v ufw >/dev/null; then
    sudo ufw status | head -3
elif command -v firewall-cmd >/dev/null; then
    firewall-cmd --state 2>/dev/null || echo "  Firewalld not active"
else
    echo "  No firewall tool detected"
fi

# Updates
echo ""
echo "✓ System Updates:"
echo "  Kernel: $(uname -r)"
if command -v apt >/dev/null; then
    echo "  Updates available: $(apt list --upgradable 2>/dev/null | grep -c upgradable)"
elif command -v yum >/dev/null; then
    echo "  Updates available: $(yum check-update --quiet | grep -c "\..*")"
fi

echo ""
echo "=== CHECKLIST COMPLETE ==="
EOF

chmod +x ~/security-lab/scripts/hardening-checklist.sh
~/security-lab/scripts/hardening-checklist.sh
```

---

## Part 4: Intrusion Detection with fail2ban

### What is fail2ban?

fail2ban monitors log files for malicious patterns (like repeated failed logins) and automatically bans offending IP addresses by adding firewall rules.

### fail2ban Installation & Configuration

```bash
# 1. Install fail2ban (Ubuntu/Debian)
sudo apt update
sudo apt install fail2ban -y

# 2. Check status
sudo systemctl status fail2ban

# 3. Create local configuration (never edit jail.conf directly)
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# 4. Configure SSH protection
sudo tee /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
# Ban time in seconds (1 hour)
bantime = 3600

# Time window to count failures (10 minutes)
findtime = 600

# Number of failures before ban
maxretry = 3

# Ignore local networks
ignoreip = 127.0.0.1/8 ::1 192.168.1.0/24

# Email notifications (optional)
# destemail = admin@example.com
# sendername = Fail2Ban
# action = %(action_mwl)s

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
EOF

# 5. Restart fail2ban
sudo systemctl restart fail2ban

# 6. Enable on boot
sudo systemctl enable fail2ban

# 7. Check status
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

### fail2ban Management Commands

```bash
# Status and Information
sudo fail2ban-client status                      # List all jails
sudo fail2ban-client status sshd                # SSH jail details
sudo fail2ban-client get sshd banned            # List banned IPs

# Manual Ban/Unban
sudo fail2ban-client set sshd banip 10.0.0.50   # Manually ban IP
sudo fail2ban-client set sshd unbanip 10.0.0.50 # Unban IP

# Configuration
sudo fail2ban-client get sshd maxretry          # Get max retry
sudo fail2ban-client set sshd maxretry 5        # Set max retry

# Logs
sudo tail -f /var/log/fail2ban.log              # Monitor fail2ban log
sudo journalctl -u fail2ban -f                  # Systemd journal
```

### Additional fail2ban Jails

```bash
# Add Apache/Nginx protection
sudo tee -a /etc/fail2ban/jail.local << 'EOF'

[apache-auth]
enabled = true
port = http,https
filter = apache-auth
logpath = /var/log/apache2/error.log
maxretry = 3

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 3
EOF

sudo systemctl restart fail2ban
```

---

## Part 5: Security Monitoring & Log Analysis

### Important Security Logs

| Log File | Purpose | Key Events |
|----------|---------|------------|
| `/var/log/auth.log` | Authentication (Debian/Ubuntu) | SSH, sudo, user logins |
| `/var/log/secure` | Authentication (RHEL/CentOS) | SSH, sudo, user logins |
| `/var/log/syslog` | System messages | Service events, errors |
| `/var/log/kern.log` | Kernel messages | Hardware, driver events |
| `/var/log/fail2ban.log` | fail2ban activity | Bans, unbans |
| `/var/log/ufw.log` | Firewall events | Blocked connections |

### Essential Log Analysis Commands

```bash
# SSH Login Analysis
grep "Accepted password" /var/log/auth.log | tail -10              # Successful logins
grep "Failed password" /var/log/auth.log | tail -10                # Failed attempts
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn  # Top attacking IPs

# Sudo Usage
grep "sudo:" /var/log/auth.log | tail -10                          # Sudo commands
grep "sudo:" /var/log/auth.log | grep "COMMAND" | tail -5          # Recent sudo commands

# User Account Changes
grep "useradd\|userdel\|usermod" /var/log/auth.log | tail -10     # User modifications
grep "passwd" /var/log/auth.log | tail -10                         # Password changes

# Root Login Attempts
grep "root" /var/log/auth.log | grep "Failed" | tail -10          # Failed root logins

# Real-time Monitoring
sudo tail -f /var/log/auth.log                                     # Live authentication log
sudo tail -f /var/log/auth.log | grep --line-buffered "Failed"   # Live failed attempts

# Systemd Journal (Alternative)
journalctl -u ssh --since "1 hour ago"                            # SSH logs last hour
journalctl -p err -n 50                                           # Last 50 errors
journalctl -f                                                     # Follow journal
```

### Security Monitoring Script

```bash
cat > ~/security-lab/scripts/monitor-security.sh << 'EOF'
#!/bin/bash
echo "=== SECURITY MONITORING REPORT ==="
echo "Report Time: $(date)"
echo ""

# Failed Login Attempts
echo "1. FAILED LOGIN ATTEMPTS (Last 10):"
if [ -f /var/log/auth.log ]; then
    grep "Failed password" /var/log/auth.log | tail -10 | awk '{print $1, $2, $3, $9, $11}' || echo "   No failed attempts"
else
    echo "   Auth log not available"
fi
echo ""

# Top Attacking IPs
echo "2. TOP ATTACKING IPs:"
if [ -f /var/log/auth.log ]; then
    grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -5 || echo "   No attacks detected"
else
    echo "   Auth log not available"
fi
echo ""

# Successful Logins
echo "3. SUCCESSFUL LOGINS (Last 5):"
if [ -f /var/log/auth.log ]; then
    grep "Accepted password" /var/log/auth.log | tail -5 | awk '{print $1, $2, $3, $9, "from", $11}' || echo "   No successful logins"
else
    echo "   Auth log not available"
fi
echo ""

# Sudo Usage
echo "4. SUDO USAGE (Last 5):"
if [ -f /var/log/auth.log ]; then
    grep "sudo:" /var/log/auth.log | grep "COMMAND" | tail -5 | awk '{print $1, $2, $5, $6}' || echo "   No sudo usage"
else
    echo "   Auth log not available"
fi
echo ""

# Current Connections
echo "5. ACTIVE SSH CONNECTIONS:"
who | grep -v "^$" || echo "   No active connections"
echo ""

# fail2ban Status
echo "6. FAIL2BAN STATUS:"
if command -v fail2ban-client >/dev/null 2>&1; then
    sudo fail2ban-client status sshd 2>/dev/null || echo "   fail2ban not running"
else
    echo "   fail2ban not installed"
fi
echo ""

echo "=== REPORT COMPLETE ==="
EOF

chmod +x ~/security-lab/scripts/monitor-security.sh
~/security-lab/scripts/monitor-security.sh
```

---

## Part 6: Encryption & Secure Data

### GPG (GNU Privacy Guard)

**File Encryption:**

```bash
# 1. Symmetric encryption (password-based)
gpg -c ~/security-lab/configs/app.conf
# Enter passphrase when prompted
# Creates app.conf.gpg

# 2. Decrypt file
gpg -d ~/security-lab/configs/app.conf.gpg
# Or decrypt to file:
gpg -o decrypted.conf -d ~/security-lab/configs/app.conf.gpg

# 3. Generate key pair (for asymmetric encryption)
gpg --gen-key
# Follow prompts: name, email, passphrase

# 4. List keys
gpg --list-keys                    # Public keys
gpg --list-secret-keys            # Private keys

# 5. Encrypt for specific recipient
gpg -e -r "email@example.com" file.txt

# 6. Encrypt and sign
gpg -se -r "email@example.com" file.txt

# 7. Decrypt
gpg -d file.txt.gpg
```

**Encrypted Backups:**

```bash
# Create encrypted backup
tar czf - ~/security-lab/configs/ | gpg -c > ~/security-lab/backups/configs-backup.tar.gz.gpg

# Restore encrypted backup
gpg -d ~/security-lab/backups/configs-backup.tar.gz.gpg | tar xzf - -C /tmp/
```

### SSH Key Authentication

**Generate and Use SSH Keys:**

```bash
# 1. Generate SSH key pair (4096-bit RSA)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_secure -C "your_email@example.com"
# Enter strong passphrase

# 2. Generate ED25519 key (modern, recommended)
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "your_email@example.com"

# 3. View public key
cat ~/.ssh/id_rsa_secure.pub

# 4. Copy public key to server
ssh-copy-id -i ~/.ssh/id_rsa_secure.pub user@server

# 5. Manual copy (if ssh-copy-id not available)
cat ~/.ssh/id_rsa_secure.pub | ssh user@server 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'

# 6. Set correct permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa_secure
chmod 644 ~/.ssh/id_rsa_secure.pub
chmod 600 ~/.ssh/authorized_keys

# 7. Test SSH key authentication
ssh -i ~/.ssh/id_rsa_secure user@server

# 8. Configure SSH client (~/.ssh/config)
cat >> ~/.ssh/config << 'EOF'
Host myserver
    HostName server.example.com
    User username
    Port 22
    IdentityFile ~/.ssh/id_rsa_secure
EOF

# 9. Disable password authentication (on server /etc/ssh/sshd_config)
# PasswordAuthentication no
# PubkeyAuthentication yes
# Then: sudo systemctl restart sshd
```

### OpenSSL Encryption

```bash
# Encrypt file with AES-256
openssl enc -aes-256-cbc -salt -in file.txt -out file.enc
# Enter password

# Decrypt file
openssl enc -aes-256-cbc -d -in file.enc -out file.txt

# Encrypt with base64 encoding
echo "secret data" | openssl enc -aes-256-cbc -a -salt -out secret.enc

# Decrypt base64
openssl enc -aes-256-cbc -d -a -in secret.enc
```

---

## Practical Exercises

### Exercise 1: Complete Firewall Setup

**Task:** Configure UFW to secure a web server allowing only necessary ports.

```bash
# 1. Reset UFW to start fresh
sudo ufw --force reset

# 2. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. Allow SSH (with rate limiting)
sudo ufw limit ssh comment 'SSH with rate limiting'

# 4. Allow HTTP and HTTPS
sudo ufw allow http comment 'HTTP traffic'
sudo ufw allow https comment 'HTTPS traffic'

# 5. Allow from internal network to database
sudo ufw allow from 192.168.1.0/24 to any port 3306 comment 'MySQL from internal network'

# 6. Enable logging
sudo ufw logging medium

# 7. Enable firewall
sudo ufw enable

# 8. Verify configuration
sudo ufw status verbose
sudo ufw status numbered

# 9. Test (in another terminal)
# curl http://localhost
# telnet localhost 23  # Should fail
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
