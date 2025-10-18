# Day 14: System Monitoring & Log Management

## Table of Contents

- [Day 14: System Monitoring & Log Management](#day-14-system-monitoring-&-log-management)
  - [Learning Objectives](#learning-objectives)
  - [Notes](#notes)
  - [Sample Exercises](#sample-exercises)
  - [Solutions](#solutions)
  - [Sample Interview Questions](#sample-interview-questions)
  - [Interview Question Answers](#interview-question-answers)
  - [Completion Checklist](#completion-checklist)
  - [Key Commands Summary](#key-commands-summary)
- [System monitoring](#system-monitoring)
- [Log management](#log-management)
  - [Best Practices](#best-practices)
  - [Next Steps](#next-steps)


## Learning Objectives
By the end of Day 14, you will:
- Monitor system resources (CPU, memory, disk, network) in real-time
- Understand and interpret system load and performance metrics
- Locate, read, and analyze log files effectively
- Set up automated log rotation and cleanup
- Troubleshoot performance issues using monitoring tools
- Implement monitoring best practices

**Estimated Time:** 1 hour

---

## Why Monitoring & Logs Matter

| Aspect | Importance | Real-World Impact |
|--------|------------|-------------------|
| **Proactive Monitoring** | Catch issues before users notice | Prevents outages, maintains uptime SLAs |
| **Performance Optimization** | Identify bottlenecks early | Better resource utilization, cost savings |
| **Troubleshooting** | Quick root cause analysis | Reduced MTTR (Mean Time To Repair) |
| **Security** | Detect intrusions and anomalies | Early threat detection, audit trails |
| **Capacity Planning** | Track growth trends | Plan hardware upgrades before crisis |
| **Compliance** | Maintain audit logs | Meet regulatory requirements (HIPAA, PCI-DSS) |

**Key for:** DevOps engineers, SREs, System Administrators, Security teams

---

## Sample Environment Setup

```bash
# Create test directory structure
mkdir -p ~/day14_test/{logs,scripts,data}

# Create test log file with sample data
cat > ~/day14_test/logs/app.log << 'EOF'
2025-10-16 10:00:01 INFO Application started successfully
2025-10-16 10:00:15 INFO User login: john@example.com
2025-10-16 10:01:23 WARNING Database connection slow (2.5s)
2025-10-16 10:02:45 ERROR Failed to connect to API: timeout
2025-10-16 10:03:12 INFO Processing batch job: 1000 items
2025-10-16 10:05:33 ERROR Out of memory: killed process
2025-10-16 10:06:01 INFO Application restarted
2025-10-16 10:07:22 WARNING High CPU usage detected (95%)
EOF

# Create script that generates load for testing
cat > ~/day14_test/scripts/generate-load.sh << 'EOF'
#!/bin/bash
# Generates CPU load for testing monitoring
echo "Generating CPU load for 30 seconds..."
timeout 30 yes > /dev/null &
timeout 30 yes > /dev/null &
echo "Load generation started. Monitor with: top or htop"
EOF

chmod +x ~/day14_test/scripts/generate-load.sh

# Create script that generates logs
cat > ~/day14_test/scripts/generate-logs.sh << 'EOF'
#!/bin/bash
# Generates sample log entries
LOG_FILE=~/day14_test/logs/test.log
for i in {1..10}; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Test log entry $i" >> $LOG_FILE
    sleep 1
done
echo "Generated 10 log entries in $LOG_FILE"
EOF

chmod +x ~/day14_test/scripts/generate-logs.sh

# Verify setup
ls -la ~/day14_test/scripts/
ls -la ~/day14_test/logs/
```

---

## Part 1: System Resource Monitoring

### Command Reference: Monitoring Tools

| Command | Usage | Description | Key Options |
|---------|-------|-------------|-------------|
| **top** | `top [options]` | Real-time process viewer | `-d SEC` = update delay<br>`-p PID` = monitor specific process<br>`-u USER` = user's processes |
| **htop** | `htop` | Enhanced interactive monitor | F3=search, F6=sort, F9=kill, F10=quit |
| **free** | `free [options]` | Memory usage statistics | `-h` = human-readable<br>`-s SEC` = continuous updates<br>`-t` = show total |
| **uptime** | `uptime` | System uptime and load average | Shows 1, 5, 15 minute load averages |
| **w** | `w` | Who is logged in and what they're doing | Shows users, login time, load |
| **vmstat** | `vmstat [interval] [count]` | Virtual memory statistics | `vmstat 2 5` = 2 sec interval, 5 times |
| **iostat** | `iostat [options] [interval]` | CPU and I/O statistics | `-x` = extended stats<br>`-c` = CPU only<br>`-d` = disk only |
| **df** | `df [options]` | Disk space usage | `-h` = human-readable<br>`-T` = show filesystem type<br>`-i` = inode usage |
| **du** | `du [options] [path]` | Directory space usage | `-h` = human-readable<br>`-s` = summary<br>`--max-depth=N` = depth limit |
| **mpstat** | `mpstat [interval] [count]` | Per-CPU statistics | `-P ALL` = all CPUs |
| **sar** | `sar [options] [interval] [count]` | System activity report | `-u` = CPU<br>`-r` = memory<br>`-d` = disk |
| **dstat** | `dstat [options]` | Versatile resource statistics | `--cpu --mem --disk --net` |
| **watch** | `watch [options] command` | Execute command repeatedly | `-n SEC` = interval<br>`-d` = highlight differences |

### Understanding System Load

**Load Average** = Number of processes waiting for CPU time (averaged over 1, 5, 15 minutes)

```bash
uptime
# Output: 10:30:45 up 5 days, 3:22, 2 users, load average: 0.52, 0.68, 0.71
#                                                           1min  5min  15min
```

| Load per CPU | Interpretation | Action |
|--------------|----------------|--------|
| **< 0.7** | Healthy | No action needed |
| **0.7 - 1.0** | Busy but OK | Monitor closely |
| **1.0 - 1.5** | Getting stressed | Investigate causes |
| **> 1.5** | Overloaded | Immediate action required |

**Example:** 4-core system with load of 3.0 = 75% utilized (3.0 / 4 cores)

### Memory Understanding

```bash
free -h
#               total        used        free      shared  buff/cache   available
# Mem:           15Gi       8.2Gi       1.1Gi       123Mi       6.1Gi       7.8Gi
# Swap:         2.0Gi       512Mi       1.5Gi
```

| Metric | Description | What to Watch |
|--------|-------------|---------------|
| **total** | Total physical RAM | Fixed (hardware) |
| **used** | RAM used by processes | High is normal (Linux caches aggressively) |
| **free** | Completely unused RAM | Low is OK if available is high |
| **shared** | RAM used by tmpfs/shared memory | Usually small |
| **buff/cache** | Used for disk caching | Released when needed (good!) |
| **available** | RAM available for new apps | **Most important metric** |
| **swap used** | Using disk as RAM | **High swap = performance issue** |

**⚠️ Warning Signs:**
- **Available < 10% of total** = Need more RAM or reduce usage
- **Swap usage > 50%** = System is thrashing (very slow)
- **OOM killer messages** in logs = Out of memory, processes killed

### Disk Monitoring

```bash
df -h
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        50G   35G   12G  75% /
# /dev/sdb1       200G  150G   40G  79% /data
```

**Thresholds:**
- **< 80%** = Healthy
- **80-90%** = Monitor and plan cleanup
- **> 90%** = Critical - take action now
- **100%** = System may fail, services crash

```bash
# Find large files
du -h /var/log | sort -rh | head -10

# Find what's using space
du -sh /var/* | sort -rh

# Find large files modified recently
find /var/log -type f -size +100M -mtime -7
```

### CPU Monitoring

**In `top` / `htop`:**

| Metric | Description | Healthy Range |
|--------|-------------|---------------|
| **us (user)** | Time running user processes | Varies by workload |
| **sy (system)** | Time running kernel code | < 30% typically |
| **ni (nice)** | Time running low-priority processes | Varies |
| **id (idle)** | CPU doing nothing | Higher = less busy |
| **wa (iowait)** | Waiting for I/O (disk/network) | **< 10% is good, > 30% = I/O bottleneck** |
| **hi (hardware interrupts)** | Handling hardware interrupts | < 5% typically |
| **si (software interrupts)** | Handling software interrupts | < 5% typically |
| **st (steal)** | VM only: time stolen by host | < 10% (VM performance) |

### Hands-On: Basic Monitoring

```bash
# 1. Check system load and uptime
uptime
w

# 2. Memory overview
free -h
# Watch memory in real-time
watch -n 2 free -h

# 3. CPU usage - top view
top
# Inside top:
# - Press '1' to see per-CPU breakdown
# - Press 'P' to sort by CPU usage
# - Press 'M' to sort by memory usage
# - Press 'q' to quit

# 4. Or use htop (more user-friendly)
htop
# Use arrow keys to navigate
# Press F3 to search for process
# Press F6 to sort by different columns
# Press F9 to kill a process
# Press F10 or 'q' to quit

# 5. Disk space check
df -h
df -h /          # Check root filesystem only
df -h /home      # Check home filesystem

# 6. Check disk usage by directory
du -sh /var/log/*
du -h /var/log | sort -rh | head -10

# 7. Generate load for testing
~/day14_test/scripts/generate-load.sh
# In another terminal, monitor:
top
# You should see high CPU usage

# 8. Monitor virtual memory stats
vmstat 2 5
# Updates every 2 seconds, 5 times
# Look at:
# - r: processes waiting for CPU
# - free: free memory
# - si/so: swap in/out (should be low)
# - us/sy/id/wa: CPU percentages

# 9. I/O statistics (install if needed: apt install sysstat)
iostat -x 2
# Look at:
# - %util: device utilization (< 80% is good)
# - await: average wait time (< 20ms is good)
```

### Advanced Monitoring

```bash
# 1. Per-CPU statistics
mpstat -P ALL 2 5
# Shows each CPU core usage separately

# 2. System activity reporter (comprehensive)
sar -u 2 5      # CPU usage
sar -r 2 5      # Memory usage
sar -d 2 5      # Disk usage

# 3. Versatile tool (install: apt install dstat)
dstat --cpu --mem --disk --net 2
# Shows everything in one view

# 4. Watch command for custom monitoring
watch -n 1 'uptime && free -h && df -h /'
# Updates every second

# 5. Find top memory consumers
ps aux --sort=-%mem | head -10

# 6. Find top CPU consumers
ps aux --sort=-%cpu | head -10
```

---

## Part 2: Log Management

### Understanding Linux Logs

**Log System Architecture:**

| Component | Description | Used By |
|-----------|-------------|---------|
| **rsyslog** | Traditional logging daemon | Older systems, custom apps |
| **systemd-journald** | Modern systemd logging | systemd services (most current distros) |
| **Application logs** | App-specific logging | Apache, MySQL, custom apps |

### Command Reference: Log Tools

| Command | Usage | Description | Key Options |
|---------|-------|-------------|-------------|
| **journalctl** | `journalctl [options]` | Query systemd journal logs | `-f` = follow (live)<br>`-u SERVICE` = specific service<br>`-p LEVEL` = priority level<br>`--since/--until` = time range |
| **tail** | `tail [options] FILE` | View end of file | `-f` = follow (live)<br>`-n NUM` = last N lines<br>`-F` = follow with retry |
| **head** | `head [options] FILE` | View beginning of file | `-n NUM` = first N lines |
| **cat** | `cat FILE` | Display entire file | Avoid for large files! |
| **less** | `less FILE` | View file page-by-page | `/pattern` = search<br>`n` = next match<br>`q` = quit |
| **more** | `more FILE` | Simple pager | Space = next page<br>`q` = quit |
| **grep** | `grep [options] PATTERN FILE` | Search text | `-i` = case-insensitive<br>`-r` = recursive<br>`-v` = invert (exclude)<br>`-A N` = N lines after<br>`-B N` = N lines before<br>`-C N` = N lines context |
| **awk** | `awk 'PATTERN {ACTION}' FILE` | Text processing | Extract fields, calculate, filter |
| **sed** | `sed 's/find/replace/' FILE` | Stream editor | Find/replace, delete lines |
| **zgrep** | `zgrep PATTERN FILE.gz` | Search compressed files | Same options as grep |
| **zcat** | `zcat FILE.gz` | View compressed file | Displays .gz files |

### Important Log Locations

| Log File | Purpose | Contains |
|----------|---------|----------|
| **System Logs** | | |
| `/var/log/syslog` | General system messages | Ubuntu/Debian general log |
| `/var/log/messages` | General system messages | RHEL/CentOS general log |
| `/var/log/kern.log` | Kernel messages | Hardware, drivers, kernel errors |
| `/var/log/dmesg` | Boot messages | Hardware detection at boot |
| **Authentication** | | |
| `/var/log/auth.log` | Authentication logs | Ubuntu/Debian SSH, sudo, login |
| `/var/log/secure` | Authentication logs | RHEL/CentOS SSH, sudo, login |
| `/var/log/faillog` | Failed login attempts | Security monitoring |
| **Services** | | |
| `/var/log/apache2/` | Apache web server | access.log, error.log |
| `/var/log/nginx/` | Nginx web server | access.log, error.log |
| `/var/log/mysql/` | MySQL database | error.log, slow-query.log |
| `/var/log/postgresql/` | PostgreSQL database | postgresql.log |
| **Applications** | | |
| `/var/log/apt/` | Package management | Ubuntu/Debian package installs |
| `/var/log/yum.log` | Package management | RHEL/CentOS package installs |
| `/var/log/cron` | Cron job logs | Scheduled task execution |
| **System** | | |
| `/var/log/boot.log` | Boot process | System startup messages |
| `/var/log/lastlog` | Last login info | User last login times |
| `/var/log/wtmp` | Login history | Binary: use `last` command |
| `/var/log/btmp` | Failed logins | Binary: use `lastb` command |

### Log Priority Levels (syslog)

| Level | Number | Name | Description | Example |
|-------|--------|------|-------------|---------|
| **emerg** | 0 | Emergency | System is unusable | Kernel panic |
| **alert** | 1 | Alert | Action must be taken immediately | Database corruption |
| **crit** | 2 | Critical | Critical conditions | Hard drive failure |
| **err** | 3 | Error | Error conditions | Service failed to start |
| **warning** | 4 | Warning | Warning conditions | Disk 90% full |
| **notice** | 5 | Notice | Normal but significant | User logged in |
| **info** | 6 | Informational | Informational messages | Service started |
| **debug** | 7 | Debug | Debug messages | Detailed function calls |

### Using journalctl (systemd logs)

```bash
# Basic viewing
journalctl                          # All logs (oldest first)
journalctl -r                       # Reverse (newest first)
journalctl -n 50                    # Last 50 entries
journalctl -f                       # Follow (like tail -f)

# By service
journalctl -u nginx                 # Nginx logs
journalctl -u ssh                   # SSH logs
journalctl -u cron                  # Cron logs

# By priority
journalctl -p err                   # Errors only
journalctl -p warning               # Warnings and above
journalctl -p crit                  # Critical and above

# By time range
journalctl --since "2025-10-16 10:00:00"
journalctl --since "1 hour ago"
journalctl --since "yesterday"
journalctl --since "2 days ago"
journalctl --until "10 minutes ago"
journalctl --since "10:00" --until "11:00"

# Combined filters
journalctl -u nginx -p err --since "1 hour ago"
journalctl -u ssh -f                # Follow SSH logs live

# By boot
journalctl -b                       # Current boot
journalctl -b -1                    # Previous boot
journalctl --list-boots             # List all boots

# Output formats
journalctl -o json                  # JSON format
journalctl -o json-pretty           # Formatted JSON
journalctl -o verbose               # All fields

# Disk usage
journalctl --disk-usage             # Show journal disk usage
sudo journalctl --vacuum-time=7d    # Keep only 7 days
sudo journalctl --vacuum-size=500M  # Keep only 500MB
```

### Log Analysis with grep, awk, sed

```bash
# 1. Basic grep searches
grep "error" /var/log/syslog
grep -i "error" /var/log/syslog             # Case-insensitive
grep -i "error" /var/log/syslog | wc -l    # Count errors

# 2. Multiple patterns
grep -E "error|fail|warn" /var/log/syslog
grep -i "error\|fail\|warn" /var/log/syslog

# 3. Exclude patterns
grep "error" /var/log/syslog | grep -v "ignored"

# 4. Context lines
grep -A 3 "error" /var/log/syslog           # 3 lines after
grep -B 3 "error" /var/log/syslog           # 3 lines before
grep -C 3 "error" /var/log/syslog           # 3 lines before and after

# 5. Recursive search
grep -r "error" /var/log/

# 6. Search compressed logs
zgrep "error" /var/log/syslog.1.gz

# 7. AWK for column extraction
# Extract timestamp and message from log
awk '{print $1, $2, $3, $NF}' /var/log/syslog

# Count occurrences
awk '/error/ {count++} END {print count}' /var/log/syslog

# Print lines with specific field
awk '$6 == "ERROR"' ~/day14_test/logs/app.log

# 8. SED for text manipulation
# Remove lines containing pattern
sed '/debug/d' /var/log/app.log

# Replace text
sed 's/ERROR/CRITICAL/g' /var/log/app.log

# Print specific line range
sed -n '10,20p' /var/log/syslog
```

### Hands-On: Log Analysis

```bash
# 1. View system log (live)
sudo tail -f /var/log/syslog        # Ubuntu/Debian
sudo tail -f /var/log/messages      # RHEL/CentOS

# 2. View last 50 lines
sudo tail -50 /var/log/syslog

# 3. Find all errors in last hour
sudo journalctl --since "1 hour ago" -p err

# 4. Search for specific pattern
sudo grep -i "failed" /var/log/auth.log
sudo grep -i "failed" /var/log/auth.log | wc -l

# 5. Find failed SSH login attempts
sudo grep "Failed password" /var/log/auth.log
sudo grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn

# 6. Analyze test log
cat ~/day14_test/logs/app.log
grep ERROR ~/day14_test/logs/app.log
grep -c ERROR ~/day14_test/logs/app.log    # Count

# 7. Extract timestamps of errors
grep ERROR ~/day14_test/logs/app.log | awk '{print $1, $2}'

# 8. Watch for new log entries
~/day14_test/scripts/generate-logs.sh &
tail -f ~/day14_test/logs/test.log

# 9. Find all WARNING and ERROR
grep -E "WARNING|ERROR" ~/day14_test/logs/app.log

# 10. Show context around errors
grep -C 2 ERROR ~/day14_test/logs/app.log
```

---

## Part 3: Log Rotation with logrotate

### What is Log Rotation?

**Problem:** Logs grow infinitely → disk fills up → system crashes

**Solution:** logrotate automatically:
1. Compresses old logs
2. Deletes very old logs
3. Creates new empty log files
4. Maintains manageable log sizes

### Command Reference: logrotate

| Command | Usage | Description |
|---------|-------|-------------|
| **logrotate** | `sudo logrotate [options] CONFIG` | Run log rotation |
| **logrotate -d** | `sudo logrotate -d CONFIG` | Debug (dry-run, shows what would happen) |
| **logrotate -f** | `sudo logrotate -f CONFIG` | Force rotation now |
| **logrotate -v** | `sudo logrotate -v CONFIG` | Verbose output |

### logrotate Configuration

**Main config:** `/etc/logrotate.conf`
**Drop-in configs:** `/etc/logrotate.d/*` (one file per application)

**Common Directives:**

| Directive | Description | Example |
|-----------|-------------|---------|
| **daily** | Rotate daily | `daily` |
| **weekly** | Rotate weekly | `weekly` |
| **monthly** | Rotate monthly | `monthly` |
| **rotate N** | Keep N rotated logs | `rotate 7` (keep 7 days) |
| **size** | Rotate when size reached | `size 100M` |
| **compress** | Compress old logs with gzip | `compress` |
| **delaycompress** | Compress on next rotation | `delaycompress` |
| **missingok** | Don't error if log missing | `missingok` |
| **notifempty** | Don't rotate if empty | `notifempty` |
| **create MODE OWNER GROUP** | Create new log with permissions | `create 0640 www-data www-data` |
| **postrotate/endscript** | Run command after rotation | Reload service to use new log |
| **prerotate/endscript** | Run command before rotation | Stop service before rotation |
| **dateext** | Use date in filename | `app.log-20251016` |
| **maxage N** | Remove logs older than N days | `maxage 30` |

### logrotate Configuration Examples

```bash
# 1. Simple daily rotation
# /etc/logrotate.d/myapp
/var/log/myapp.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}

# 2. Weekly with size limit
/var/log/bigapp/*.log {
    weekly
    size 100M
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 0640 appuser appgroup
}

# 3. With postrotate (reload service)
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}

# 4. Size-based rotation only
/var/log/app/error.log {
    size 50M
    rotate 5
    compress
    missingok
    notifempty
    copytruncate
}

# 5. Multiple logs, one config
/var/log/app/*.log /var/log/app/*/*.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
    dateext
    dateformat -%Y%m%d
    maxage 90
}
```

### Hands-On: Log Rotation

```bash
# 1. View main logrotate config
cat /etc/logrotate.conf

# 2. View existing app configs
ls -la /etc/logrotate.d/
cat /etc/logrotate.d/apache2    # Example

# 3. Create test log that needs rotation
mkdir -p ~/day14_test/logs
for i in {1..1000}; do
    echo "$(date) Log entry $i with some text to make it bigger" >> ~/day14_test/logs/big.log
done
ls -lh ~/day14_test/logs/big.log

# 4. Create logrotate config for test log
sudo tee /etc/logrotate.d/day14test << 'EOF'
/home/$(whoami)/day14_test/logs/big.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0644 $(whoami) $(whoami)
}
EOF

# 5. Test configuration (dry-run)
sudo logrotate -d /etc/logrotate.d/day14test

# 6. Force rotation now
sudo logrotate -f /etc/logrotate.d/day14test

# 7. Verify rotation happened
ls -lh ~/day14_test/logs/
# Should see: big.log (new empty) and big.log.1.gz (compressed old)

# 8. View compressed log
zcat ~/day14_test/logs/big.log.1.gz | head

# 9. Check logrotate status
cat /var/lib/logrotate/status

# 10. Remove test config
sudo rm /etc/logrotate.d/day14test
```

---

## Part 4: Performance Troubleshooting

### Troubleshooting Methodology

```
1. Identify the symptom → What is slow/broken?
2. Check system resources → CPU, memory, disk, network
3. Find the bottleneck → Which resource is constrained?
4. Analyze logs → What errors occurred?
5. Correlate events → When did it start? What changed?
6. Fix or mitigate → Apply solution
7. Monitor → Verify fix works
```

### Common Performance Issues

| Symptom | Likely Cause | How to Diagnose | Solution |
|---------|--------------|-----------------|----------|
| **System very slow** | High CPU usage | `top`, `htop` - check %CPU | Kill/optimize high-CPU processes |
| **Applications crash** | Out of memory | `free -h`, `dmesg | grep -i kill` | Add RAM, reduce usage, fix memory leaks |
| **Disk operations slow** | High I/O wait | `iostat -x`, `iotop` - check %util, await | Optimize I/O, upgrade disk, reduce writes |
| **Network slow** | Bandwidth saturation | `iftop`, `nethogs`, `ss -s` | QoS, upgrade bandwidth, reduce traffic |
| **Login slow** | High load average | `uptime`, `w` - check load vs CPUs | Reduce processes, add CPUs |
| **Swap thrashing** | Not enough RAM | `vmstat` - high si/so, `free -h` | Add RAM, reduce memory usage |
| **Services not responding** | Resource exhaustion | `systemctl status SERVICE`, logs | Restart service, increase limits |

### Troubleshooting Commands Quick Reference

```bash
# 1. Quick health check
uptime && free -h && df -h /

# 2. Find resource hog
top -b -n 1 | head -20
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# 3. Check for OOM (Out Of Memory) kills
dmesg | grep -i "killed process"
grep -i "out of memory" /var/log/syslog

# 4. Disk I/O bottleneck
iostat -x 2 5
# Look for %util > 80%, await > 50ms

# 5. Network issues
ss -s                               # Socket summary
netstat -tuln | wc -l               # Count connections
iftop                               # Bandwidth by connection

# 6. Process details
lsof -p PID                         # Files opened by process
strace -p PID                       # System calls (debug)
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head

# 7. Check system messages for hardware errors
dmesg -T | tail -50
journalctl -p crit --since "1 hour ago"
```

### Hands-On: Performance Troubleshooting Scenario

```bash
# Scenario: System is slow, investigate

# Step 1: Check load average
uptime
# If load average > number of CPUs, system is overloaded

# Step 2: Identify CPU hogs
top
# Press 'P' to sort by CPU, look for processes using > 50%

# Or with ps:
ps aux --sort=-%cpu | head -10

# Step 3: Check memory
free -h
# If "available" < 1GB and swap is being used, memory issue

# Step 4: Check disk space
df -h
# If any filesystem > 90%, disk space problem

# Step 5: Check I/O wait
iostat -x 2
# If %iowait > 30%, disk I/O is bottleneck

# Step 6: Check for errors in logs
sudo journalctl -p err --since "1 hour ago"
sudo grep -i error /var/log/syslog | tail -20

# Step 7: Check specific service
systemctl status nginx
sudo journalctl -u nginx -n 50

# Step 8: If process is the problem
# Option A: Kill it
sudo kill PID
# Option B: Reduce priority
sudo renice 10 -p PID
```

---

## Sample Exercises

### Exercise 1: Real-Time Monitoring
**Task:** Monitor CPU, memory, and disk usage in real-time.

**Solution:**
```bash
# Option 1: htop (best for interactive)
htop

# Option 2: top (standard)
top

# Option 3: Custom dashboard with watch
watch -n 2 'echo "=== SYSTEM STATUS ===" && uptime && echo "" && free -h && echo "" && df -h /'

# Option 4: Continuous vmstat
vmstat 2

# Option 5: dstat (if installed)
dstat --cpu --mem --disk --net 2
```

### Exercise 2: Find Top Memory Consumers
**Task:** Identify the top 5 processes consuming the most memory.

**Solution:**
```bash
# Method 1: Using ps
ps aux --sort=-%mem | head -6
# First line is header, next 5 are top processes

# Method 2: With custom formatting
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -6

# Method 3: Using top
top -b -n 1 -o %MEM | head -12

# Method 4: Show only what matters
ps aux --sort=-%mem | awk 'NR<=6{printf "%-8s %-8s %-6s %s\n", $2, $11, $4"%", $12}'

# Method 5: In htop
htop
# Press F6, select MEM%, press Enter
# Top 5 will be at the top
```

### Exercise 3: Monitor Directory Growth
**Task:** Watch disk usage of a directory grow in real-time.

**Solution:**
```bash
# Create directory and generate data
mkdir -p ~/day14_test/data

# Method 1: Watch df (filesystem level)
watch -n 2 'df -h | grep -E "Filesystem|/$"'

# Method 2: Watch du (directory level)
watch -n 1 'du -sh ~/day14_test/data'

# Method 3: Watch with detailed view
watch -n 2 'du -sh ~/day14_test/data/* | sort -h'

# Generate growth (in another terminal)
for i in {1..100}; do
    dd if=/dev/zero of=~/day14_test/data/file$i.dat bs=1M count=10 2>/dev/null
    sleep 1
done

# Method 4: Continuous monitoring with timestamp
while true; do
    echo "$(date '+%H:%M:%S') - $(du -sh ~/day14_test/data | cut -f1)"
    sleep 2
done
```

### Exercise 4: Log Analysis for Errors
**Task:** View and filter system logs to find all errors in the last hour.

**Solution:**
```bash
# Method 1: Using journalctl (systemd)
sudo journalctl --since "1 hour ago" -p err

# Method 2: More specific - last 30 minutes, errors and critical
sudo journalctl --since "30 minutes ago" -p err -p crit

# Method 3: Traditional syslog
sudo grep -i error /var/log/syslog | grep "$(date '+%b %e')"

# Method 4: Count errors by type
sudo journalctl --since "1 hour ago" -p err | grep -oP '\w+\[\d+\]' | sort | uniq -c | sort -rn

# Method 5: Specific service errors
sudo journalctl -u nginx --since "1 hour ago" -p warning

# Method 6: Search test log
grep ERROR ~/day14_test/logs/app.log
grep -E "ERROR|WARNING" ~/day14_test/logs/app.log

# Method 7: With context (2 lines before and after)
grep -C 2 ERROR ~/day14_test/logs/app.log

# Method 8: Extract just timestamps and messages
grep ERROR ~/day14_test/logs/app.log | awk '{print $1, $2, $4, $5, $6, $7, $8}'
```

### Exercise 5: Set Up Log Rotation
**Task:** Configure log rotation for a custom application log.

**Solution:**
```bash
# 1. Create application log with substantial content
mkdir -p ~/day14_test/app/logs
for i in {1..5000}; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Application log entry $i" >> ~/day14_test/app/logs/app.log
done

# Check size
ls -lh ~/day14_test/app/logs/app.log

# 2. Create logrotate configuration
sudo tee /etc/logrotate.d/myapp << EOF
/home/$USER/day14_test/app/logs/app.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 $USER $USER
}
EOF

# 3. Test configuration (dry-run)
sudo logrotate -d /etc/logrotate.d/myapp

# 4. Force rotation immediately
sudo logrotate -f /etc/logrotate.d/myapp

# 5. Verify rotation
ls -lh ~/day14_test/app/logs/
# Should see app.log (new) and app.log.1 (old, compressed if delay not set)

# 6. View rotated log
if [ -f ~/day14_test/app/logs/app.log.1.gz ]; then
    zcat ~/day14_test/app/logs/app.log.1.gz | head -10
else
    head -10 ~/day14_test/app/logs/app.log.1
fi

# 7. Verify new log is being used
echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] New log entry after rotation" >> ~/day14_test/app/logs/app.log
tail ~/day14_test/app/logs/app.log

# 8. Cleanup (when done testing)
sudo rm /etc/logrotate.d/myapp
rm -rf ~/day14_test/app
```

### Exercise 6: Advanced - Performance Bottleneck Investigation
**Task:** Create a performance issue, identify it, and resolve it.

**Solution:**
```bash
# 1. Create a CPU-intensive script
cat > ~/day14_test/scripts/cpu-hog.sh << 'EOF'
#!/bin/bash
# CPU-intensive loop
echo "Starting CPU hog (PID: $)"
while true; do
    echo "scale=5000; a(1)*4" | bc -l > /dev/null
done
EOF

chmod +x ~/day14_test/scripts/cpu-hog.sh

# 2. Start the problematic process
~/day14_test/scripts/cpu-hog.sh &
CPU_HOG_PID=$!
echo "Started CPU hog with PID: $CPU_HOG_PID"

# 3. Investigate - Check load
uptime
# Load should be increasing

# 4. Identify the culprit with top
top -b -n 1 | head -15
# Should see cpu-hog.sh or bc near the top

# 5. Or with ps
ps aux --sort=-%cpu | head -5
# Should show high CPU usage for bc or bash

# 6. Get detailed info
ps -p $CPU_HOG_PID -o pid,ppid,cmd,%cpu,%mem,stat

# 7. Reduce priority (temporary fix)
sudo renice 19 -p $CPU_HOG_PID
# Check priority changed
ps -eo pid,ni,cmd | grep cpu-hog

# 8. Monitor the change
top -p $CPU_HOG_PID
# CPU should still be used but process is "nicer"

# 9. Kill the process (permanent fix)
kill $CPU_HOG_PID
# Verify it's gone
ps aux | grep cpu-hog

# 10. If it doesn't die gracefully
# kill -9 $CPU_HOG_PID

# Cleanup
rm ~/day14_test/scripts/cpu-hog.sh
```

---

## Sample Interview Questions

| # | Question | Difficulty | Focus Area |
|---|----------|------------|------------|
| 1 | What tools do you use to monitor system resources? | Basic | Tools knowledge |
| 2 | How do you find and troubleshoot high CPU usage? | Intermediate | Troubleshooting |
| 3 | How do you monitor logs in real time? | Basic | Log management |
| 4 | What is log rotation and why is it important? | Basic | Concepts |
| 5 | Explain load average. What's considered healthy? | Intermediate | Metrics understanding |
| 6 | How do you check if a system is running out of memory? | Intermediate | Memory analysis |
| 7 | What's the difference between `top` and `htop`? | Basic | Tools comparison |
| 8 | How do you monitor disk I/O? | Intermediate | I/O monitoring |
| 9 | How would you centralize logs from multiple servers? | Advanced | Architecture |
| 10 | How do you set up alerts for resource usage? | Advanced | Automation |
| 11 | What's the difference between `free` and `available` memory? | Intermediate | Memory concepts |
| 12 | How do you find which process is using a specific file? | Intermediate | Process investigation |
| 13 | Explain iowait. When should you be concerned? | Advanced | Performance tuning |
| 14 | How do you analyze logs for security incidents? | Advanced | Security |
| 15 | What's your approach to troubleshooting a slow system? | Advanced | Methodology |

---

## Interview Question Answers

| Question | Answer | Example/Details |
|----------|--------|-----------------|
| **1. Monitoring Tools** | **Real-time:** `top`, `htop`, `vmstat`, `iostat`<br>**Memory:** `free`, `vmstat`<br>**Disk:** `df`, `du`, `iotop`<br>**Network:** `iftop`, `nethogs`, `ss`<br>**Comprehensive:** `sar`, `dstat`<br>**Logs:** `journalctl`, `tail -f` | `htop` for interactive use<br>`vmstat 2` for continuous monitoring<br>`iostat -x 2` for I/O performance<br>`df -h` for disk space |
| **2. High CPU Troubleshooting** | **Step 1:** Use `top`/`htop` to identify high-CPU processes<br>**Step 2:** Check with `ps aux --sort=-%cpu`<br>**Step 3:** Investigate with `strace -p PID` (system calls)<br>**Step 4:** Check logs for errors<br>**Step 5:** Reduce priority with `renice` or kill if necessary | `top` → Press 'P' to sort by CPU<br>`ps aux --sort=-%cpu | head`<br>`strace -p 1234` to see what process is doing<br>`kill PID` or `renice 10 PID` |
| **3. Real-time Logs** | **systemd:** `journalctl -f`<br>**Traditional:** `tail -f /var/log/syslog`<br>**Specific service:** `journalctl -u nginx -f`<br>**With filtering:** `tail -f /var/log/syslog | grep error`<br>**Multiple files:** `multitail /var/log/syslog /var/log/auth.log` | `sudo tail -f /var/log/syslog`<br>`sudo journalctl -f -p err`<br>`sudo journalctl -u apache2 -f` |
| **4. Log Rotation** | **Purpose:** Prevents disk space exhaustion by rotating, compressing, and deleting old logs<br>**Managed by:** `logrotate` (runs daily via cron)<br>**Config:** `/etc/logrotate.conf` and `/etc/logrotate.d/*`<br>**Common settings:** daily/weekly, rotate count, compress, size limits | Without rotation → logs grow infinitely → disk fills → system crashes<br>Example: `daily`, `rotate 7`, `compress` = keep 7 days, compressed |
| **5. Load Average** | **Definition:** Number of processes in run queue (running + waiting for CPU), averaged over 1, 5, 15 minutes<br>**Calculation:** Load / CPU cores<br>**Healthy:** < 0.7 per CPU<br>**Busy:** 0.7-1.0 per CPU<br>**Overloaded:** > 1.0 per CPU<br>**Example:** 4-core system with load 3.0 = 75% utilized (OK) | `uptime` shows: `load average: 0.52, 0.68, 0.71`<br>4-core system: < 2.8 is healthy<br>Single-core: > 1.0 = overloaded |
| **6. Memory Check** | **Check available:** `free -h` → look at "available" column<br>**Check swap:** High swap usage (> 50%) = memory pressure<br>**OOM kills:** `dmesg | grep -i "killed process"`<br>**Warning signs:** available < 10% total, swap used > 50%<br>**Processes:** `ps aux --sort=-%mem | head` | `free -h` → available < 1GB = problem<br>`vmstat 2` → si/so columns show swap activity<br>`grep -i "out of memory" /var/log/syslog` |
| **7. top vs htop** | **top:** Standard, built-in, keyboard-only, minimal interface<br>**htop:** Enhanced, colorful, mouse support, easier to use<br>**top advantages:** Always available, lower overhead<br>**htop advantages:** Better UX, easier navigation, tree view, mouse support<br>**Both show:** CPU, memory, processes, load | `top`: Press 'P' (CPU), 'M' (memory), 'k' (kill)<br>`htop`: F3 (search), F6 (sort), F9 (kill), arrow keys navigate |
| **8. Disk I/O Monitoring** | **iostat:** `iostat -x 2` → %util, await, r/s, w/s<br>**iotop:** Shows I/O by process (like top for disk)<br>**vmstat:** `vmstat 2` → bi/bo columns (blocks in/out)<br>**sar:** `sar -d 2 5` → disk statistics<br>**Metrics:** %util > 80% = busy, await > 50ms = slow | `iostat -x 2` → watch %util column<br>`sudo iotop` → see which process does I/O<br>High %iowait in `top` = I/O bottleneck |
| **9. Centralized Logging** | **Solutions:**<br>• **ELK Stack:** Elasticsearch, Logstash, Kibana<br>• **Rsyslog:** Forward logs to central server<br>• **Syslog-ng:** Advanced syslog<br>• **Fluentd/Fluent Bit:** Lightweight collectors<br>• **Graylog:** Open-source log management<br>• **Splunk:** Commercial solution | **Basic setup:** Configure rsyslog on all servers to forward to central server<br>**Modern:** Use Fluentd to collect → Elasticsearch to store → Kibana to visualize |
| **10. Resource Alerts** | **Methods:**<br>• **Monitoring tools:** Nagios, Zabbix, Prometheus + Alertmanager<br>• **Custom scripts:** Cron jobs that check metrics and send alerts<br>• **Cloud native:** CloudWatch (AWS), Azure Monitor, Google Cloud Monitoring<br>• **Thresholds:** CPU > 80%, Memory < 10% available, Disk > 90%, Load > CPU count | **Simple script:** Check `df -h`, if > 90% send email<br>**Prometheus:** Define alert rules, Alertmanager sends notifications<br>**Nagios:** NRPE plugin checks, sends alerts |
| **11. free vs available** | **free:** Completely unused RAM (small is normal)<br>**available:** RAM available for new applications (includes buff/cache that can be freed)<br>**Key:** Linux uses "free" RAM for disk caching (buff/cache)<br>**cached memory is freed automatically when needed**<br>**Available = free + reclaimable cache** | `free -h`:<br>free = 500M, available = 5G → OK!<br>Linux cached 4.5G for performance<br>If app needs 3G, Linux frees cache automatically |
| **12. Find Process Using File** | **lsof:** `lsof /path/to/file` → shows all processes<br>**fuser:** `fuser /path/to/file` → shows PIDs<br>**lsof by PID:** `lsof -p PID` → all files by process<br>**lsof by user:** `lsof -u username`<br>**Network:** `lsof -i :80` → processes on port 80 | `lsof /var/log/syslog` → which process writes to it<br>`fuser -v /var/log/syslog` → PIDs and users<br>`lsof -i :443` → what's using HTTPS port |
| **13. iowait Explanation** | **Definition:** % of time CPU is idle while waiting for I/O operations (disk/network)<br>**Normal:** < 10%<br>**Concern:** > 30% = I/O bottleneck<br>**Causes:** Slow disk, too many reads/writes, failing hardware<br>**Check with:** `top`, `vmstat`, `iostat -x` | In `top`: `%wa` column shows iowait<br>High iowait → use `iostat -x` to find busy disk<br>Then `iotop` to find which process causes I/O |
| **14. Security Log Analysis** | **Check auth logs:** Failed SSH logins, sudo usage<br>**Commands:** `grep "Failed password" /var/log/auth.log`<br>**Find IPs:** `awk '/Failed password/ {print $11}' /var/log/auth.log | sort | uniq -c | sort -rn`<br>**Successful logins:** `grep "Accepted" /var/log/auth.log`<br>**Tools:** fail2ban, OSSEC, Splunk, ELK<br>**Correlate:** Check same timeframe across multiple logs | Failed SSH: `grep "Failed password" /var/log/auth.log | wc -l`<br>Top attacking IPs: extract and count<br>Privilege escalation: `grep sudo /var/log/auth.log` |
| **15. Troubleshooting Methodology** | **1. Identify symptom:** What's slow? Error messages?<br>**2. Quick health check:** `uptime`, `free -h`, `df -h`<br>**3. Find bottleneck:** CPU? Memory? Disk? Network?<br>**4. Identify culprit:** `top`/`htop`, `ps`, `iostat`<br>**5. Check logs:** Errors, warnings, correlation<br>**6. Apply fix:** Kill process, increase resources, optimize<br>**7. Verify:** Monitor to confirm fix works | **Example:** System slow → `uptime` (load high) → `top` (find CPU hog) → `ps` (identify process) → Check logs for errors → Kill or optimize → Monitor |

---

## Completion Checklist

**Use this to verify your Day 14 mastery:**

### System Monitoring
- [ ] Can use `top` and `htop` to monitor processes in real-time
- [ ] Understand load average and what's healthy for the system
- [ ] Can check memory with `free -h` and interpret results
- [ ] Know the difference between "free" and "available" memory
- [ ] Can monitor disk space with `df -h` and set thresholds
- [ ] Can use `du` to find large directories and files
- [ ] Understand CPU metrics: user, system, iowait, idle
- [ ] Can use `vmstat` to monitor virtual memory statistics
- [ ] Can use `iostat` to monitor disk I/O performance
- [ ] Can identify resource bottlenecks (CPU, memory, disk, I/O)

### Log Management
- [ ] Know important log file locations (`/var/log/*`)
- [ ] Can use `journalctl` to query systemd logs
- [ ] Can filter logs by time, priority, and service
- [ ] Can follow logs in real-time with `tail -f` or `journalctl -f`
- [ ] Can search logs with `grep`, `awk`, and `sed`
- [ ] Can analyze logs for errors, warnings, and patterns
- [ ] Understand log priority levels (info, warning, error, critical)
- [ ] Can find failed login attempts in auth logs
- [ ] Can correlate events across multiple log files

### Log Rotation
- [ ] Understand why log rotation is necessary
- [ ] Know logrotate configuration files and locations
- [ ] Can create custom logrotate configuration
- [ ] Know common directives (daily, rotate, compress, etc.)
- [ ] Can test logrotate config with `-d` (dry-run)
- [ ] Can force rotation with `logrotate -f`
- [ ] Can use postrotate scripts to reload services
- [ ] Understand size-based vs time-based rotation

### Performance Troubleshooting
- [ ] Can identify high CPU usage and find the process
- [ ] Can detect memory exhaustion and OOM kills
- [ ] Can identify disk I/O bottlenecks with iostat
- [ ] Can check for swap thrashing with vmstat
- [ ] Know how to check disk space issues
- [ ] Can identify network connectivity problems
- [ ] Have a systematic troubleshooting methodology
- [ ] Can use `lsof` to find which process uses a file
- [ ] Can reduce process priority with `renice`
- [ ] Can kill problematic processes safely

---

## Command Quick Reference Card

### System Monitoring Commands

```bash
# Load and Uptime
uptime                              # System uptime and load average
w                                   # Who's logged in and what they're doing

# CPU Monitoring
top                                 # Real-time process viewer
htop                                # Enhanced interactive monitor
mpstat -P ALL 2                     # Per-CPU statistics
sar -u 2 5                          # CPU usage report

# Memory Monitoring
free -h                             # Memory usage (human-readable)
free -h -s 2                        # Update every 2 seconds
vmstat 2 5                          # Virtual memory stats
ps aux --sort=-%mem | head -10      # Top memory consumers

# Disk Monitoring
df -h                               # Disk space usage
df -h /var/log                      # Specific filesystem
df -i                               # Inode usage
du -sh /var/log/*                   # Directory sizes
du -h /var/log | sort -rh | head    # Largest directories
ncdu /var/log                       # Interactive disk usage (if installed)

# I/O Monitoring
iostat -x 2                         # Extended I/O statistics
iotop                               # I/O by process (needs root)
vmstat 2                            # Shows I/O in bi/bo columns
sar -d 2 5                          # Disk statistics

# Network Monitoring
ss -s                               # Socket statistics summary
ss -tuln                            # TCP/UDP listening sockets
netstat -tuln                       # Network connections (legacy)
iftop                               # Bandwidth by connection
nethogs                             # Bandwidth by process

# Process Information
ps aux                              # All processes
ps aux --sort=-%cpu | head          # Top CPU consumers
ps -eo pid,ppid,cmd,%mem,%cpu       # Custom format
pgrep -a httpd                      # Find processes by name
lsof -p PID                         # Files opened by process
lsof /path/to/file                  # Processes using file
lsof -i :80                         # Processes on port 80

# Continuous Monitoring
watch -n 2 'free -h'                # Watch memory every 2 seconds
watch -n 1 'df -h /'                # Watch disk space
dstat --cpu --mem --disk --net 2    # All-in-one stats
```

### Log Management Commands

```bash
# journalctl (systemd logs)
journalctl                          # All logs
journalctl -f                       # Follow (live)
journalctl -r                       # Reverse (newest first)
journalctl -n 50                    # Last 50 entries
journalctl -u nginx                 # Specific service
journalctl -p err                   # Errors only
journalctl --since "1 hour ago"     # Time filter
journalctl --since "2025-10-16 10:00"
journalctl --until "10 minutes ago"
journalctl -u nginx -p err --since "1 hour ago"
journalctl -b                       # Current boot
journalctl -b -1                    # Previous boot
journalctl --disk-usage             # Journal disk usage
sudo journalctl --vacuum-time=7d    # Keep 7 days only

# Traditional logs
tail -f /var/log/syslog             # Follow system log (Ubuntu/Debian)
tail -f /var/log/messages           # RHEL/CentOS
tail -50 /var/log/syslog            # Last 50 lines
tail -f /var/log/apache2/error.log  # Follow Apache errors

# Searching logs
grep "error" /var/log/syslog
grep -i "error" /var/log/syslog     # Case-insensitive
grep -E "error|fail" /var/log/syslog # Multiple patterns
grep -A 3 "error" /var/log/syslog   # 3 lines after
grep -B 3 "error" /var/log/syslog   # 3 lines before
grep -C 3 "error" /var/log/syslog   # 3 lines context
grep -r "error" /var/log/           # Recursive
zgrep "error" /var/log/syslog.1.gz  # Search compressed

# Log analysis
grep "Failed password" /var/log/auth.log
grep "Failed password" /var/log/auth.log | wc -l
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn
awk '/error/ {print $1, $2, $3}' /var/log/syslog
sed -n '100,200p' /var/log/syslog   # Lines 100-200

# View compressed logs
zcat /var/log/syslog.1.gz | less
zgrep "error" /var/log/syslog.*.gz
```

### Log Rotation Commands

```bash
# logrotate
sudo logrotate -d /etc/logrotate.conf     # Debug/dry-run
sudo logrotate -f /etc/logrotate.conf     # Force rotation
sudo logrotate -v /etc/logrotate.conf     # Verbose
sudo logrotate -d /etc/logrotate.d/nginx  # Test specific config
cat /var/lib/logrotate/status             # Check rotation status

# Configuration files
cat /etc/logrotate.conf                   # Main config
ls /etc/logrotate.d/                      # Individual configs
sudo vim /etc/logrotate.d/myapp           # Edit app config
```

### Troubleshooting Commands

```bash
# Quick health check
uptime && free -h && df -h /

# Find resource hogs
top -b -n 1 | head -20
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# Check for OOM kills
dmesg | grep -i "killed process"
grep -i "out of memory" /var/log/syslog
sudo journalctl -p crit --since "1 hour ago"

# Service status
systemctl status nginx
systemctl is-active nginx
systemctl is-failed nginx

# Hardware/kernel errors
dmesg -T | tail -50
dmesg -T | grep -i error
```

---

## Best Practices

### Monitoring Best Practices

| Practice | Why | How |
|----------|-----|-----|
| **Set thresholds** | Know when to act | CPU > 80%, Mem avail < 10%, Disk > 90% |
| **Monitor trends** | Predict issues | Track metrics over time, capacity planning |
| **Automate alerts** | Quick response | Nagios, Prometheus, custom scripts |
| **Document baselines** | Know what's normal | Record typical CPU, memory, disk usage |
| **Regular reviews** | Catch slow degradation | Weekly/monthly metric reviews |
| **Test alerts** | Ensure they work | Periodically trigger test alerts |

### Log Management Best Practices

| Practice | Why | How |
|----------|-----|-----|
| **Rotate regularly** | Prevent disk full | Daily/weekly with compression |
| **Secure permissions** | Protect sensitive data | 640 for logs, restrict access |
| **Centralize logs** | Easy searching/correlation | ELK, rsyslog, Graylog |
| **Retention policy** | Compliance + space | Keep 30-90 days, archive older |
| **Monitor log sizes** | Catch logging storms | Alert if log grows > X MB/hour |
| **Parse structured logs** | Better analysis | Use JSON logs when possible |
| **Sync time (NTP)** | Accurate correlation | All servers same time |

### Performance Troubleshooting Best Practices

| Practice | Why | How |
|----------|-----|-----|
| **Systematic approach** | Find root cause | Follow methodology, don't guess |
| **Document findings** | Knowledge sharing | Note what worked, what didn't |
| **Check basics first** | Quick wins | Disk space, memory, load average |
| **One change at a time** | Know what fixed it | Test, measure, repeat |
| **Monitor after fix** | Verify solution | Watch metrics for hours/days |
| **Root cause analysis** | Prevent recurrence | Why did it happen? How to prevent? |

---

## Troubleshooting Scenarios

### Scenario 1: Website Running Slow

```bash
# Step 1: Check load
uptime
# Load is 8.5 on 4-core system = overloaded

# Step 2: Find CPU hogs
top
# Apache processes using 90% CPU

# Step 3: Check connections
ss -s
# 500+ established connections (normally 50)

# Step 4: Check logs
sudo tail -f /var/log/apache2/access.log
# Lots of requests from same IPs (possible DDoS)

# Step 5: Block attackers
sudo iptables -A INPUT -s 192.168.1.100 -j DROP

# Step 6: Restart Apache
sudo systemctl restart apache2

# Step 7: Monitor
watch -n 1 'uptime && ss -s'
```

### Scenario 2: System Running Out of Disk

```bash
# Step 1: Check disk usage
df -h
# /var is 98% full

# Step 2: Find large directories
sudo du -sh /var/* | sort -rh | head
# /var/log is 80GB

# Step 3: Find large log files
sudo du -sh /var/log/* | sort -rh | head
# /var/log/apache2/access.log is 50GB

# Step 4: Check if rotated
ls -lh /var/log/apache2/
# No rotation happening!

# Step 5: Rotate now
sudo logrotate -f /etc/logrotate.d/apache2

# Step 6: Clean old logs manually
sudo find /var/log -name "*.gz" -mtime +90 -delete

# Step 7: Verify space freed
df -h /var
```

### Scenario 3: Memory Exhaustion

```bash
# Step 1: Check memory
free -h
# Available: 100MB, Swap: 1.8GB used

# Step 2: Check for OOM kills
dmesg | grep -i "killed process"
# MySQL was killed 3 times today

# Step 3: Find memory hogs
ps aux --sort=-%mem | head -10
# MySQL using 12GB RAM

# Step 4: Check MySQL config
cat /etc/mysql/my.cnf | grep -E "buffer|cache"
# innodb_buffer_pool_size = 12G (too high for 16GB system)

# Step 5: Reduce buffer pool
sudo vim /etc/mysql/my.cnf
# Set innodb_buffer_pool_size = 8G

# Step 6: Restart MySQL
sudo systemctl restart mysql

# Step 7: Monitor
watch -n 2 free -h
```

---
## Next Steps
Proceed to [Day 15: Networking & Troubleshooting](../Day_15/notes_and_exercises.md) to learn network configuration and diagnostics.
