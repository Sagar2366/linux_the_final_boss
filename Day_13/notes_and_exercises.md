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
- Master cron for recurring task scheduling
- Use at for one-time job scheduling
- Understand anacron for periodic tasks
- Troubleshoot scheduled jobs
- Implement automated system maintenance

**Estimated Time:** 3-4 hours

## Notes
- **Why Scheduling Matters:**
  - Automates repetitive tasks, backups, monitoring, and maintenance.
  - Essential for DevOps, SRE, and system admins.

- **Process Management Recap:**
  - `ps`, `top`, `htop`, `kill`, `nice`, `renice`, `jobs`, `fg`, `bg` (see Day 8)

- **Job Scheduling Tools:**
  - `cron`: Schedule recurring tasks
    - Edit with `crontab -e`
    - Syntax: `* * * * * command` (min, hour, day, month, weekday)
    - List: `crontab -l`; Remove: `crontab -r`
    - System-wide: `/etc/crontab`, `/etc/cron.*`
  - `at`: Schedule one-time tasks
    - `at 10:00` (then enter commands, Ctrl+D to finish)
    - List: `atq`; Remove: `atrm <job#>`
  - `anacron`: Run periodic jobs not guaranteed to run at set times (good for laptops)
    - Config: `/etc/anacrontab`

```mermaid
flowchart TD
    A[Job Scheduling] --> B[cron<br>Recurring Tasks]
    A --> C[at<br>One-time Tasks]
    A --> D[anacron<br>Periodic Tasks]
    
    B --> B1[crontab -e]
    B --> B2[Cron Syntax<br>min hour day month weekday]
    B --> B3[System cron<br>/etc/crontab]
    
    C --> C1[at 10:00]
    C --> C2[atq - list jobs]
    C --> C3[atrm - remove job]
    
    D --> D1["/etc/anacrontab"]
    D --> D2[Handles missed jobs]
    
    B2 --> E[Daily Backup<br>0 2 * * *]
    B2 --> F[Every 5 min<br>*/5 * * * *]
    B2 --> G[Weekly Task<br>0 0 * * 0]
    
    style A fill:#f96
    style B fill:#9f6
    style C fill:#69f
    style D fill:#f69
```

- **Crontab Examples:**
  - `0 2 * * * /usr/bin/backup.sh` — Run daily at 2am
  - `*/5 * * * * /usr/bin/check.sh` — Every 5 minutes

- **Best Practices:**
  - Use absolute paths in cron jobs
  - Redirect output to log files for troubleshooting
  - Test jobs manually before scheduling
  - Document scheduled tasks



- **Cron Syntax Examples:**
  ```bash
  # Format: min hour day month weekday command
  0 2 * * * /backup.sh              # Daily at 2 AM
  */15 * * * * /check.sh            # Every 15 minutes
  0 0 * * 0 /weekly.sh              # Weekly on Sunday
  0 9-17 * * 1-5 /business.sh       # Business hours weekdays
  
  # Special strings
  @reboot /startup.sh               # At boot
  @daily /daily.sh                  # Once per day
  @hourly /hourly.sh                # Once per hour
  ```

- **Process Management Commands:**
  ```bash
  # View processes
  ps aux | grep process_name
  pgrep -f process_name
  top -p PID
  
  # Control processes
  kill PID
  kill -9 PID                       # Force kill
  killall process_name
  pkill -f pattern
  
  # Process priority
  nice -n 10 command                # Start with lower priority
  renice 5 -p PID                   # Change priority
  ```

## Sample Exercises
1. Schedule a script to run every day at midnight using cron.
2. Schedule a one-time job to run 10 minutes from now using `at`.
3. List all current user's cron jobs.
4. Set up an anacron job to run a script daily.
5. Redirect cron job output to a log file.

## Solutions
1. **Daily cron job:**
   ```bash
   # Create script
   vi /path/to/script.sh 
   # Add these content in the script.sh
   '#!/bin/bash
    echo "Cron executed successfully" > /tmp/hello.txt'
   chmod +x /path/to/script.sh
   crontab -e
   # Add: 0 0 * * * /path/to/script.sh
   # Check if cronjob is installed
   crontab -l
   # Check if the txts are generating 
   cat /tmp/hello.txt
   # Check cron logs if it does not run
   grep CRON /var/log/syslog # Ubuntu/Debian
   grep CRON /var/log/cron # CentOS/RHEL
   ```

2. **One-time at job:**
   ```bash
   echo "/path/to/script.sh" | at now + 10 minutes
   at 14:30 tomorrow
   /path/to/script.sh
   Ctrl+D
   ```

3. **List cron jobs:**
   ```bash
   crontab -l
   sudo crontab -l -u username
   ```

4. **Anacron job:**
   ```bash
   anacron -V # Check anacron version and install if not installed 
   sudo vim /etc/anacrontab
   # Add: 1 5 myjob /path/to/script.sh
   grep anacron /var/log/syslog # Ubuntu/Debian
   grep anacron /var/log/cron # CentOS/RHEL
   ```

5. **Cron with logging:**
   ```bash
   vi myscript.sh # Create a script
   chmod +x myscript.sh
   Add the below
   '#!/bin/bash
   echo "Script started at $(date)"
   # Your commands here
   echo "Script ended at $(date)"'
   crontab -e
   0 0 * * * /path/to/myscript.sh > /var/log/script.log 2>&1
   # Check cron logs if it does not run
   grep CRON /var/log/syslog # Ubuntu/Debian
   grep CRON /var/log/cron # CentOS/RHEL
   ```

## Sample Interview Questions
1. What is the difference between cron, at, and anacron?
2. How do you edit and list cron jobs for a user?
3. What is the crontab syntax?
4. How do you schedule a job to run every Monday at 5am?
5. How do you redirect output from a cron job?
6. What are the risks of running scripts as root in cron?
7. How do you prevent overlapping cron jobs?
8. How do you troubleshoot a cron job that isn't running?
9. Where are system-wide cron jobs defined?
10. How do you schedule a job to run only once?

## Interview Question Answers
1. **Scheduling Tools:** cron (recurring), at (one-time), anacron (periodic, handles missed jobs)
2. **Cron Management:** `crontab -e` to edit, `crontab -l` to list current user's jobs
3. **Crontab Format:** `min hour day month weekday command` (0-59 0-23 1-31 1-12 0-7)
4. **Weekly Schedule:** `0 5 * * 1 command` (Monday=1, Sunday=0 or 7)
5. **Output Redirect:** Add `> /path/to/log 2>&1` to capture stdout and stderr
6. **Root Risks:** Full system access, validate scripts, use least privilege, audit regularly
7. **Prevent Overlap:** Use flock, lock files, or check if process already running
8. **Troubleshooting:** Check logs (/var/log/cron), permissions, paths, environment variables
9. **System Jobs:** /etc/crontab, /etc/cron.d/, /etc/cron.{daily,weekly,monthly}/
10. **One-time Jobs:** Use `at` command for single execution

## Completion Checklist
- [ ] Can create and manage cron jobs
- [ ] Understand crontab syntax and timing
- [ ] Know how to use at for one-time scheduling
- [ ] Can troubleshoot failed scheduled jobs
- [ ] Understand process management commands
- [ ] Can prevent job overlap and conflicts

## Key Commands Summary
```bash
# Cron management
crontab -e                       # Edit user crontab
crontab -l                       # List cron jobs
crontab -r                       # Remove all cron jobs

# At scheduling
at 14:30                         # Schedule for 2:30 PM
at now + 1 hour                  # Schedule relative time
atq                              # List at jobs
atrm job_number                  # Remove at job

# Process control
ps aux | grep process
kill PID
killall process_name
```

## Next Steps
Proceed to [Day 14: System Monitoring & Log Management](../Day_14/notes_and_exercises.md) to learn system observability.
