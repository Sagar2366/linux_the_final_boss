# Day 13: Process Management & Scheduling (cron, at, anacron)

## Table of Contents

- [Day 13: Process Management & Scheduling (cron, at, anacron)](#day-13-process-management-&-scheduling-cron-at-anacron)
  - [Learning Objectives](#learning-objectives)
  - [Notes](#notes)
  - [Sample Exercises](#sample-exercises)
  - [Solutions](#solutions)
  - [Sample Interview Questions](#sample-interview-questions)
  - [Interview Question Answers](#interview-question-answers)
  - [Completion Checklist](#completion-checklist)
  - [Key Commands Summary](#key-commands-summary)
- [Cron management](#cron-management)
- [At scheduling](#at-scheduling)
- [Process control](#process-control)
  - [Next Steps](#next-steps)


## Learning Objectives
By the end of Day 13, you will:
- Master process viewing, control, signals, and prioritisation
- Use cron for recurring task scheduling (including advanced patterns)
- Use at for one-time job scheduling
- Understand anacron for periodic tasks on intermittent systems
- Troubleshoot scheduled jobs effectively
- Implement automated system maintenance tasks

**Estimated Time:** 1 hour

---

## Why These Tools Matter

| Tool | Purpose | Real-World Use Case |
|------|---------|---------------------|
| **Process Management** | Control running programs, manage resources | Kill hung applications, adjust priority for background tasks |
| **cron** | Automate recurring tasks | Daily backups, log rotation, system health checks |
| **at** | Schedule one-time jobs | Delayed system restart, reminder scripts, temporary tasks |
| **anacron** | Handle missed jobs on systems not always on | Laptop maintenance tasks, desktop cleanup jobs |

**Key for:** DevOps engineers, SREs, system administrators, automation tasks

---

## Sample Environment Setup

```bash
# Create test directory structure
mkdir -p ~/day13_test/{scripts,logs,procs}

# Create a dummy long-running process script
cat > ~/day13_test/scripts/longproc.sh << 'EOF'
#!/bin/bash
while true; do 
    echo "Running... $(date)" >> ~/day13_test/logs/proc.log
    sleep 10
done
EOF

# Create scheduling scripts
cat > ~/day13_test/scripts/daily.sh << 'EOF'
#!/bin/bash
echo "Cron job ran at $(date)" >> ~/day13_test/logs/cron.log
EOF

cat > ~/day13_test/scripts/onetime.sh << 'EOF'
#!/bin/bash
echo "One-time job ran at $(date)" >> ~/day13_test/logs/at.log
EOF

cat > ~/day13_test/scripts/weekly.sh << 'EOF'
#!/bin/bash
echo "Weekly task ran at $(date)" >> ~/day13_test/logs/weekly.log
EOF

# Make scripts executable
chmod +x ~/day13_test/scripts/*.sh

# Verify setup
ls -la ~/day13_test/scripts/
ls -la ~/day13_test/logs/  # Should be empty initially
```

---

## Part 1: Process Management (Recap & Deep Dive)

### Command Reference: Process Management

| Command | Usage | Description | Common Options |
|---------|-------|-------------|----------------|
| **ps** | `ps [options]` | Display snapshot of current processes | `aux` = all processes, full details<br>`-ef` = all with parent PIDs<br>`-p PID` = specific process<br>`-u USER` = user's processes |
| **top** | `top [options]` | Real-time process monitor | `-p PID` = monitor specific process<br>`-u USER` = user's processes<br>`-d SEC` = update delay |
| **htop** | `htop` | Enhanced interactive process viewer | (interactive: F3=search, F6=sort, F9=kill) |
| **pgrep** | `pgrep [options] pattern` | Find process ID by name | `-f` = match full command line<br>`-u USER` = by user<br>`-l` = show name with PID |
| **pstree** | `pstree [options]` | Display process tree | `-p` = show PIDs<br>`-u` = show user transitions<br>`-a` = show command line args |
| **kill** | `kill [signal] PID` | Send signal to process | `-15` or `-TERM` = graceful (default)<br>`-9` or `-KILL` = force kill<br>`-l` = list all signals |
| **killall** | `killall [options] name` | Kill processes by name | `-i` = interactive confirm<br>`-u USER` = by user<br>`-w` = wait for termination |
| **pkill** | `pkill [options] pattern` | Kill by pattern match | `-f` = match full command<br>`-u USER` = by user<br>`-9` = force kill |
| **nice** | `nice -n NUM command` | Start process with priority | `-n NUM` = niceness (-20 to 19)<br>Higher = lower priority |
| **renice** | `renice NUM [options]` | Change process priority | `NUM` = new niceness<br>`-p PID` = by process ID<br>`-u USER` = all user's processes |
| **jobs** | `jobs [options]` | List background jobs | `-l` = show PIDs<br>`-p` = PIDs only |
| **bg** | `bg [job_spec]` | Resume job in background | `%1` = job number 1 |
| **fg** | `fg [job_spec]` | Bring job to foreground | `%1` = job number 1 |

**Signal Reference:**

| Signal | Number | Name | Usage | Description |
|--------|--------|------|-------|-------------|
| SIGHUP | 1 | HUP | `kill -1 PID` or `kill -HUP PID` | Hangup - reload config |
| SIGINT | 2 | INT | `kill -2 PID` or Ctrl+C | Interrupt - stop interactive |
| SIGKILL | 9 | KILL | `kill -9 PID` | Force kill - cannot be caught |
| SIGTERM | 15 | TERM | `kill PID` or `kill -15 PID` | Terminate gracefully (default) |
| SIGSTOP | 19 | STOP | `kill -19 PID` or Ctrl+Z | Pause process |
| SIGCONT | 18 | CONT | `kill -18 PID` or `bg`/`fg` | Continue stopped process |

### Understanding Processes

Every command or script you run becomes a **process** - a running instance of a program with:
- **PID** (Process ID): Unique identifier
- **PPID** (Parent PID): Process that started it
- **User**: Owner of the process
- **State**: Running (R), Sleeping (S), Stopped (T), Zombie (Z)
- **Priority**: CPU scheduling priority (nice value)
- **Resources**: CPU%, Memory%, Time

### Process Viewing Commands

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `ps` | Snapshot of processes | `aux` = all users, full details<br>`-ef` = every process with parent |
| `top` | Live interactive monitor | `P` = sort by CPU, `M` = sort by memory<br>`k` = kill, `q` = quit, `1` = per-CPU |
| `htop` | Enhanced top (install separately) | Color-coded, mouse support, F9=kill |
| `pgrep` | Find PID by name | `pgrep -f script.sh` |
| `pstree` | Show process tree | `pstree -p` (with PIDs) |

#### PS Command Options Explained

| Option | Description | Example |
|--------|-------------|---------|
| `a` | All processes with terminals | `ps a` |
| `u` | User-oriented format (shows %CPU, %MEM) | `ps u` |
| `x` | Processes without terminals (daemons) | `ps x` |
| `aux` | **Most common**: All processes, detailed | `ps aux | grep nginx` |
| `-e` | Every process (alternative to `ax`) | `ps -e` |
| `-f` | Full format with parent PID | `ps -ef | grep ssh` |
| `-p PID` | Specific process | `ps -p 1234` |

**Example Output:**
```
USER  PID  %CPU %MEM    VSZ   RSS STAT START   TIME COMMAND
john  1234  0.5  2.1 123456 67890 S    10:30   0:05 /bin/bash script.sh
```

### Process States (STAT Column)

| State | Meaning | Description |
|-------|---------|-------------|
| **R** | Running | Actively executing or in run queue |
| **S** | Sleeping | Waiting for event (most processes) |
| **D** | Uninterruptible sleep | Waiting for I/O (disk, network) |
| **T** | Stopped | Paused (Ctrl+Z or SIGSTOP) |
| **Z** | Zombie | Finished but parent hasn't acknowledged |
| **<** | High priority | Nice value < 0 |
| **N** | Low priority | Nice value > 0 |
| **s** | Session leader | Process group leader |
| **+** | Foreground | In foreground process group |

### Top vs Htop Comparison

| Feature | top | htop |
|---------|-----|------|
| **Installation** | Built-in (no install) | `sudo apt install htop` or `brew install htop` |
| **Interface** | Text-based, keyboard-only | Colorful, mouse + keyboard |
| **Navigation** | Page Up/Down only | Arrow keys, scroll |
| **Sorting** | `P` (CPU), `M` (Memory), `T` (Time) | `F6` dropdown menu |
| **Killing** | `k` then enter PID | `F9` on highlighted row |
| **Search** | None (use `ps | grep`) | `F3` search, `F4` filter |
| **CPU View** | `1` key for per-CPU | Built-in multi-CPU view |
| **Colors** | Minimal | CPU/Memory bars, state colors |
| **Best For** | Quick checks, servers | Interactive use, desktops |

**Top Interactive Keys:**
- `P`: Sort by CPU usage
- `M`: Sort by memory usage
- `T`: Sort by running time
- `k`: Kill a process (prompts for PID)
- `1`: Toggle per-CPU view
- `q`: Quit

### Process Control: Signals

Processes respond to **signals** - software interrupts that tell them what to do.

| Signal | Number | Name | Description | Use Case |
|--------|--------|------|-------------|----------|
| **SIGTERM** | 15 | Terminate | Polite request to stop (allows cleanup) | Default `kill PID` |
| **SIGKILL** | 9 | Kill | Force kill (no cleanup, instant) | When SIGTERM fails |
| **SIGHUP** | 1 | Hangup | Reload configuration | `kill -HUP PID` for nginx/apache |
| **SIGINT** | 2 | Interrupt | Same as Ctrl+C | Stop interactive process |
| **SIGSTOP** | 19 | Stop | Pause process (cannot be caught) | Same as Ctrl+Z |
| **SIGCONT** | 18 | Continue | Resume stopped process | Use with `fg`/`bg` |

**List all signals:** `kill -l`

### Kill Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `kill PID` | Send SIGTERM (graceful) | `kill 1234` |
| `kill -9 PID` | Force kill (SIGKILL) | `kill -9 1234` |
| `kill -HUP PID` | Reload config | `kill -HUP $(cat /var/run/nginx.pid)` |
| `killall NAME` | Kill all by exact name | `killall firefox` |
| `pkill PATTERN` | Kill by pattern | `pkill -f "script.sh"` |
| `pkill -u USER` | Kill user's processes | `pkill -u apache` |

**⚠️ Warning:** `kill -9` should be **last resort** - it prevents cleanup, can corrupt data, leave lock files, orphan children.

### Process Priority: Nice Values

**Nice values** control CPU scheduling priority: **-20** (highest) to **19** (lowest). Default is **0**.

| Nice Value | Priority | Use Case |
|------------|----------|----------|
| **-20** | Highest | Critical system tasks (requires root) |
| **-10** | High | Important services |
| **0** | Normal | Default for user processes |
| **10** | Low | Background tasks |
| **19** | Lowest | Batch jobs, backups |

**Commands:**

| Command | Purpose | Example |
|---------|---------|---------|
| `nice -n NUM CMD` | Start with priority | `nice -n 15 ~/backup.sh` |
| `renice NUM PID` | Change running process | `renice -5 1234` (requires root for negative) |
| `renice NUM -u USER` | Change user's processes | `renice 10 -u john` |

**View nice value:** In `top`, check **NI** column. In `ps`, use `ps -eo pid,ni,cmd`.

### Hands-On Process Management

```bash
# 1. Start a background process
~/day13_test/scripts/longproc.sh &
# Note the PID (e.g., [1] 1234)

# 2. Find the process
ps aux | grep longproc
# Or
pgrep -f longproc.sh

# 3. Monitor it live
top -p 1234  # Replace 1234 with actual PID
# Press 'q' to quit

# 4. Check the log
tail -f ~/day13_test/logs/proc.log
# Ctrl+C to stop watching

# 5. Kill it gracefully
kill 1234
# Verify it's gone
ps aux | grep longproc

# 6. If it won't die (simulate by starting again)
~/day13_test/scripts/longproc.sh &
NEW_PID=$(pgrep -f longproc)
kill -9 $NEW_PID  # Force kill

# 7. Priority example
nice -n 15 ~/day13_test/scripts/longproc.sh &
ps -eo pid,ni,cmd | grep longproc  # NI column shows 15

# 8. Change priority (get PID first)
renice 5 $(pgrep -f longproc)
ps -eo pid,ni,cmd | grep longproc  # NI now 5
```

---

## Part 2: Cron - Recurring Task Scheduling

### Command Reference: Cron

| Command | Usage | Description | Examples |
|---------|-------|-------------|----------|
| **crontab** | `crontab [options]` | Manage user's cron jobs | See detailed options below |
| **crontab -e** | `crontab -e` | Edit current user's crontab | Opens in default editor (nano/vim) |
| **crontab -l** | `crontab -l` | List current user's crontab | Shows all scheduled jobs |
| **crontab -r** | `crontab -r` | Remove user's crontab | ⚠️ Deletes all jobs, no confirmation |
| **crontab -u** | `crontab -u USER [options]` | Manage another user's crontab | Requires root: `sudo crontab -u john -e` |
| **crontab -i** | `crontab -i -r` | Interactive removal | Prompts before deleting |

**Crontab File Locations:**

| Type | Location | Editor | Format |
|------|----------|--------|--------|
| User crontab | `/var/spool/cron/crontabs/USER` | Use `crontab -e` only | 5 fields + command |
| System crontab | `/etc/crontab` | `sudo vim /etc/crontab` | 6 fields (adds USER) |
| Drop-in directory | `/etc/cron.d/` | Create file: `sudo vim /etc/cron.d/myjob` | 6 fields |
| Hourly scripts | `/etc/cron.hourly/` | Place executable script | No cron syntax |
| Daily scripts | `/etc/cron.daily/` | Place executable script | No cron syntax |
| Weekly scripts | `/etc/cron.weekly/` | Place executable script | No cron syntax |
| Monthly scripts | `/etc/cron.monthly/` | Place executable script | No cron syntax |

### What is Cron?

**Cron** is a time-based job scheduler in Unix-like systems. The **cron daemon** (`crond` or `cron`) runs in the background and executes scheduled tasks.

### Crontab Syntax

**Format:** `minute hour day month weekday command`

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 7) (0 or 7 is Sunday)
│ │ │ │ │
│ │ │ │ │
* * * * * command to execute
```

### Cron Pattern Operators

| Operator | Meaning | Example | Explanation |
|----------|---------|---------|-------------|
| **\*** | Any/Every | `* * * * *` | Every minute |
| **,** | List | `0 1,13 * * *` | 1am and 1pm |
| **-** | Range | `0 9-17 * * *` | 9am to 5pm (hourly) |
| **/** | Step | `*/15 * * * *` | Every 15 minutes (0,15,30,45) |
| **Combined** | Multiple operators | `*/10 9-17 * * 1-5` | Every 10 min, 9-5pm, weekdays |

### Special Cron Strings

| String | Equivalent | When It Runs |
|--------|------------|--------------|
| `@reboot` | N/A | Once at system startup |
| `@yearly` or `@annually` | `0 0 1 1 *` | January 1st midnight |
| `@monthly` | `0 0 1 * *` | 1st of month midnight |
| `@weekly` | `0 0 * * 0` | Sunday midnight |
| `@daily` or `@midnight` | `0 0 * * *` | Every day midnight |
| `@hourly` | `0 * * * *` | Top of every hour |

### Common Cron Patterns

| Schedule | Cron Pattern | Description |
|----------|--------------|-------------|
| Every minute | `* * * * *` | Runs every 60 seconds |
| Every 5 minutes | `*/5 * * * *` | 0,5,10,15,20,25,30,35,40,45,50,55 |
| Every 15 minutes | `*/15 * * * *` | 0,15,30,45 past each hour |
| Every 30 minutes | `*/30 * * * *` or `0,30 * * * *` | 0,30 past each hour |
| Every hour | `0 * * * *` or `@hourly` | Top of every hour |
| Every 2 hours | `0 */2 * * *` | 0,2,4,6,8,10,12,14,16,18,20,22 |
| Daily at 2:30am | `30 2 * * *` | Once per day |
| Daily at midnight | `0 0 * * *` or `@daily` | 12:00am |
| Twice daily | `0 9,21 * * *` | 9am and 9pm |
| Every weekday 9am | `0 9 * * 1-5` | Monday-Friday |
| Every Sunday 3am | `0 3 * * 0` or `0 3 * * 7` | Weekly |
| 1st of month | `0 0 1 * *` or `@monthly` | First day of month |
| Every Monday 5am | `0 5 * * 1` | Weekly on Monday |
| Business hours | `0 9-17 * * 1-5` | Hourly, 9am-5pm, weekdays |
| Quarterly | `0 0 1 */3 *` | Jan, Apr, Jul, Oct |

### Cron Examples with Logging

```bash
# Basic examples
0 2 * * * /usr/bin/backup.sh                      # Daily 2am
*/10 * * * * /home/user/check.sh                  # Every 10 minutes
0 0 * * 0 /home/user/weekly-report.sh             # Sunday midnight
0 */6 * * * /usr/local/bin/sync.sh                # Every 6 hours

# With output redirection (IMPORTANT!)
0 2 * * * /home/user/backup.sh >> /var/log/backup.log 2>&1
*/5 * * * * /home/user/monitor.sh > /tmp/monitor.log 2>&1

# With environment variables
0 3 * * * export PATH=/usr/local/bin:$PATH && /home/user/script.sh

# Conditional execution (prevent overlap)
*/15 * * * * pgrep -f backup.sh || /home/user/backup.sh

# Using flock to prevent overlap
*/10 * * * * flock -n /tmp/myjob.lock /home/user/job.sh

# Special strings
@reboot /home/user/startup.sh                     # At boot
@daily /home/user/daily-cleanup.sh >> /var/log/cleanup.log 2>&1
@hourly /usr/local/bin/hourly-check.sh
```

### Hands-On Cron Practice

```bash
# 1. Edit your crontab
crontab -e
# (If first time, choose editor: nano is easiest)

# 2. Add a test job that runs every minute
* * * * * echo "Cron test at $(date)" >> ~/day13_test/logs/minute.log

# 3. Save and exit (Ctrl+O, Enter, Ctrl+X in nano)

# 4. Verify it was added
crontab -l

# 5. Wait 2 minutes, then check the log
cat ~/day13_test/logs/minute.log
# Should see 2+ entries with timestamps

# 6. Add a daily job
crontab -e
# Add this line:
0 2 * * * ~/day13_test/scripts/daily.sh >> ~/day13_test/logs/cron.log 2>&1

# 7. Add a weekday business hours job
crontab -e
# Add:
0 9-17 * * 1-5 echo "Business hours check" >> ~/day13_test/logs/business.log

# 8. List all your jobs
crontab -l

# 9. Remove the minute test job
crontab -e
# Delete the * * * * * line, save

# 10. View system-wide cron jobs
cat /etc/crontab
ls -la /etc/cron.d/
ls /etc/cron.daily/
```

### Cron Environment Issues

**Problem:** Cron jobs run with a **minimal environment** (limited PATH, no aliases, no .bashrc).

**Solutions:**

```bash
# 1. Use absolute paths
# Bad:
0 2 * * * backup.sh

# Good:
0 2 * * * /home/user/scripts/backup.sh

# 2. Set environment variables in crontab
PATH=/usr/local/bin:/usr/bin:/bin
SHELL=/bin/bash
0 2 * * * /home/user/backup.sh

# 3. Source profile in script
#!/bin/bash
source ~/.bashrc
# ... rest of script

# 4. Debug environment
* * * * * env > ~/cron-env.txt
# Compare with: env > ~/shell-env.txt
```

---

## Part 3: At - One-Time Job Scheduling

### What is At?

**At** schedules commands to run **once** at a specific time. Unlike cron (recurring), at jobs execute once and disappear.

### At Command Syntax

| Format | Example | When It Runs |
|--------|---------|--------------|
| Absolute time | `at 14:30` | Today at 2:30 PM |
| | `at 10:00 AM tomorrow` | Tomorrow 10am |
| | `at 15:00 2025-10-20` | Specific date/time |
| Relative time | `at now + 10 minutes` | 10 minutes from now |
| | `at now + 2 hours` | 2 hours from now |
| | `at now + 3 days` | 3 days from now |
| | `at now + 1 week` | 7 days from now |

### At Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `at TIME` | Schedule job (interactive) | `at 14:30` then enter commands, Ctrl+D |
| `echo "cmd" | at TIME` | Schedule job (piped) | `echo "~/script.sh" | at now + 10 min` |
| `atq` | List queued jobs | Shows job#, time, queue, user |
| `atrm JOB#` | Remove job | `atrm 3` (cancels job 3) |
| `at -c JOB#` | View job details | `at -c 3` (shows full command & env) |
| `batch` | Run when load is low | Like at, but waits for low system load |

### Hands-On At Practice

```bash
# 1. Check if atd service is running
systemctl status atd  # Ubuntu/Debian
# If not running: sudo systemctl start atd

# 2. Schedule a job for 2 minutes from now (interactive)
at now + 2 minutes
# Type:
~/day13_test/scripts/onetime.sh
# Press Ctrl+D to finish
# Output: job 1 at Wed Oct 15 14:32:00 2025

# 3. Schedule a job (piped - easier)
echo "~/day13_test/scripts/onetime.sh" | at now + 3 minutes

# 4. List queued jobs
atq
# Output:
# 1    Wed Oct 15 14:32:00 2025 a john
# 2    Wed Oct 15 14:33:00 2025 a john

# 5. View job details
at -c 1

# 6. Remove a job
atrm 2
atq  # Verify it's gone

# 7. Wait for first job to run, then check log
sleep 180  # Wait 3 minutes
cat ~/day13_test/logs/at.log

# 8. More examples
at 23:59
# Type commands, Ctrl+D

echo "shutdown -h now" | sudo at 02:00
# Schedule shutdown for 2am

at noon tomorrow
# Type commands, Ctrl+D

at 10:00 PM + 3 days
# Schedule for 10pm three days from now
```

---

## Part 4: Anacron - Periodic Task Scheduling

### Command Reference: Anacron

| Command | Usage | Description | Examples |
|---------|-------|-------------|----------|
| **anacron** | `anacron [options]` | Run periodic jobs | See options below |
| **anacron -T** | `sudo anacron -T` | Test config syntax | No output = syntax OK |
| **anacron -n** | `sudo anacron -n` | Run jobs now (don't wait for delay) | Forces immediate execution |
| **anacron -f** | `sudo anacron -f` | Force run even if up-to-date | Ignores timestamps |
| **anacron -u** | `sudo anacron -u` | Update timestamps only (don't run) | Marks jobs as run |
| **anacron -d** | `sudo anacron -d` | Debug mode (run in foreground) | Shows detailed output |
| **anacron -s** | `sudo anacron -s JOB` | Run specific job only | `sudo anacron -s cron.daily` |
| **anacron -t FILE** | `sudo anacron -t /path/to/file` | Use alternative config file | Default: `/etc/anacrontab` |

**Anacron Configuration Files:**

| File | Purpose | Format |
|------|---------|--------|
| `/etc/anacrontab` | Main config | `period delay job-id command` |
| `/var/spool/anacron/` | Timestamp directory | Contains job-id files with last run date |
| `/etc/cron.daily/` | Daily jobs | Anacron runs these scripts |
| `/etc/cron.weekly/` | Weekly jobs | Anacron runs these scripts |
| `/etc/cron.monthly/` | Monthly jobs | Anacron runs these scripts |

**Anacron Config Format:**

```bash
# /etc/anacrontab format
# period  delay  job-identifier  command

# Example:
1         5      cron.daily      run-parts /etc/cron.daily
7         10     cron.weekly     run-parts /etc/cron.weekly
30        15     cron.monthly    run-parts /etc/cron.monthly
```

| Field | Description | Valid Values | Example |
|-------|-------------|--------------|---------|
| **period** | Days between runs | 1-365 (days) | `1` (daily), `7` (weekly), `30` (monthly) |
| **delay** | Minutes to wait after boot | 0-∞ (minutes) | `5` (wait 5 min), `10` (wait 10 min) |
| **job-identifier** | Unique job name (no spaces) | alphanumeric, hyphens, underscores | `daily-backup`, `weekly_cleanup` |
| **command** | Command or script to execute | Full path recommended | `/home/user/script.sh` |

**Special Variables in /etc/anacrontab:**

```bash
SHELL=/bin/bash           # Shell to use
PATH=/sbin:/bin:/usr/sbin:/usr/bin  # PATH for commands
MAILTO=root               # Email output to user
RANDOM_DELAY=45          # Max random delay in minutes
START_HOURS_RANGE=3-22   # Only run between 3am-10pm
```

### What is Anacron?

**Anacron** ensures periodic jobs run even if the system was off during the scheduled time. Perfect for:
- Laptops (not always on)
- Desktops (shut down overnight)
- Systems with unpredictable uptime

**Difference from Cron:**
- **Cron:** "Run at exact time" (e.g., daily at 2am - if off, skipped)
- **Anacron:** "Run once per period" (e.g., daily - catches up when system boots)

### Anacron Timestamps

Anacron tracks last run time in `/var/spool/anacron/`:
```bash
ls /var/spool/anacron/
# cron.daily  cron.weekly  cron.monthly

cat /var/spool/anacron/cron.daily
# 20251015 (YYYYMMDD of last run)
```

### Hands-On Anacron Practice

```bash
# 1. Check anacron version
anacron -V

# 2. View current config
cat /etc/anacrontab

# 3. Test syntax
sudo anacron -T
# No output = syntax OK

# 4. Add a custom job (requires root)
sudo vim /etc/anacrontab
# Add this line:
1  10  test-daily  /home/user/day13_test/scripts/daily.sh

# 5. Test syntax again
sudo anacron -T

# 6. Force run now (don't wait for delay)
sudo anacron -n -f

# 7. Check if it ran
cat ~/day13_test/logs/cron.log

# 8. View timestamp
sudo cat /var/spool/anacron/test-daily

# 9. Check logs
grep anacron /var/log/syslog  # Ubuntu/Debian
grep anacron /var/log/cron    # RHEL/CentOS

# 10. Remove test job
sudo vim /etc/anacrontab
# Delete the test-daily line
```

---

## Part 5: Troubleshooting Scheduled Jobs

### Command Reference: Logging & Debugging

| Command | Usage | Description | Examples |
|---------|-------|-------------|----------|
| **grep** | `grep PATTERN FILE` | Search log files | `grep CRON /var/log/syslog` |
| **tail** | `tail [options] FILE` | View end of file | `-f` follow (live), `-n NUM` last N lines |
| **journalctl** | `journalctl [options]` | Query systemd logs | `-u cron` = cron service logs<br>`-f` = follow |
| **systemctl** | `systemctl status SERVICE` | Check service status | `systemctl status cron` |
| **ls -la** | `ls -la FILE` | Check permissions | Shows rwx permissions and owner |
| **chmod** | `chmod MODE FILE` | Change permissions | `chmod +x script.sh` (make executable) |
| **env** | `env` | Show environment variables | `env > file.txt` to save |
| **bash -x** | `bash -x SCRIPT` | Debug shell script | Shows each command as executed |
| **df -h** | `df -h` | Check disk space | `-h` = human-readable |
| **flock** | `flock [options] FILE CMD` | File locking for overlap prevention | `-n` = non-blocking (exit if locked) |

**Log File Locations:**

| System | Cron Logs | Syslog | At Logs |
|--------|-----------|--------|---------|
| **Ubuntu/Debian** | `/var/log/syslog` (grep CRON) | `/var/log/syslog` | `/var/log/syslog` (grep atd) |
| **RHEL/CentOS/Fedora** | `/var/log/cron` | `/var/log/messages` | `/var/log/cron` |
| **systemd (all)** | `journalctl -u cron` | `journalctl` | `journalctl -u atd` |
| **macOS** | `/var/log/system.log` | `/var/log/system.log` | N/A (use cron instead) |

**Useful Log Commands:**

```bash
# View last 50 cron entries
grep CRON /var/log/syslog | tail -50        # Ubuntu/Debian
tail -50 /var/log/cron                      # RHEL/CentOS

# Follow cron logs in real-time
tail -f /var/log/syslog | grep CRON         # Ubuntu/Debian
tail -f /var/log/cron                       # RHEL/CentOS
journalctl -u cron -f                       # systemd

# View cron logs for specific user
grep CRON /var/log/syslog | grep "(john)"

# View all cron job executions today
grep CRON /var/log/syslog | grep "$(date +%b\ %d)"

# Check anacron logs
grep anacron /var/log/syslog                # Ubuntu/Debian
grep anacron /var/log/cron                  # RHEL/CentOS

# Check at daemon logs
grep atd /var/log/syslog                    # Ubuntu/Debian
journalctl -u atd                           # systemd
```

### Common Cron Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Job doesn't run | Cron syntax error | Check with `crontab -l`, verify format |
| | crond not running | `sudo systemctl status cron` or `crond` |
| | Script not executable | `chmod +x script.sh` |
| Job runs but fails | Wrong path (relative) | Use absolute paths: `/home/user/script.sh` |
| | Environment missing | Add PATH in crontab or source ~/.bashrc in script |
| | Permission denied | Check file ownership and permissions |
| No output/logs | Output not redirected | Add `>> /path/to/log 2>&1` |
| Job runs multiple times | Overlapping execution | Use flock or process check |

### Troubleshooting Checklist

```bash
# 1. Check if cron daemon is running
systemctl status cron     # Ubuntu/Debian
systemctl status crond    # RHEL/CentOS

# If not running:
sudo systemctl start cron
sudo systemctl enable cron

# 2. Check cron logs
grep CRON /var/log/syslog    # Ubuntu/Debian
cat /var/log/cron            # RHEL/CentOS
journalctl -u cron           # systemd systems

# 3. Verify crontab entry
crontab -l

# 4. Test script manually
/home/user/scripts/script.sh
# Does it work? Check for errors

# 5. Check script permissions
ls -la /home/user/scripts/script.sh
# Should be: -rwxr-xr-x (executable)

# 6. Verify paths are absolute
crontab -l | grep -v "^#" | grep -v "^$"
# All commands should use /full/paths

# 7. Check environment
# Add this cron job temporarily:
* * * * * env > ~/cron-env.txt
# Compare with your shell: env > ~/shell-env.txt

# 8. Check for output/errors
# Temporarily redirect to file:
* * * * * /home/user/script.sh >> /tmp/debug.log 2>&1
# Wait a minute, then: cat /tmp/debug.log

# 9. Check disk space
df -h
# Full disk prevents cron from running

# 10. Check user permissions
# Can user run the command?
sudo -u username /home/user/script.sh
```

### Preventing Overlapping Jobs

**Problem:** Job runs every 5 minutes but takes 10 minutes to complete.

**Solutions:**

#### 1. Using flock (Recommended)
```bash
# In crontab:
*/5 * * * * flock -n /tmp/myjob.lock /home/user/script.sh
# -n = non-blocking (exit if locked)
```

#### 2. Using pidfile in script
```bash
#!/bin/bash
PIDFILE=/tmp/myscript.pid

if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p $PID > /dev/null; then
        echo "Already running (PID $PID)"
        exit 1
    fi
fi

echo $$ > "$PIDFILE"
trap "rm -f $PIDFILE" EXIT

# Your script logic here
sleep 600  # Simulate long-running task

rm -f "$PIDFILE"
```

#### 3. Using pgrep
```bash
# In crontab:
*/5 * * * * pgrep -f myscript.sh || /home/user/myscript.sh
# Only runs if not already running
```

---

## Sample Exercises

### Exercise 1: Process Management
**Task:** Start a long-running process, find its PID, monitor it, adjust priority, and kill it.

**Solution:**
```bash
# 1. Start process in background
~/day13_test/scripts/longproc.sh &
# Note: [1] 12345 (job number and PID)

# 2. Find PID multiple ways
ps aux | grep longproc
pgrep -f longproc.sh
jobs -l  # Shows background jobs

# 3. Monitor it
top -p 12345  # Press 'q' to quit
# Or: htop (then F3 to search, type "longproc")

# 4. Check nice value
ps -eo pid,ni,cmd | grep longproc

# 5. Change priority
renice 10 12345  # Lower priority (nice to others)
ps -eo pid,ni,cmd | grep longproc  # Verify NI=10

# 6. Kill gracefully
kill 12345
sleep 2
ps aux | grep longproc  # Should be gone

# 7. If still running, force kill
kill -9 12345
```

### Exercise 2: Basic Cron Job
**Task:** Schedule a script to run every day at midnight.

**Solution:**
```bash
# 1. Create script if needed
cat > ~/day13_test/scripts/midnight.sh << 'EOF'
#!/bin/bash
echo "Midnight job ran at $(date)" >> ~/day13_test/logs/midnight.log
EOF

chmod +x ~/day13_test/scripts/midnight.sh

# 2. Edit crontab
crontab -e

# 3. Add this line:
0 0 * * * ~/day13_test/scripts/midnight.sh >> ~/day13_test/logs/cron.log 2>&1

# 4. Save and verify
crontab -l

# 5. Test manually
~/day13_test/scripts/midnight.sh
cat ~/day13_test/logs/midnight.log

# 6. To test without waiting for midnight, temporarily change to:
# */1 * * * * ~/day13_test/scripts/midnight.sh >> ~/day13_test/logs/cron.log 2>&1
# Wait 2 minutes, check log, then change back to 0 0 * * *
```

### Exercise 3: One-Time Job with At
**Task:** Schedule a one-time job to run 10 minutes from now.

**Solution:**
```bash
# 1. Check atd service
systemctl status atd
# If not running: sudo systemctl start atd

# 2. Schedule the job
echo "~/day13_test/scripts/onetime.sh" | at now + 10 minutes
# Output: job 3 at Wed Oct 15 14:45:00 2025

# 3. List queued jobs
atq
# Output: 3    Wed Oct 15 14:45:00 2025 a username

# 4. View job details
at -c 3

# 5. Wait 10 minutes (or remove to test removal)
# atrm 3  # To cancel
# Or wait and check log:
sleep 600
cat ~/day13_test/logs/at.log

# 6. Verify job is gone
atq  # Should be empty
```

### Exercise 4: Advanced Cron Patterns
**Task:** Create these schedules:
- Every 5 minutes during business hours (9am-5pm) on weekdays
- Every Monday at 5am
- First day of every month at midnight
- Every 15 minutes

**Solution:**
```bash
crontab -e

# Add these lines:
*/5 9-17 * * 1-5 ~/day13_test/scripts/business.sh >> ~/day13_test/logs/business.log 2>&1
0 5 * * 1 ~/day13_test/scripts/weekly.sh >> ~/day13_test/logs/weekly.log 2>&1
0 0 1 * * ~/day13_test/scripts/monthly.sh >> ~/day13_test/logs/monthly.log 2>&1
*/15 * * * * ~/day13_test/scripts/frequent.sh >> ~/day13_test/logs/frequent.log 2>&1

# Verify
crontab -l
```

### Exercise 5: Prevent Job Overlap
**Task:** Create a script that takes 2 minutes to run, schedule it every minute, and prevent overlap.

**Solution:**
```bash
# 1. Create slow script
cat > ~/day13_test/scripts/slow.sh << 'EOF'
#!/bin/bash
echo "Starting at $(date)" >> ~/day13_test/logs/slow.log
sleep 120  # 2 minutes
echo "Finished at $(date)" >> ~/day13_test/logs/slow.log
EOF

chmod +x ~/day13_test/scripts/slow.sh

# 2. Add to crontab with flock
crontab -e

# Add:
* * * * * flock -n /tmp/slow.lock ~/day13_test/scripts/slow.sh

# 3. Verify behavior
# Wait 3-4 minutes, then:
cat ~/day13_test/logs/slow.log
# Should see starts are 2+ minutes apart (no overlap)
```

### Exercise 6: Troubleshoot Failed Cron Job
**Task:** Debug a cron job that isn't running.

**Solution:**
```bash
# 1. Check if cron daemon is running
systemctl status cron

# 2. Check cron logs
grep CRON /var/log/syslog | tail -20    # Ubuntu/Debian
tail -20 /var/log/cron                  # RHEL/CentOS

# 3. List crontab
crontab -l

# 4. Test script manually
bash -x ~/day13_test/scripts/problem.sh
# -x shows debug output

# 5. Check permissions
ls -la ~/day13_test/scripts/problem.sh
# Should be executable (chmod +x if not)

# 6. Check for relative paths
# Bad: 0 2 * * * scripts/backup.sh
# Good: 0 2 * * * /home/user/scripts/backup.sh

# 7. Debug environment
crontab -e
# Add temporarily:
* * * * * env > ~/cron-env.txt
# Wait 1 minute, then:
diff <(sort ~/cron-env.txt) <(sort <(env))

# 8. Add logging to cron job
crontab -e
# Change:
# 0 2 * * * ~/script.sh
# To:
# 0 2 * * * ~/script.sh >> ~/logs/script.log 2>&1

# 9. Check disk space
df -h

# 10. Verify PATH in crontab
crontab -e
# Add at top:
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
```

### Exercise 7: Anacron Configuration
**Task:** Set up anacron to run a daily maintenance script.

**Solution:**
```bash
# 1. Check anacron is installed
anacron -V

# 2. Create maintenance script
cat > ~/day13_test/scripts/maintenance.sh << 'EOF'
#!/bin/bash
echo "Maintenance ran at $(date)" >> ~/day13_test/logs/maintenance.log
# Add cleanup tasks here
find ~/day13_test/logs -name "*.log" -mtime +30 -delete
EOF

chmod +x ~/day13_test/scripts/maintenance.sh

# 3. Edit anacrontab (requires root)
sudo vim /etc/anacrontab

# 4. Add line:
1  15  daily-maintenance  /home/user/day13_test/scripts/maintenance.sh

# 5. Test syntax
sudo anacron -T

# 6. Force run now
sudo anacron -n -f

# 7. Check logs
cat ~/day13_test/logs/maintenance.log
grep anacron /var/log/syslog

# 8. Check timestamp
sudo cat /var/spool/anacron/daily-maintenance
```

---

## Sample Interview Questions

| # | Question | Key Concepts |
|---|----------|--------------|
| 1 | What is the difference between cron, at, and anacron? | Recurring vs one-time vs periodic scheduling |
| 2 | How do you edit and list cron jobs for a user? | crontab commands, user context |
| 3 | What is the crontab syntax? Explain each field. | Field order, ranges, wildcards, special characters |
| 4 | How do you schedule a job to run every Monday at 5am? | Weekday field, hour field |
| 5 | How do you redirect output from a cron job? | stdout/stderr redirection, logging |
| 6 | What are the risks of running scripts as root in cron? | Security, privilege escalation, damage potential |
| 7 | How do you prevent overlapping cron jobs? | Lock files, flock, process checks |
| 8 | How do you troubleshoot a cron job that isn't running? | Logs, permissions, environment, paths |
| 9 | Where are system-wide cron jobs defined? | Config file locations |
| 10 | How do you schedule a job to run only once? | at command usage |
| 11 | Explain process states in Linux. | R, S, D, T, Z states |
| 12 | What's the difference between kill and kill -9? | SIGTERM vs SIGKILL, cleanup |
| 13 | How do nice values work? | Priority range -20 to 19, CPU scheduling |
| 14 | What happens if a cron job takes longer than its interval? | Overlap issues, prevention methods |
| 15 | How does cron's environment differ from your shell? | Minimal PATH, no profile, limited variables |

---

## Interview Question Answers

| Question | Answer | Example |
|----------|--------|---------|
| **1. Scheduling Tools** | **cron:** Recurring tasks at specific times (exact schedule)<br>**at:** One-time jobs at specific time (runs once, then removed)<br>**anacron:** Periodic tasks that catch up if system was off | cron: Daily backup at 2am every day<br>at: Send reminder email in 30 minutes<br>anacron: Weekly report (catches up Monday if laptop was off Sunday) |
| **2. Cron Management** | **Edit:** `crontab -e` (opens editor for current user's crontab)<br>**List:** `crontab -l` (displays all scheduled jobs)<br>**Remove:** `crontab -r` (deletes entire crontab - dangerous!)<br>**Other user:** `sudo crontab -u username -e` | `crontab -e` → Add `0 2 * * * ~/backup.sh`<br>`crontab -l` → Verify entry appears<br>`sudo crontab -u apache -l` → View apache's jobs |
| **3. Crontab Format** | `min hour day month weekday command`<br>**Fields:** 0-59 (min), 0-23 (hour), 1-31 (day), 1-12 (month), 0-7 (weekday; 0/7=Sunday)<br>**Operators:** * (any), , (list), - (range), / (step) | `30 14 * * 1-5` = 2:30 PM weekdays<br>`*/15 * * * *` = every 15 mins (0,15,30,45)<br>`0 0 1 * *` = midnight on 1st of month<br>`0 9-17 * * 1-5` = hourly 9am-5pm weekdays |
| **4. Weekly Schedule** | `0 5 * * 1 ~/script.sh`<br>**Breakdown:** 0 (minute 0), 5 (5am), * (any day), * (any month), 1 (Monday)<br>**Note:** Weekday 1=Mon, 0 or 7=Sun | Monday 5am: `0 5 * * 1 ~/backup.sh`<br>Every day 5am: `0 5 * * * ~/backup.sh`<br>Sunday 5am: `0 5 * * 0 ~/backup.sh` |
| **5. Output Redirect** | Append `>> /path/to/log 2>&1` to capture stdout and stderr<br>`>>` = append (vs `>` overwrite)<br>`2>&1` = redirect stderr (2) to stdout (1)<br>**Critical:** Without this, cron emails output (or silently fails) | `0 2 * * * ~/backup.sh >> ~/logs/backup.log 2>&1`<br>(Captures success messages and errors)<br>Discard output: `> /dev/null 2>&1` |
| **6. Root Risks** | **Full system access:** Can modify/delete OS files, create security holes<br>**Risks:** Typos can destroy system (`rm -rf / tmp` vs `/tmp`), malicious code, privilege escalation<br>**Mitigate:** Test as user first, use sudo for specific commands only, audit scripts, validate all inputs, use absolute paths | **Bad:** `0 2 * * * rm -rf $DIR/*` (if $DIR empty = disaster)<br>**Good:** Run as user, use sudo only when needed: `0 2 * * * sudo /usr/bin/specific-task` |
| **7. Prevent Overlap** | **flock:** `flock -n /tmp/lock.file script.sh` (exits if locked)<br>**Lock file:** Create file before running, check if exists<br>**Process check:** `pgrep -f script.sh` to see if already running<br>**Why:** Long-running jobs can stack up, consume resources, cause conflicts | **Best:** `*/5 * * * * flock -n /tmp/backup.lock ~/backup.sh`<br>**Script:** `pgrep -f backup.sh || ~/backup.sh`<br>**Manual lock:** Script creates `/tmp/myjob.lock`, removes on exit |
| **8. Troubleshooting** | **1. Check daemon:** `systemctl status cron`<br>**2. Check logs:** `/var/log/cron` or `grep CRON /var/log/syslog`<br>**3. Verify syntax:** `crontab -l`<br>**4. Test manually:** Run script directly<br>**5. Permissions:** Script executable? (`chmod +x`)<br>**6. Paths:** Use absolute paths (`/home/user/script.sh`)<br>**7. Environment:** cron has minimal env (add PATH in crontab)<br>**8. Disk space:** `df -h` | Debug: `* * * * * env > ~/cron-env.txt` to see cron's environment<br>Fix PATH: Add `PATH=/usr/bin:/bin` at top of crontab<br>Test: `bash -x ~/script.sh` (debug mode) |
| **9. System Jobs** | **User crontab:** `crontab -e` (stored in `/var/spool/cron/`)<br>**System crontab:** `/etc/crontab` (requires USER field)<br>**Drop-in:** `/etc/cron.d/` (package cron jobs, 6-field format)<br>**Convenience:** `/etc/cron.{hourly,daily,weekly,monthly}/` (scripts run by anacron/cron) | **User:** `crontab -e` → `0 2 * * * ~/backup.sh`<br>**System:** `/etc/crontab` → `0 2 * * * root /backup.sh`<br>**Drop-in:** `/etc/cron.d/myapp` → `0 2 * * * root /usr/local/bin/myapp`<br>**Script:** `/etc/cron.daily/cleanup` (no cron syntax, just executable script) |
| **10. One-Time Jobs** | Use `at` command:<br>**Piped:** `echo "command" | at TIME`<br>**Interactive:** `at TIME` → type commands → Ctrl+D<br>**Manage:** `atq` (list), `atrm JOB#` (remove), `at -c JOB#` (view details) | `echo "~/backup.sh" | at now + 1 hour`<br>`at 15:00 tomorrow` → `~/script.sh` → Ctrl+D<br>`atq` → `3  Thu Oct 16 15:00:00 2025`<br>`atrm 3` (cancel job 3) |
| **11. Process States** | **R:** Running (executing or runnable)<br>**S:** Sleeping (waiting for event, most processes)<br>**D:** Uninterruptible sleep (I/O wait, can't be killed)<br>**T:** Stopped (Ctrl+Z or SIGSTOP)<br>**Z:** Zombie (finished, parent hasn't acknowledged)<br>**Modifiers:** `<` (high priority), `N` (low priority), `s` (session leader) | `ps aux`: STAT column shows state<br>`R` = actively running<br>`S` = waiting (interruptible)<br>`D` = disk I/O (can't kill)<br>`Z` = zombie (parent should reap) |
| **12. Kill vs Kill -9** | **kill PID** (SIGTERM, signal 15): Polite request to stop, allows cleanup (close files, save state, exit gracefully)<br>**kill -9 PID** (SIGKILL, signal 9): Force kill, immediate, no cleanup possible<br>**When -9:** Only if SIGTERM fails (hung process) | **Good:** `kill 1234` → process saves data, closes files, exits cleanly<br>**Last resort:** `kill -9 1234` → instant death, may corrupt data, leave lock files<br>**Other:** `kill -HUP 1234` (reload config) |
| **13. Nice Values** | **Range:** -20 (highest priority) to 19 (lowest)<br>**Default:** 0 (normal)<br>**Negative:** Requires root (critical tasks)<br>**Positive:** Any user (background/batch jobs)<br>**CPU sharing:** Nice processes get less CPU time | **Low priority:** `nice -n 15 ~/batch-job.sh`<br>**High priority:** `sudo nice -n -10 ~/critical.sh`<br>**Change running:** `renice 10 1234`<br>View: `top` (NI column) or `ps -eo pid,ni,cmd` |
| **14. Job Overlap** | **Problem:** Job scheduled every 5 min takes 10 min → multiple instances run simultaneously<br>**Consequences:** Resource contention, data corruption, duplicate operations<br>**Solutions:** flock, lock files, process checks, increase interval | **Without protection:** 5 jobs stack up, system overloads<br>**With flock:** `*/5 * * * * flock -n /tmp/job.lock ~/job.sh` (skips if running)<br>**With check:** `pgrep -f job.sh || ~/job.sh` |
| **15. Cron Environment** | **Cron:** Minimal environment, limited PATH (`/usr/bin:/bin`), no HOME, no aliases, no .bashrc<br>**Shell:** Full environment, custom PATH, aliases, variables from profile<br>**Fix:** Set variables in crontab, use absolute paths, source profile in script | **Cron PATH:** `/usr/bin:/bin`<br>**Shell PATH:** `/usr/local/bin:/usr/bin:/bin:...`<br>**Debug:** `* * * * * env > ~/cron-env.txt`<br>**Fix:** Add `PATH=/usr/local/bin:/usr/bin:/bin` in crontab |

---

## Completion Checklist

**Use this to verify your Day 13 mastery:**

### Process Management
- [ ] Can view processes with `ps aux` and filter results with grep
- [ ] Understand `top` interface: sorting (P/M/T), killing (k), per-CPU view (1)
- [ ] Know difference between `kill` (SIGTERM) and `kill -9` (SIGKILL)
- [ ] Can use `killall` and `pkill` to kill processes by name/pattern
- [ ] Understand process states: R (running), S (sleeping), D (I/O wait), T (stopped), Z (zombie)
- [ ] Can adjust process priority with `nice` (start) and `renice` (change running)
- [ ] Know nice value range: -20 (highest) to 19 (lowest), default 0

### Cron Scheduling
- [ ] Can edit crontab with `crontab -e` and list with `crontab -l`
- [ ] Understand crontab syntax: `min hour day month weekday command`
- [ ] Can create patterns: wildcards (*), ranges (1-5), steps (*/5), lists (1,3,5)
- [ ] Know special strings: `@daily`, `@reboot`, `@hourly`, `@weekly`, `@monthly`
- [ ] Can redirect output: `>> /path/to/log 2>&1`
- [ ] Understand common patterns: every 5 mins, daily, weekly, business hours
- [ ] Know difference between user crontab and system crontab (`/etc/crontab`)
- [ ] Can troubleshoot cron jobs: check logs, test manually, verify permissions

### At Scheduling
- [ ] Can schedule one-time jobs with `at now + TIME` or `at TIME`
- [ ] Know time formats: `now + 10 minutes`, `14:30`, `tomorrow`, specific dates
- [ ] Can list queued jobs with `atq`
- [ ] Can remove jobs with `atrm JOB#`
- [ ] Can view job details with `at -c JOB#`
- [ ] Understand `batch` command (runs when system load is low)

### Anacron
- [ ] Understand anacron's purpose: periodic tasks that catch up missed runs
- [ ] Know config file: `/etc/anacrontab`
- [ ] Understand format: `period delay identifier command`
- [ ] Can test syntax with `sudo anacron -T`
- [ ] Can force run with `sudo anacron -n`
- [ ] Know timestamp location: `/var/spool/anacron/`

### Troubleshooting & Best Practices
- [ ] Can check cron logs: `/var/log/cron` or `grep CRON /var/log/syslog`
- [ ] Always use absolute paths in cron jobs (not relative)
- [ ] Can prevent overlapping jobs with flock or process checks
- [ ] Understand cron environment limitations (minimal PATH, no aliases)
- [ ] Know security risks of running cron jobs as root
- [ ] Can debug cron environment with `* * * * * env > ~/cron-env.txt`
- [ ] Always redirect output to log files for debugging
- [ ] Test scripts manually before adding to cron

---

## Key Commands Summary

| Category | Command | Purpose |
|----------|---------|---------|
| **Cron Management** | `crontab -e` | Edit current user's crontab |
| | `crontab -l` | List current user's cron jobs |
| | `crontab -r` | Remove all user's cron jobs (⚠️ no confirmation!) |
| | `sudo crontab -u USER -e` | Edit another user's crontab |
| | `sudo crontab -u USER -l` | List another user's cron jobs |
| **At Scheduling** | `at TIME` | Schedule job at specific time (interactive) |
| | `echo "cmd" | at TIME` | Schedule job (piped) |
| | `atq` | List queued at jobs |
| | `atrm JOB#` | Remove at job by number |
| | `at -c JOB#` | View job details and environment |
| | `batch` | Run when system load is low |
| **Process Viewing** | `ps aux` | List all processes (detailed) |
| | `ps -ef` | List with parent PID (tree-like) |
| | `ps aux | grep NAME` | Find process by name |
| | `pgrep NAME` | Get PID by name |
| | `pgrep -f PATTERN` | Get PID by full command pattern |
| | `top` | Live process monitor (q=quit, k=kill) |
| | `htop` | Enhanced monitor (if installed) |
| | `pstree` | Show process tree |
| **Process Control** | `kill PID` | Send SIGTERM (graceful stop) |
| | `kill -9 PID` | Send SIGKILL (force kill) |
| | `kill -HUP PID` | Send SIGHUP (reload config) |
| | `killall NAME` | Kill all processes by exact name |
| | `pkill PATTERN` | Kill by pattern match |
| | `pkill -u USER` | Kill user's processes |
| **Process Priority** | `nice -n NUM CMD` | Start with priority (-20 to 19) |
| | `renice NUM PID` | Change running process priority |
| | `renice NUM -u USER` | Change user's process priorities |
| **Anacron** | `anacron -T` | Test anacrontab syntax |
| | `anacron -n` | Run jobs now (force) |
| | `anacron -u` | Update timestamps only |
| | `sudo vim /etc/anacrontab` | Edit anacron config |
| **Logs & Debugging** | `grep CRON /var/log/syslog` | Check cron logs (Ubuntu/Debian) |
| | `cat /var/log/cron` | Check cron logs (RHEL/CentOS) |
| | `journalctl -u cron` | Check cron logs (systemd) |
| | `systemctl status cron` | Check cron daemon status |
| | `systemctl status atd` | Check at daemon status |

---

## Quick Reference: Common Cron Patterns

| Schedule | Cron Pattern | Description |
|----------|--------------|-------------|
| Every minute | `* * * * *` | Runs every 60 seconds (testing only!) |
| Every 5 minutes | `*/5 * * * *` | 0,5,10,15,20,25,30,35,40,45,50,55 past each hour |
| Every 15 minutes | `*/15 * * * *` | 0,15,30,45 past each hour |
| Every 30 minutes | `*/30 * * * *` or `0,30 * * * *` | 0,30 past each hour |
| Every hour | `0 * * * *` or `@hourly` | Top of every hour (XX:00) |
| Every 2 hours | `0 */2 * * *` | 0:00, 2:00, 4:00, 6:00, ... |
| Every 6 hours | `0 */6 * * *` | 0:00, 6:00, 12:00, 18:00 |
| Daily at midnight | `0 0 * * *` or `@daily` or `@midnight` | 12:00 AM every day |
| Daily at 2:30 AM | `30 2 * * *` | 2:30 AM every day |
| Daily at 2 AM | `0 2 * * *` | 2:00 AM every day (common for backups) |
| Twice daily | `0 9,21 * * *` | 9:00 AM and 9:00 PM |
| Every weekday 9 AM | `0 9 * * 1-5` | Monday-Friday at 9:00 AM |
| Every Sunday 3 AM | `0 3 * * 0` or `0 3 * * 7` | Weekly on Sunday at 3:00 AM |
| Every Monday 5 AM | `0 5 * * 1` | Weekly on Monday at 5:00 AM |
| First of month | `0 0 1 * *` or `@monthly` | Midnight on the 1st of each month |
| Business hours | `0 9-17 * * 1-5` | Hourly, 9 AM-5 PM, Monday-Friday |
| At boot | `@reboot` | Once when system starts |
| Weekly | `0 0 * * 0` or `@weekly` | Sunday at midnight |
| Quarterly | `0 0 1 */3 *` | 1st of Jan, Apr, Jul, Oct |
| Twice per hour | `0,30 * * * *` | :00 and :30 of every hour |

---

## Next Steps

**🎉 You've completed Day 13!** You now know how to:
- View and manage Linux processes (ps, top, kill, nice)
- Schedule recurring tasks with cron (including complex patterns)
- Schedule one-time jobs with at
- Handle periodic tasks with anacron
- Troubleshoot scheduling issues (logs, permissions, environment)
- Prevent job overlap and conflicts
- Understand process states and signals

**📚 Proceed to Day 14: System Monitoring & Log Management** to learn:
- System resource monitoring (CPU, memory, disk, network)
- Log file locations and formats
- Log analysis with grep, awk, sed
- Log rotation with logrotate
- Performance troubleshooting and metrics
- Real-time monitoring tools

**💪 Practice Challenge:**

Create a complete backup automation system:

1. **Script Requirements:**
   - Backs up `~/day13_test` to `~/backups/` with timestamp
   - Compresses with tar and gzip
   - Deletes backups older than 7 days
   - Logs success/failure to `~/day13_test/logs/backup.log`
   - Sends email on failure (bonus)

2. **Scheduling:**
   - Runs daily at 3 AM via cron
   - Uses flock to prevent overlap
   - Redirects all output to log file

3. **Testing:**
   - Test manually first
   - Verify permissions
   - Check logs after each run
   - Confirm old backups are deleted

**Solution Hint:**
```bash
# Create backup script
cat > ~/day13_test/scripts/full-backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/backups
SOURCE=~/day13_test
LOG=~/day13_test/logs/backup.log
DATE=$(date +%Y%m%d_%H%M%S)

echo "========================================" >> "$LOG"
echo "Backup started at $(date)" >> "$LOG"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
if tar -czf "$BACKUP_DIR/day13_backup_$DATE.tar.gz" -C ~ day13_test/ >> "$LOG" 2>&1; then
    echo "✓ Backup successful: day13_backup_$DATE.tar.gz" >> "$LOG"
else
    echo "✗ Backup failed!" >> "$LOG"
    exit 1
fi

# Delete old backups (older than 7 days)
find "$BACKUP_DIR" -name "day13_backup_*.tar.gz" -mtime +7 -delete
echo "✓ Old backups cleaned" >> "$LOG"

echo "Backup finished at $(date)" >> "$LOG"
EOF

chmod +x ~/day13_test/scripts/full-backup.sh

# Add to crontab
crontab -e
# Add this line:
0 3 * * * flock -n /tmp/backup.lock ~/day13_test/scripts/full-backup.sh

# Test manually
~/day13_test/scripts/full-backup.sh
cat ~/day13_test/logs/backup.log
ls -lh ~/backups/
```

---

**📌 Day 13 Complete!** ✓

**Key Takeaways:**
1. Processes are managed with ps, top, kill, and nice
2. Cron automates recurring tasks with flexible time patterns
3. At handles one-time scheduled jobs
4. Anacron ensures periodic tasks run even on intermittent systems
5. Always use absolute paths and log output in cron jobs
6. Prevent overlap with flock or process checks
7. Troubleshoot with logs, manual testing, and environment debugging

**Move to Day 14 when ready!** 🚀
