# Day 05: Basic Linux Commands for DevOps Engineers

## Table of Contents

- [Day 05: Basic Linux Commands for DevOps Engineers](#day-05-basic-linux-commands-for-devops-engineers)
  - [Learning Objectives](#learning-objectives)
  - [Why Learn Basic Linux Commands?](#why-learn-basic-linux-commands)
  - [1. Navigation & System Information](#1.-navigation-&-system-information)
  - [2. File & Directory Operations](#2.-file-&-directory-operations)
  - [3. Viewing & Inspecting File Content](#3.-viewing-&-inspecting-file-content)
  - [4. Searching & Finding](#4.-searching-&-finding)
  - [5. Wildcards (Globbing)](#5.-wildcards-globbing)
  - [6. Aliases & Shell Productivity](#6.-aliases-&-shell-productivity)
  - [7. Command History & Reuse](#7.-command-history-&-reuse)
  - [8. Comparison & Inspection Utilities](#8.-comparison-&-inspection-utilities)
  - [9. Safety & Validation Patterns](#9.-safety-&-validation-patterns)
  - [10. Performance & Scaling Considerations](#10.-performance-&-scaling-considerations)
  - [11. Advanced Quick Win Commands](#11.-advanced-quick-win-commands)
- [Count unique IPs in access log](#count-unique-ips-in-access-log)
- [Files bigger than 50MB](#files-bigger-than-50mb)
- [Last 5 commands you ran](#last-5-commands-you-ran)
- [Show only usernames from /etc/passwd](#show-only-usernames-from-etcpasswd)
  - [Mini Hands-On Lab: Build a Workspace](#mini-hands-on-lab-build-a-workspace)
  - [Common Mistakes & How to Avoid Them](#common-mistakes-&-how-to-avoid-them)
  - [Sample Exercises](#sample-exercises)
  - [Solutions](#solutions)
- [1](#1)
- [2](#2)
- [3](#3)
- [4](#4)
- [5](#5)
- [6](#6)
- [7](#7)
- [8](#8)
- [9](#9)
- [10](#10)
  - [Completion Checklist](#completion-checklist)
  - [Key Commands Summary (Revision)](#key-commands-summary-revision)
    - [Navigation](#navigation)
    - [File & Directory Operations](#file-&-directory-operations)
    - [Viewing & Inspecting](#viewing-&-inspecting)
    - [Searching & Finding](#searching-&-finding)
    - [Comparison & Inspection](#comparison-&-inspection)
    - [Productivity & History](#productivity-&-history)
    - [Safety & Validation](#safety-&-validation)
    - [Quick Wins & One-Liners](#quick-wins-&-one-liners)
  - [Best Practices](#best-practices)
  - [Sample Interview Questions](#sample-interview-questions)
    - [Interview Answers](#interview-answers)
  - [Next Steps](#next-steps)


## Learning Objectives
By the end of Day 5, you will:
- Master essential Linux navigation and file operations
- Use core commands for system and environment awareness
- Confidently view, search, compare, and organize files
- Leverage history, tab completion, and wildcards for speed
- Create reusable shortcuts with aliases
- Apply safe deletion and inspection habits

**Estimated Time:** 1 hour

---

## Why Learn Basic Linux Commands?
These fundamentals are the daily tools of DevOps, SRE, cloud, and platform engineers. They let you:
- Navigate unfamiliar systems quickly
- Troubleshoot with precision
- Automate reliably (Bash, Ansible, pipelines)
- Reduce mistakes in production environments

---

## 1. Navigation & System Information
This category helps you orient yourself: Where am I? Who am I? What system am I on? It establishes context before making changes.

| Command | Purpose | Example / Notes |
|---------|---------|-----------------|
| `pwd` | Show absolute current directory | Always verify before destructive ops |
| `ls -l` | Long listing (permissions, owner, size, time) | Add `-h` for human sizes |
| `ls -a` | Include hidden `.` files | Dotfiles store configs |
| `ls -lah` | Combined useful view | Common alias target (`ll`) |
| `ls -R` | Recursive listing | Avoid in huge dirs |
| `cd dir` | Change directory | `cd /etc` |
| `cd -` | Previous directory | Toggle quickly |
| `cd ~` | Home directory | `~user` targets another user |
| `whoami` | Current user | Combine with `id` for groups |
| `date` | System date/time | Format: `date "+%F %T"` |
| `cal` | Calendar view | `cal 2026` |
| `uname -r` | Kernel version | For module compatibility |
| `uname -m` | Architecture | `x86_64`, `aarch64` |
| `uname -a` | Full system string | Kernel + host + arch |
| `history` | Show history | Pipe to `tail` for recent |
| `clear` / `Ctrl+L` | Clear terminal | Visual reset |

---

## 2. File & Directory Operations
Core CRUD actions (create, copy, move, delete). Precision here prevents data loss and supports repeatable workflows.

| Command | Action | Example / Notes |
|---------|--------|-----------------|
| `touch file` | Create empty file / update timestamp | Placeholder creation |
| `mkdir dir` | Create directory | Fails if parent missing |
| `mkdir -p a/b/c` | Create nested structure | No error if exists |
| `cp src dest` | Copy file | Overwrites unless `-i` |
| `cp -r dir1 dir2` | Recursive copy | Copies tree |
| `cp -i` | Interactive copy | Prompts before overwrite |
| `cp -u` | Copy only if newer | Sync-style copy |
| `mv old new` | Rename / move | Atomic same FS |
| `mv -i` | Prompt before overwrite | Safety habit |
| `rm file` | Delete file | Irreversible |
| `rm -r dir` | Recursive delete | Use caution |
| `rm -rf dir` | Force recursive delete | NEVER in `/` |
| `rmdir emptydir` | Remove empty dir | Clean scaffolding |
| `ln -s target link` | Create symlink | Inspect with `ls -l` |

---

## 3. Viewing & Inspecting File Content
See what’s inside without overwhelming the terminal.

| Command | Purpose | Example / Notes |
|---------|---------|-----------------|
| `cat file` | Print full file | Small files only |
| `less file` | Scroll & search pager | `/pattern`, `q` to quit |
| `more file` | Basic pager | Prefer `less` |
| `head -n 20 file` | First N lines | Default = 10 |
| `tail -n 50 file` | Last N lines | Quick endings |
| `tail -f file` | Follow appended lines | Log monitoring |
| `nl file` | Add line numbers | For reference |
| `wc -l file` | Count lines | With `-w` words |
| `cut -d: -f1 /etc/passwd` | Extract fields | Delimited data parsing |

---

## 4. Searching & Finding
Locate text patterns or files across the system.

| Command | Purpose | Example / Notes |
|---------|---------|-----------------|
| `grep pattern file` | Search in file | Case-sensitive |
| `grep -i pattern file` | Case-insensitive search | Logs vary |
| `grep -n pattern file` | Include line numbers | Easier referencing |
| `grep -r pattern dir` | Recursive search | Tree-wide |
| `grep -v pattern file` | Exclude matches | Filter noise |
| `grep -E "a|b"` | Extended regex | Alternation |
| `grep -F text file` | Fixed string (fast) | No regex parsing |
| `find path -name "*.log"` | Find by name | Glob style |
| `find . -type f -size +10M` | Files bigger than 10MB | Capacity triage |
| `find . -mtime -1` | Modified last 24h | Fresh changes |
| `find . -exec cmd {} \;` | Run per file | Use `+` to batch |
| `locate nginx.conf` | Indexed filename search | Needs updatedb |
| `diff -u old new` | Show differences | Patch-ready |
| `cmp f1 f2` | Binary compare | Silent unless different |
| `xargs` | Build command pipelines | `... \| xargs rm` |

---

## 5. Wildcards (Globbing)
Filename expansion handled by the shell before execution.

| Pattern | Matches | Notes |
|---------|---------|-------|
| `*` | Any string (including empty) | Broadest |
| `?` | Single character | One position |
| `[abc]` | One of a, b, c | Character sets |
| `[0-9]` | Any digit | Ranges supported |
| `[!x]` | Not x (bash) | Negation |
| `{dev,prod}.conf` | `dev.conf`, `prod.conf` | Brace expansion |
| `*.{log,txt}` | Multi-extension match | Combines globs |

Dry-run globs:
```bash
echo *.log
```

---

## 6. Aliases & Shell Productivity
Shortcuts reduce keystrokes and encode safe defaults.

| Command / Concept | Purpose | Example / Notes |
|-------------------|---------|-----------------|
| `alias` | List all aliases | Inventory |
| `alias ll='ls -l'` | Define alias | Session only |
| `unalias ll` | Remove alias | Temporary removal |
| Persist alias | Save in `~/.bashrc` | Append & `source` |
| `source ~/.bashrc` | Reload config | Apply new aliases |
| `set -o vi` | vi key bindings | Modal editing |
| `set -o emacs` | Emacs bindings | Default bash mode |

---

## 7. Command History & Reuse
Powerful repetition & correction tools.

| Command / Shortcut | Purpose | Example / Notes |
|--------------------|---------|-----------------|
| `history` | Show history list | Indexed lines |
| `!42` | Run history entry 42 | Check first |
| `!!` | Repeat last command | `sudo !!` common |
| `!grep` | Last command starting with grep | Pattern recall |
| `Ctrl+R` | Reverse search | Interactive lookup |
| `Alt+.` | Insert last argument | Cycle on repeat |
| `history -c` | Clear history | Privacy use |
| `HISTSIZE` / `HISTFILESIZE` | History length | Set in rc file |

---

## 8. Comparison & Inspection Utilities
Assess differences and usage patterns.

| Command | Purpose | Example / Notes |
|---------|---------|-----------------|
| `diff -u f1 f2` | Unified diff view | For reviews/patches |
| `wc -l file` | Line count | Add `-w` or `-c` |
| `du -sh dir` | Directory size summary | Human readable |
| `df -h` | Filesystem usage | Mounted volumes |
| `stat file` | Metadata details | Access/change times |
| `file binary` | Detect file type | Magic headers |
| `md5sum file` | Legacy checksum | Not secure |
| `sha256sum file` | Strong hash | Integrity check |

---

## 9. Safety & Validation Patterns
Validate before irreversible actions.

| Pattern | Purpose | Example |
|---------|---------|--------|
| `pwd` | Confirm directory | Before `rm -rf` |
| `ls -ld target/` | Inspect target path | Avoid typos |
| `du -sh target/` | Size impact awareness | Before archiving |
| `cp file{,.bak}` | Quick backup | Creates `file.bak` |
| `echo rm -rf *.log` | Preview expansion | Safety check |
| `find . -name "*.tmp"` | Preview deletion set | Add `-delete` later |
| `nginx -t` | Config test | Before restart |
| `grep -i error logfile` | Scan for issues | Troubleshooting |

---

## 10. Performance & Scaling Considerations
Choose tools that scale efficiently.

| Need | Command | Reason |
|------|---------|-------|
| Fast literal search | `grep -F pattern file` | Skips regex engine |
| Filter huge trees | `find ... -maxdepth N` | Limits traversal |
| Real-time filtering | `tail -f file | grep --line-buffered PATTERN` | Streams matches |
| Count occurrences | `grep -c pattern file` | Built-in tally |
| Large file paging | `less file` | Streams content |
| Batch operations | `xargs -r -n` | Fewer forks |

---

## 11. Advanced Quick Win Commands
High-leverage one-liners for instant insight.

| Goal | Command | Explanation |
|------|---------|-------------|
| Top client IPs by frequency | `awk '{print $1}' access.log \| sort \| uniq -c \| sort -nr \| head` | Counts first field occurrences |
| Files over 50MB | `find . -type f -size +50M -exec ls -lh {} \;` | Locates large files with readable sizes |
| Last 5 commands | `history \| tail -5` | Quick recall |
| List usernames only | `cut -d: -f1 /etc/passwd \| head` | Parses first field |
| Total log lines | `cat *.log 2>/dev/null \| wc -l` | Aggregates line counts |
| Most common words | `tr -cs '[:alnum:]' '\n' < file \| tr A-Z a-z \| sort \| uniq -c \| sort -nr \| head` | Normalizes & ranks |
| Open listening ports | `ss -tuln` | Socket summary |
| Largest directories (top 5) | `du -sh * 2>/dev/null \| sort -hr \| head -5` | Disk usage hotspots |
| Executable scripts | `find . -type f -perm -111` | Any execute bit |
| Trailing whitespace lines | `grep -R "[[:blank:]]$" .` | Code hygiene |

Raw snippet:
```bash
# Count unique IPs in access log
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head

# Files bigger than 50MB
find . -type f -size +50M -exec ls -lh {} \;

# Last 5 commands you ran
history | tail -5

# Show only usernames from /etc/passwd
cut -d: -f1 /etc/passwd | head
```

---

## Mini Hands-On Lab: Build a Workspace
1. Create base structure:
   ```bash
   mkdir -p devops_lab/{logs,data,scripts}
   touch devops_lab/{README.md,.env}
   ```
2. Populate log:
   ```bash
   echo "INFO: start $(date)" >> devops_lab/logs/app.log
   echo "ERROR: failed connection" >> devops_lab/logs/app.log
   echo "WARN: retrying" >> devops_lab/logs/app.log
   ```
3. Extract errors:
   ```bash
   grep -i error devops_lab/logs/app.log
   ```
4. Count lines:
   ```bash
   wc -l devops_lab/logs/app.log
   ```
5. Copy + verify:
   ```bash
   cp devops_lab/logs/app.log devops_lab/logs/app.log.bak
   diff -u devops_lab/logs/app.log devops_lab/logs/app.log.bak
   ```
6. Simulate rotation:
   ```bash
   mv devops_lab/logs/app.log devops_lab/logs/app.log.1
   touch devops_lab/logs/app.log
   tail -f devops_lab/logs/app.log
   ```
7. Clean carefully:
   ```bash
   find devops_lab/logs -name "*.bak"
   ```

---

## Common Mistakes & How to Avoid Them
| Mistake | Risk | Prevention |
|---------|------|-----------|
| `rm -rf tmp` typo | Data loss | `ls` first |
| `cp -r /etc /etc_backup` confusion | Overwrite | Mind trailing slashes |
| `cat huge.log` | Flooded terminal | Use `less` |
| `grep pattern *` | Noise, slow | `grep -r --include="*.log"` |
| Unquoted vars | Unexpected expansion | Quote: `"$var"` |
| Overwritten config | No rollback | `cp file{,.bak}` |

---

## Sample Exercises
1. List all files, including hidden ones, in your home directory.  
2. Create a directory, add a file, copy and rename it, then delete both.  
3. View the first and last 10 lines of `/etc/passwd`.  
4. Search for the word `root` in `/etc/passwd`.  
5. Create an alias to list files in long format and use it.  
6. Find `.log` files in `/var/log` modified in last 24 hours.  
7. Count how many users have `/bin/bash` as their shell.  
8. Show lines in `/etc/passwd` that do NOT contain `/bin/false`.  
9. Preview which `*.tmp` files would be deleted.  
10. Compare two config files and show differences.  

---

## Solutions
```bash
# 1
ls -la ~

# 2
mkdir testdir
touch testdir/file.txt
cp testdir/file.txt testdir/file2.txt
mv testdir/file2.txt testdir/file3.txt
rm testdir/file3.txt
rm -r testdir

# 3
head -10 /etc/passwd
tail -10 /etc/passwd

# 4
grep root /etc/passwd
grep -n root /etc/passwd

# 5
alias ll='ls -l'
ll

# 6
find /var/log -type f -name "*.log" -mtime -1

# 7
grep "/bin/bash" /etc/passwd | wc -l

# 8
grep -v "/bin/false" /etc/passwd

# 9
echo *.tmp         # or: find . -maxdepth 1 -name "*.tmp"

# 10
diff -u config_old.conf config_new.conf
```

---

## Completion Checklist
- [ ] Can navigate with `pwd`, `cd`, `ls`
- [ ] Perform safe file/directory creation & deletion
- [ ] View content with `cat`, `less`, `head`, `tail -f`
- [ ] Search using `grep` (case, recursive, invert)
- [ ] Locate files with `find` (name, size, time)
- [ ] Use wildcards safely
- [ ] Create and persist aliases
- [ ] Reuse commands with history features
- [ ] Compare files using `diff`
- [ ] Practice safe deletion & backups
- [ ] Apply quick-win one-liners for insight

---

## Key Commands Summary (Revision)

### Navigation
| Command(s) | Purpose | Notes |
|------------|---------|-------|
| `pwd` | Show current directory | Confirm before rm |
| `ls -lah` | List with perms/sizes/hidden | Common alias |
| `cd /path`, `cd -`, `cd ~` | Change / previous / home | Speed navigation |
| `whoami`, `id` | User & identity info | Auth context |
| `uname -r`, `uname -m`, `uname -a` | Kernel / arch / full system | Env profiling |
| `history`, `clear` | Recall / reset screen | Use with filtering |

### File & Directory Operations
| Command(s) | Purpose | Notes |
|------------|---------|-------|
| `touch file` | Create empty file | Placeholder |
| `mkdir -p path` | Create nested dirs | Idempotent |
| `cp -i src dest`, `cp -r dir1 dir2` | Copy (safe) | Use `-u` for newer |
| `mv -i old new` | Rename/move | Preserve accidentally overwritten |
| `rm file`, `rm -r dir`, `rm -rf dir` | Delete (single/recursive/force) | Last is dangerous |
| `ln -s target link` | Create symlink | Relative for portability |

### Viewing & Inspecting
| Command(s) | Purpose | Notes |
|------------|---------|-------|
| `cat file` | Dump file | Small files |
| `less file` | Scroll/search | Use `/pattern` |
| `head -n N`, `tail -n N` | Beginning/end of file | Quick sampling |
| `tail -f file` | Follow changes | Logs |
| `wc -l file` | Line count | Combine pipe |
| `cut -d: -f1 file` | Extract first column | Delimited data |

### Searching & Finding
| Command(s) | Purpose | Notes |
|------------|---------|-------|
| `grep -i pattern file` | Case-insensitive search | Log analysis |
| `grep -rn pattern dir` | Recursive with line numbers | Code search |
| `grep -v pattern file` | Exclude matches | Noise reduction |
| `grep -E 'a|b'` | Extended regex | Alternation |
| `grep -F text file` | Fixed string | Fast path |
| `find . -name "*.log"` | Match by filename | Glob-style |
| `find . -type f -size +50M` | Large files | Disk triage |
| `locate file` | Index-based lookup | Needs updated DB |

### Comparison & Inspection
| Command(s) | Purpose | Notes |
|------------|---------|-------|
| `diff -u old new` | Show differences | Unified format |
| `cmp f1 f2` | Binary compare | Silent unless diff |
| `wc -l`, `wc -w` | Line / word count | Performance cheap |
| `du -sh dir` | Directory size | Human readable |
| `df -h` | Filesystem usage | Capacity watch |
| `stat file` | Metadata (times, perms) | Auditing |
| `file object` | Type detection | Non-extension-based |
| `sha256sum file` | Integrity hash | Preferred over MD5 |

### Productivity & History
| Command(s) | Purpose | Notes |
|------------|---------|-------|
| `alias ll='ls -l'` | Shortcut creation | Persist in `.bashrc` |
| `unalias name` | Remove alias | Session scope |
| `!!`, `!42`, `!grep` | Repeat by pattern/index | Shortcuts |
| `Ctrl+R` | Reverse history search | Interactive |
| `Alt+.` | Last argument insertion | Reusable paths |
| `source ~/.bashrc` | Reload shell config | Apply changes |

### Safety & Validation
| Command(s) | Purpose | Notes |
|------------|---------|-------|
| `pwd` | Confirm path | Before destructive ops |
| `ls -ld path/` | Inspect target | Avoid typos |
| `cp file{,.bak}` | Quick backup | Brace expansion |
| `echo *.tmp` | Dry-run glob | Preview match set |
| `grep -i error logfile` | Error scan | Before restart |
| `find . -name "*.tmp"` | Candidate cleanup | Append `-delete` after audit |

### Quick Wins & One-Liners
| Command(s) | Purpose | Notes |
|------------|---------|-------|
| `awk '{print $1}' access.log | sort | uniq -c | sort -nr | head` | Top IPs | Log triage |
| `find . -type f -size +50M -exec ls -lh {} \;` | Large files | Human sizes |
| `history | tail -5` | Recent commands | Audit |
| `cut -d: -f1 /etc/passwd | head` | Usernames list | Account parsing |
| `du -sh * | sort -hr | head` | Largest dirs | Disk usage |
| `tail -f log | grep --line-buffered ERROR` | Live error view | Real-time filter |
| `grep -R "TODO" . --exclude-dir=.git` | Code search | Recursively |
| `tr -cs '[:alnum:]' '\n' < file | sort | uniq -c | sort -nr | head` | Word frequency | Basic analysis |

---

## Best Practices
- Always confirm location with `pwd` before bulk operations
- Backup config before editing: `cp file{,.bak}`
- Use `less` for large files instead of `cat`
- Prefer `grep -F` for literal string searches (speed)
- Use `find ... -delete` only after verifying matches
- Pipe + page: `command | less -S` to avoid wrapping
- Use `set -o noclobber` to prevent accidental overwrites

---

## Sample Interview Questions
1. Difference between `cat` and `less`?  
2. How do you find files modified in the last day?  
3. How to search recursively for a string in code?  
4. What’s the difference between wildcards and regex?  
5. How do you count the number of users with Bash shell?  
6. How do you follow new log lines as they’re written?  
7. Explain `cp file{,.bak}` expansion.  
8. Show only usernames from `/etc/passwd`.  
9. Why use `grep -F` over `grep` sometimes?  
10. How to safely preview a delete operation using globs?  

### Interview Answers
1. `cat` dumps content; `less` provides pager navigation/search.  
2. `find /path -type f -mtime -1`  
3. `grep -r "pattern" .` (use `--include` to narrow)  
4. Globs expand by shell; regex is interpreted by tools.  
5. `grep "/bin/bash" /etc/passwd | wc -l`  
6. `tail -f /var/log/app.log`  
7. Brace expansion creates `file` and `file.bak` (backup).  
8. `cut -d: -f1 /etc/passwd`  
9. `grep -F` is faster (no regex engine) and avoids unintended pattern features.  
10. `echo *.tmp` or `find . -name "*.tmp"` before `rm`.  

---

## Next Steps
Proceed to [Day 06: Advanced Linux Commands](../Day_06/notes_and_exercises.md) to dive into redirection, pipelines, `grep` mastery, text processing (`awk`, `sed`), and automation patterns.
