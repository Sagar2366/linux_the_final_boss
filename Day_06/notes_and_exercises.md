# Day 06: Advanced Linux Commands

## Learning Objectives
By the end of Day 6, you will:
- Master advanced text processing with grep, awk, and sed, including common flags and regex patterns
- Use find and xargs for file operations with criteria like size, type, and user
- Combine commands with pipes, redirection, and xargs for powerful one-liners
- Process and manipulate text data efficiently, including counting, sorting, and transforming
- Apply these tools in real DevOps scenarios like log analysis and automation

**Estimated Time:** 1 hour

## Sample Dataset: sample.log

We'll use the following log file, `sample.log`, for all command examples and exercises:

```
2025-10-07 10:10:10 INFO  user1 192.168.0.1 Login successful
2025-10-07 10:12:15 WARN  user2 10.0.0.2 Disk space low
2025-10-07 10:13:25 ERROR user3 172.16.0.2 Failed password attempt
2025-10-07 10:15:40 INFO  user1 192.168.0.1 File uploaded
2025-10-07 10:17:50 ERROR user4 203.0.113.25 Connection lost
2025-10-07 10:18:30 INFO  user2 10.0.0.2 Logout
2025-10-07 10:19:50 INFO  user5 172.16.0.3 Login successful
2025-10-07 10:20:55 WARN  user1 192.168.0.1 High CPU usage
```

## Notes

- **Why Learn Advanced Linux Commands?**
  - These commands are essential for text processing, automation, and efficient system administration in high-volume environments like logs and configs.
  - Mastery of these tools is expected in DevOps, SRE, and system engineering interviews, where you'll debug issues or automate workflows on the fly.

## Top 6 Log Parsing Commands

| Command | Description | Examples |
|---------|-------------|----------|
| **GREP**<br>`$ grep <pattern> file.log` | Searches any given input files, selecting lines that match one or more patterns | 1. Find file names that match: `grep -l "linuxthefinalboss" *.log`<br>2. Case insensitive word match: `grep -i "linuxthefinalboss" test.log`<br>3. Show line numbers: `grep -n "linuxthefinalboss" test.log`<br>4. Invert matches: `grep -v "linuxthefinalboss" test.log`<br>5. Take patterns from a file: `grep -f pattern.txt test.log`<br>6. Search recursively in a dir: `grep -R "linuxthefinalboss" /home` |
| **CUT**<br>`$ cut -d' ' -f3 file.log` | Cuts out selected portions of each line from each file and writes them to the standard output | 1. Cut first 3 bytes: `cut -b1-3 file.log`<br>2. Select 2nd column delimited by a space: `cut -d' ' -f2 test.log`<br>3. Specify character position: `cut -c1-8 test.log` |
| **SED**<br>`$ sed /<regex>/<replace>/g` | Reads the specified files, modifying the input as specified by a list of commands | 1. Substitute a string: `sed s/linuxthefinalboss/go/g test.log`<br>2. Replace the 2nd occurrence: `sed s/linuxthefinalboss/go/2 test.log`<br>3. Replace case insensitive: `sed /linuxthefinalboss/go/I test.log`<br>4. Replace string on line range of 2-4: `sed '2,4s/linuxthefinalboss/go/' test.log`<br>5. Delete a line: `sed '4d' test.log` |
| **AWK**<br>`$ awk '{print $4}' test.log` | Scans each input file for lines that match any of a set of patterns | 1. Print matched lines: `awk /linuxthefinalboss/ {print} test.log`<br>2. Split a line into fields: `awk '{print $1 $3}' test.log`<br>3. Print lines 2 to 7: `awk 'NR>=2 && NR=7 {print NR, $0}' test.log`<br>4. Print lines with more than 10 characters: `awk 'length($0)>10' test.log`<br>5. Find a string (field=4) = "byte" print $0: `awk '$4=="byte" print $0' test.log` |
| **SORT**<br>`$ sort test.log` | Sorts text and binary files lines | 1. Output to a file: `sort -o output.txt input.txt`<br>2. Sort in reverse order: `sort -r test.log`<br>3. Sort numerically: `sort -n test.log`<br>4. Sort based on the 3rd column: `sort -k3n test.log`<br>5. Check if a file is ordered: `sort -c test.log`<br>6. Sort and remove duplicates: `sort -u test.log` |
| **UNIQ**<br>`$ uniq test.log` | Compares adjacent input lines, writing a copy of each unique input line to the output file | 1. Tell how many times a line repeats: `uniq -c test.log`<br>2. Print repeated lines: `uniq -d test.log`<br>3. Print unique lines: `uniq -u test.log`<br>4. Skip the first two fields: `uniq -f 2 test.log`<br>5. Compare case-insensitive: `uniq -i test.log`

---

### grep (Global Regular Expression Print)
**grep** searches for patterns (strings or regex) in files, outputting matching lines. Use it for log filtering, error hunting, or auditing. Supports basic/extended regex (-E) and fixed strings (-F).

```bash
# Search for ERROR log entries
grep 'ERROR' sample.log

# Case insensitive search for "login"
grep -i 'login' sample.log

# Get all lines for user1
grep 'user1' sample.log

# Show line numbers for WARN
grep -n 'WARN' sample.log

# Count matching lines
grep -c 'INFO' sample.log

# Invert match: Show non-ERROR lines
grep -v 'ERROR' sample.log

# Recursive search in directory
grep -r 'ERROR' /var/log/

# List files with matches (no content)
grep -l 'Disk space low' *.log

# Extended regex: Match IPs (basic example)
grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' sample.log
```

---

### awk
**awk** processes text by records (lines) and fields (space-separated by default). Use patterns/actions for filtering, math, and formatting. FS (field separator) and OFS (output separator) are customizable.

```bash
# Print the username and IP address columns
awk '{print $4, $5}' sample.log

# Print only ERROR log lines' usernames
awk '$3 == "ERROR" {print $4}' sample.log

# Count number of lines per log level
awk '{count[$3]++} END {for (level in count) print level, count[level]}' sample.log

# Sum timestamps (assuming numeric) for INFO lines
awk '$3 == "INFO" {sum += $2} END {print "Total INFO seconds:", sum}' sample.log

# Change field separator to tab for output
awk -F' ' 'OFS="\t" {print $4, $5}' sample.log

# BEGIN/END blocks: Header and total count
awk 'BEGIN {print "Log Analysis"} {print $0; total++} END {print "Total lines:", total}' sample.log

# Match pattern: Lines with IP starting with 192
awk '/^192/ {print $4}' sample.log
```

---

### sed (Stream Editor)
**sed** edits streams/files non-interactively: substitute, delete, insert, or transform. Use -i for in-place edits (with backup via -i.bak). Chain commands with -e.

```bash
# Replace "user1" with "admin"
sed 's/user1/admin/g' sample.log

# Delete all INFO lines
sed '/INFO/d' sample.log

# Print lines 2 to 5
sed -n '2,5p' sample.log

# In-place replace (backup to .bak)
sed -i.bak 's/user1/admin/g' sample.log

# Multiple edits: Replace user1 and add prefix to ERROR
sed -e 's/user1/admin/g' -e 's/^ERROR/ALERT: ERROR/g' sample.log

# Insert line before matching pattern
sed '/ERROR/i\--- SECURITY ALERT ---' sample.log

# Global substitute with regex: Change all IPs starting with 10 to 192
sed 's/10\.[0-9]\+\.[0-9]\+\.[0-9]\+/192.168.0.X/g' sample.log
```

---

### find & xargs
**find** locates files/directories by criteria (name, type, size, time, permissions). **xargs** reads stdin to build/execute commands, handling args safely (e.g., -0 for null-separated input).

Assume you have several log files in your current directory (sample.log, app.log, system.log):

```bash
# Find all .log files in current directory
find . -name '*.log'

# Search for "ERROR" in all .log files
find . -name '*.log' -exec grep 'ERROR' {} +

# Remove all .log files containing "Disk space low"
grep -l 'Disk space low' *.log | xargs rm

# Find files larger than 1MB
find . -name '*.log' -size +1M

# Find files owned by user 'root', modified in last 7 days
find /var/log -user root -mtime -7

# Use xargs with placeholder for complex args
find . -name '*.log' | xargs -I {} grep -c 'ERROR' {}

# xargs with null delimiter (safer for filenames with spaces)
ls *.log | xargs -0 rm

# Combine: Grep in found files, then count total matches
find . -name '*.log' -exec grep -l 'ERROR' {} + | xargs wc -l
```

---

### cut, sort, uniq, tr
- **cut** extracts sections: -d for delimiter, -f for fields, -c for characters.
- **sort** orders: -n numeric, -r reverse, -k key field, -u unique.
- **uniq** deduplicates: -c count, -i ignore case, -d duplicates only.
- **tr** transforms: -d delete, -s squeeze repeats, -c complement set.

These are essential for extracting and cleaning up data.

```bash
# Extract only IP addresses (column 5)
cut -d' ' -f5 sample.log

# Show unique usernames
awk '{print $4}' sample.log | sort | uniq

# Count unique IP addresses
awk '{print $5}' sample.log | sort | uniq | wc -l

# Convert usernames and log levels to uppercase
awk '{print $3, $4}' sample.log | tr 'a-z' 'A-Z'

# cut characters: First 10 chars per line
cut -c1-10 sample.log

# sort numeric by timestamp (column 2)
cut -d' ' -f2 sample.log | sort -n

# uniq with count and ignore case
echo -e "User\nuser\nUser" | sort | uniq -i -c

# tr delete newlines and squeeze spaces
tr -d '\n' < sample.log | tr -s ' '
```

---

## Extract IP Addresses

Extracting IP addresses from log files is a common task, whether working with web server logs or application logs. This can be done with awk (field extraction) or grep (regex matching).

### Example 1: Web server logs (access.log)

```bash
# Sample log entries (web server format)
echo "172.16.0.2 - - [01/Oct/2025:19:10:00 +0530] \"GET /about HTTP/1.1\" 200 2048" >> access.log
echo "203.0.113.25 - - [01/Oct/2025:19:15:00 +0530] \"POST /submit HTTP/1.1\" 404 256" >> access.log

# Method 1: Using grep with regex pattern to extract IP addresses
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log

# Method 2: Using awk to extract the first field (IP address)
awk '/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/ {print $1}' access.log

# Count unique IPs
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log | sort | uniq -c
```

### Example 2: Course sample logs (sample.log)

We'll use the provided sample.log (see top of these notes) for all course command demos.

```bash
# Extract IP addresses (column 5) using awk
awk '{print $5}' sample.log

# Extract IP addresses with grep regex (matches any IP-like pattern)
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' sample.log

# Extract only unique IP addresses
awk '{print $5}' sample.log | sort | uniq

# Filter IPs starting with 192 using cut and grep
cut -d' ' -f5 sample.log | grep '^192'
```

---

## Sample Exercises

1. Search for all ERROR log entries and count them.
2. Print all unique usernames found in the logs, sorted reverse-alphabetically.
3. Replace every "user1" with "admin" in the log file (in-place with backup).
4. Count how many times each log level appears, sorted by count descending.
5. Extract all unique IP addresses and count their occurrences.
6. Extract all IP addresses from sample.log and from access.log (if available), then merge and deduplicate.
7. Print lines 3 through 6 of the sample.log file using both sed and awk.
8. Delete all INFO entries from the log file (output to a new file) and uppercase the remaining log levels.
9. Find all .log files modified in the last day and grep for "ERROR" in them.
10. Use tr to remove all vowels from usernames in the logs.

---

## Solutions

1. **Search for ERROR log entries and count:**
   ```bash
   grep 'ERROR' sample.log
   grep -c 'ERROR' sample.log
   ```

2. **Print unique usernames, sorted reverse:**
   ```bash
   awk '{print $4}' sample.log | sort | uniq | sort -r
   ```

3. **Replace every "user1" with "admin" (in-place with backup):**
   ```bash
   sed -i.bak 's/user1/admin/g' sample.log
   ```

4. **Count log levels, sorted by count descending:**
   ```bash
   awk '{count[$3]++} END {for (level in count) print level, count[level]}' sample.log | sort -k2 -nr
   ```

5. **Extract unique IPs with counts:**
   ```bash
   awk '{print $5}' sample.log | sort | uniq -c
   ```

6. **Extract and merge IPs:**
   - From sample.log:
     ```bash
     awk '{print $5}' sample.log
     grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' sample.log
     ```
   - From access.log:
     ```bash
     grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log
     awk '/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/ {print $1}' access.log
     ```
   - Merge and dedup:
     ```bash
     (awk '{print $5}' sample.log; grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log) | sort | uniq
     ```

7. **Print lines 3 through 6:**
   ```bash
   sed -n '3,6p' sample.log
   awk 'NR >= 3 && NR <= 6' sample.log
   ```

8. **Delete INFO and uppercase levels:**
   ```bash
   sed '/INFO/d' sample.log | awk '{ $3 = toupper($3); print }' > no_info_sample.log
   ```

9. **Find recent .log files and grep ERROR:**
   ```bash
   find . -name '*.log' -mtime -1 -exec grep 'ERROR' {} +
   ```

10. **Remove vowels from usernames:**
    ```bash
    awk '{ gsub(/[aeiou]/, "", $4); print $4 }' sample.log | tr -d '\n'
    ```

---

## Completion Checklist
- [ ] Can use grep with options like -i, -v, -c, -l, -r, -E for flexible searching
- [ ] Understand awk for column processing, patterns, BEGIN/END, and custom separators
- [ ] Use sed for text replacement, deletion, insertion with -i, -e, and regex
- [ ] Master find for file searching with criteria like -name, -type, -size, -mtime, -user
- [ ] Combine commands with pipes, xargs (-I, -0), and redirection for workflows
- [ ] Can create complex one-liners for data processing, including sort/uniq/tr variants

---

## Key Command Combinations

```bash
# Find all ERROR lines and show unique users
grep 'ERROR' sample.log | awk '{print $4}' | sort | uniq

# Count how many times each IP appears, sorted
awk '{print $5}' sample.log | sort | uniq -c | sort -nr

# Remove all .log files older than 7 days
find . -name "*.log" -mtime +7 | xargs rm

# Recursive grep in logs, count per file
grep -r 'ERROR' /var/log/*.log | awk -F: '{print $1}' | sort | uniq -c

# Extract, transform, and summarize: IPs to uppercase, unique count
awk '{print $5}' sample.log | tr 'a-z' 'A-Z' | sort | uniq | wc -l
```

---

## Best Practices
- Test commands on sample data first to avoid data loss
- Use `--help` or `man` pages (e.g., `man grep`) to explore options quickly
- Combine simple commands for complex tasks—pipes are your friend for readability
- Use `-i` flags carefully (they modify files in place); always specify backups
- Quote patterns to handle spaces/special chars: `grep "pattern with space"`
- For large files, consider `grep -F` for literals and `awk` for computations to optimize
- Always backup important files before bulk operations like find/xargs rm

---

## Sample Interview Questions

1. How do you search for a specific word in a log file, case-insensitively?
2. How do you print specific columns from a text file using awk?
3. How do you replace text in a file using sed, in-place?
4. How do you count unique entries in a column, with occurrences?
5. How do you process multiple files matching a pattern with find and exec?
6. How do you delete lines containing a certain pattern with sed?
7. How do you combine commands to get unique IPs from error logs?
8. How do you use tr for string manipulation, like deleting characters?
9. How do you print a range of lines from a file with sed or awk?
10. How do you chain commands with pipes for sorting and deduping?
11. What's the difference between grep -exec and xargs?
12. How would you find and compress all .log files over 10MB?

---

## Interview Question Answers

1. `grep -i 'word' sample.log`
2. `awk '{print $2, $4}' sample.log`
3. `sed -i 's/oldtext/newtext/g' sample.log`
4. `awk '{print $4}' sample.log | sort | uniq -c`
5. `find . -name '*.log' -exec command {} +`
6. `sed '/pattern/d' sample.log`
7. `grep 'ERROR' sample.log | awk '{print $5}' | sort | uniq`
8. `echo "text" | tr -d 'aeiou'` (deletes vowels)
9. `sed -n '3,6p' sample.log` or `awk 'NR>=3 && NR<=6' sample.log`
10. `grep 'ERROR' sample.log | awk '{print $4}' | sort | uniq`
11. `-exec` runs command per file (slower for many); `xargs` batches args (faster, handles large input).
12. `find . -name '*.log' -size +10M -exec gzip {} +`

---
## Next Steps
Proceed to [Day 7: Users, Groups & Permissions](../Day_07/notes_and_exercises.md) to learn user management and security.
