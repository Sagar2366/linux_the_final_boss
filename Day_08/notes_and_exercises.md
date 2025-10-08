# Day 08: File Management & Editors (nano, vi/vim)

## Learning Objectives
By the end of Day 8, you will:
- Master advanced file operations like comparison, counting, and timestamp manipulation
- Use nano for simple, beginner-friendly text editing
- Understand vi/vim basics, modes, and commands for efficient system administration
- Manage file attributes, metadata, and extended attributes (e.g., immutable)
- Apply file compression and archiving techniques with tar and gzip
- Combine these tools for DevOps tasks like config editing and log rotation

**Estimated Time:** 1 Hour

## Notes

- **Why File Management & Editors Matter?**
  - Files are the backbone of Linux: configs, scripts, logs—everything needs safe handling and editing.
  - Editors like nano (easy) and vim (powerful) are must-haves for remote servers (no GUI).
  - Advanced ops ensure data integrity, backups, and security in DevOps pipelines.

### Top 8 File Management & Editing Commands

Quick-reference table for core tools, like Day 6's parsing table. Each has a simple description and examples for fast practice.

| Command | Simple Description | Examples |
|---------|--------------------|----------|
| **NANO**<br>`$ nano file.txt` | Beginner-friendly editor with on-screen shortcuts. | 1. Open/edit: `nano config.conf`<br>2. Search: Ctrl+W "pattern"<br>3. Save/exit: Ctrl+O, Ctrl+X |
| **VIM**<br>`$ vim file.txt` | Powerful modal editor for pros (vi-compatible). | 1. Open: `vim script.sh`<br>2. Insert mode: `i` (edit), Esc (normal)<br>3. Save/quit: `:wq` |
| **STAT**<br>`$ stat file` | Shows detailed file info (size, perms, timestamps). | 1. Basic: `stat app.conf`<br>2. Multiple: `stat *.log`<br>3. Formatted: `stat -c '%A %y %n' file` |
| **DIFF**<br>`$ diff file1 file2` | Compares two files and shows differences. | 1. Basic: `diff config1.conf config2.conf`<br>2. Unified: `diff -u file1 file2`<br>3. Side-by-side: `diff -y file1 file2` |
| **WC**<br>`$ wc file` | Counts lines, words, characters in a file. | 1. All: `wc sample.log`<br>2. Lines only: `wc -l sample.log`<br>3. Words: `wc -w script.sh` |
| **TOUCH**<br>`$ touch file` | Updates timestamps or creates empty files. | 1. Create/update: `touch newfile`<br>2. Set time: `touch -t 202501011200 file`<br>3. Copy timestamp: `touch -r ref.txt target.txt` |
| **CHATTR**<br>`$ sudo chattr +i file` | Sets extended attributes (e.g., make immutable). | 1. Immutable: `sudo chattr +i config.conf`<br>2. Remove: `sudo chattr -i config.conf`<br>3. List: `lsattr config.conf` |
| **TAR**<br>`$ tar -czf archive.tar.gz dir` | Archives/compresses files (with gzip). | 1. Create: `tar -czf backup.tar.gz test_files/`<br>2. Extract: `tar -xzf backup.tar.gz`<br>3. List: `tar -tzf backup.tar.gz` |

---

### nano Editor (Beginner-Friendly)
Nano is simple—no modes, just type. Great for quick config edits on servers.

```bash
nano filename                    # Open (creates if missing)

# Shortcuts (bottom of screen)
Ctrl+O                          # Save (Write Out)
Ctrl+X                          # Exit (confirm if unsaved)
Ctrl+W                          # Search (Where Is)
Ctrl+\                          # Search & Replace
Ctrl+K                          # Cut line
Ctrl+U                          # Paste (UnCut)
Ctrl+G                          # Help
Alt+A                           # Mark text (for copy/cut blocks)
```

**Tips:** Use for simple tasks like editing /etc/hosts. Install: `apt install nano`.

---

### vi/vim Editor (Advanced)
Vim is modal (switch modes) and keyboard-only—fast once learned. Essential for remote work.

```bash
vi filename                      # Basic vi
vim filename                     # Enhanced (syntax highlighting)

# Modes
# Normal: Default—navigate/commands (Esc to enter)
# Insert: Edit text (i to enter)
# Command: Save/search (: to enter)

# Quick Start
vim file
i                               # Insert mode (edit)
Esc                             # Normal mode
:wq                             # Command: Save & Quit
:q!                             # Quit without save

# Navigation (Normal mode)
h/j/k/l                         # Left/down/up/right
w/b                             # Word forward/back
0/$                             # Line start/end
gg/G                            # File start/end
:10                             # Go to line 10

# Editing (Normal mode)
x                               # Delete char
dd                              # Delete line
yy                              # Copy line
p                               # Paste
u                               # Undo
.                               # Repeat last action

# Search/Replace (Command mode)
/pattern                        # Search forward
n/N                             # Next/prev match
:%s/old/new/g                   # Replace all (global)
:%s/old/new/gc                  # Replace with confirm

# Advanced
:set number                     # Show line numbers
:set ignorecase                 # Case-insensitive search
:split file2                    # Edit two files side-by-side
```

**Tips:** Practice with `vimtutor`. Use for complex scripts/configs. Install: `apt install vim`.

---

### File Attributes and Archiving
Manage "hidden" file properties and bundle files for backups/transfers.

```bash
# Extended attributes
lsattr filename                  # List (e.g., i=immutable)
sudo chattr +i filename          # Set immutable (can't edit/delete)
sudo chattr -i filename          # Unset

# Archiving/Compression
tar -czf archive.tar.gz dir/     # Create compressed (c=create, z=gzip, f=file)
tar -xzf archive.tar.gz          # Extract (x=extract)
tar -tzf archive.tar.gz          # List contents
tar -cf archive.tar dir/         # Uncompressed tar
```

**Tips:** Immutable protects configs from accidental rm. Tar for backups in pipelines.

---

## Sample Exercises

1. Create a file using nano, add content, and save it.
2. Open a file in vim, navigate to a specific line, and make edits.
3. Compare two similar files and identify differences.
4. Use vim to search and replace text in a configuration file.
5. Set file attributes to make a file immutable.
6. Count lines, words, and characters in a text file.
7. Create a backup of a file with timestamp.
8. Use vim to edit multiple files simultaneously.
9. Archive a directory with tar/gzip and extract it.
10. View detailed metadata for a file and copy its timestamp to another.

---

## Solutions

1. **Create file with nano:**
   ```bash
   nano myfile.txt
   # Type content, Ctrl+O to save, Ctrl+X to exit
   cat myfile.txt                  # Verify
   ```

2. **Edit with vim:**
   ```bash
   vim filename
   :10                             # Go to line 10
   i                               # Enter insert mode
   # Make edits
   Esc                             # Exit insert mode
   :wq                             # Save and quit
   ```

3. **Compare files:**
   ```bash
   diff file1.txt file2.txt
   diff -u file1.txt file2.txt     # Unified format
   vimdiff file1.txt file2.txt     # Visual in vim
   ```

4. **Search and replace in vim:**
   ```bash
   vim config.conf
   /old_value                      # Search
   n                               # Next match
   :%s/old_value/new_value/g       # Replace all
   :wq                             # Save and quit
   ```

5. **Make file immutable:**
   ```bash
   sudo chattr +i important.conf
   lsattr important.conf           # Verify (shows ----i---------)
   sudo rm important.conf          # Fails (immutable)
   sudo chattr -i important.conf   # Unset
   ```

6. **Count file content:**
   ```bash
   wc sample.log                   # Lines words chars
   wc -l sample.log                # Lines only
   wc -w sample.log                # Words
   ```

7. **Backup with timestamp:**
   ```bash
   cp file.txt file.txt.$(date +%Y%m%d_%H%M%S).bak
   ls -l file.txt.*                # Verify
   ```

8. **Edit multiple files in vim:**
   ```bash
   vim file1.txt file2.txt
   :next                           # Switch to file2
   # Edit
   :prev                           # Back to file1
   :wa :qa                         # Save all, quit all
   ```

9. **Archive and extract:**
   ```bash
   tar -czf backup.tar.gz test_files/
   ls -lh backup.tar.gz            # Check size
   tar -xzf backup.tar.gz          # Extract
   tar -tzf backup.tar.gz          # List without extracting
   ```

10. **Metadata and timestamp copy:**
    ```bash
    stat app.conf                   # View details
    touch -r app.conf app_modified.conf  # Copy timestamp
    stat app_modified.conf          # Verify times match
    ```

---

## Completion Checklist
- [ ] Can create and edit files using nano with shortcuts
- [ ] Understand vim modes, navigation, and basic editing
- [ ] Know how to save, quit, search/replace in both editors
- [ ] Can compare files with diff and count with wc
- [ ] Manage timestamps with touch and attributes with chattr
- [ ] Archive/extract files with tar/gzip
- [ ] View file metadata with stat and file

---

## Key Command Combinations

```bash
# Quick config edit and backup
cp config.conf config.conf.bak; vim config.conf  # Backup then edit

# Compare and count changes in logs
diff -u old.log new.log | wc -l                  # Lines changed

# Immutable backup archive
sudo chattr +i important.conf; tar -czf secure.tar.gz important.conf

# Vim multi-file replace
vim *.conf; :argdo %s/old/new/g | update         # Replace in all open files

# Timestamp sync for deploys
touch -r live.conf deployed.conf; cp deployed.conf live.conf
```

---

## Best Practices
- Always backup before editing: `cp file{,.bak}` (brace expansion).
- Use `vim -R` for read-only view to avoid accidents.
- For large files, use `less` or `vim +/pattern file` to jump to search.
- Set editor default: `export EDITOR=vim` in ~/.bashrc.
- Avoid `rm` on immutable files—use `chattr -i` first.
- Compress archives: `tar -czf` (gzip) or `tar -cJf` (xz for smaller).
- Test vim: Run `vimtutor` for 15-min intro.
- Remote editing: SSH with `ssh user@host vim file` for efficiency.

---

## Sample Interview Questions

1. What is the difference between nano and vim?
2. How do you save and exit in vim?
3. What are the different modes in vim?
4. How do you search and replace text in vim?
5. What is the purpose of the `stat` command?
6. How do you make a file immutable in Linux?
7. What is the difference between `diff` and `cmp`?
8. How do you count lines in a file?
9. How do you copy timestamps from one file to another?
10. What are file ACLs and how do you manage them?
11. How do you create a compressed tar archive?
12. What's the quickest way to backup a file before editing?

---

## Interview Question Answers

1. **nano vs vim:** Nano is simple, menu-driven for beginners; vim is modal, keyboard-centric for power users (steeper curve but faster).
2. **vim Save/Exit:** `:w` (save), `:q` (quit), `:wq` or `:x` (save & quit), `:q!` (force quit, no save).
3. **vim Modes:** Normal (navigate/commands), Insert (type text), Visual (select), Command (: for save/search).
4. **vim Search/Replace:** `/pattern` (search), `n` (next); `:%s/old/new/g` (replace all globally).
5. **stat Command:** Displays file metadata (perms, size, timestamps, inode) for debugging.
6. **Immutable Files:** `sudo chattr +i file` (can't modify/delete, even by root); unset with `-i`.
7. **diff vs cmp:** `diff` compares text line-by-line (shows changes); `cmp` does byte-by-byte (binary-safe, less readable).
8. **Count Lines:** `wc -l file` or `grep -c . file` (counts non-empty lines).
9. **Copy Timestamps:** `touch -r source target` (copies access/modify times).
10. **File ACLs:** Extra perms beyond rwx for specific users/groups; manage with `setfacl -m u:user:r file` (set), `getfacl file` (view).
11. **Compressed Tar:** `tar -czf archive.tar.gz dir/` (c=create, z=gzip, f=file).
12. **Quick Backup:** `cp file{,.bak}` (brace expansion creates file.bak).

---

## Command Summary

| Category | Command | Description | Common Options/Usage |
|----------|---------|-------------|----------------------|
| **Editors** | `nano` | Simple editor | `nano file` (Ctrl+O save, Ctrl+X exit) |
| | `vim` | Advanced modal editor | `vim file` (i insert, :wq save/quit) |
| **Metadata** | `stat` | File details | `stat file` (size, perms, times) |
| | `file` | Detect type | `file binary` (text or executable?) |
| **Comparison** | `diff` | Text differences | `-u file1 file2` (unified output) |
| | `cmp` | Binary compare | `cmp file1 file2` (byte-level) |
| **Counting** | `wc` | Lines/words/chars | `-l file` (lines), `-w file` (words) |
| **Timestamps** | `touch` | Update/create | `-r source target` (copy time), `-t stamp file` (set time) |
| **Attributes** | `chattr` | Extended attrs | `+i file` (immutable), `-i file` (unset) |
| | `lsattr` | List attrs | `lsattr file` (shows flags like i) |
| **Archiving** | `tar` | Bundle/compress | `-czf archive.tar.gz dir/` (create gzip), `-xzf archive.tar.gz` (extract) |

---

## Next Steps
Proceed to [Day 9: File Transfer](../Day_09/notes_and_exercises.md) to learn secure file transfer methods like SCP and rsync.
