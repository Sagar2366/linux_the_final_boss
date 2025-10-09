# Day 08: Editors & Terminal Shortcuts (nano, vi/vim)

## Learning Objectives
By the end of Day 8, you will:
- Use nano for simple, beginner-friendly text editing
- Understand vi/vim basics, modes, and commands for efficient system administration
- Leverage terminal shortcuts for faster navigation, command reuse, and workflow efficiency

**Estimated Time:** 30 Mins

## Notes

**Why Editors & Terminal Shortcuts Matter?**
- Files are the backbone of Linux: configs, scripts, logs - everything needs safe handling and editing.
- Editors like nano (easy) and vim (powerful) are must-haves for remote servers (no GUI).
- Terminal shortcuts speed up everything saving seconds per command adds up in long sessions, making you 2-3x faster at repetitive tasks.

### Top 2 File Editors & Editing Commands

| Command | Simple Description | Examples |
|---------|--------------------|----------|
| **NANO**<br>`$ nano file.txt` | Beginner-friendly editor with on-screen shortcuts. | 1. Open/edit: `nano config.conf`<br>2. Search: Ctrl+W "pattern"<br>3. Save/exit: Ctrl+O, Ctrl+X |
| **VIM**<br>`$ vim file.txt` | Powerful modal editor for pros (vi-compatible). | 1. Open: `vim script.sh`<br>2. Insert mode: `i` (edit), Esc (normal)<br>3. Save/quit: `:wq` |

---

### nano Editor (Beginner-Friendly)
Nano is simple — no modes, just type. Great for quick config edits on servers.

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
Vim is modal (switch modes) and keyboard-only — fast once learned. Essential for remote work.

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

### Terminal Shortcuts
Speed up your workflow with bash keyboard magic, no mouse needed!

| Shortcut | What It Does | Example/Use |
|----------|--------------|-------------|
| **Ctrl+C** | Interrupt/stop current command. | Stop a long-running script: Ctrl+C during `ping google.com`. |
| **Ctrl+D** | End input (EOF) or exit shell. | Exit current shell: Ctrl+D in empty prompt. |
| **Ctrl+Z** | Suspend process (send to background). | Pause vim: Ctrl+Z, then `fg` to resume. |
| **Ctrl+R** | Reverse search history. | Type partial command (e.g., "git"), Ctrl+R to find. |
| **!!** | Run last command again. | Forgot sudo? `sudo !!` reruns last cmd with sudo. |
| **Tab** | Auto-complete (files/commands). | Type `ls /etc/pa`, Tab → `ls /etc/passwd`. |
| **Ctrl+A/E** | Jump to line start/end. | Edit long command: Ctrl+A (start), type, Ctrl+E (end). |
| **Ctrl+U** | Cut from cursor to line start. | Clear prompt: Ctrl+U, then paste with Ctrl+Y. |
| **Ctrl+L** | Clear screen. | Clean view: Ctrl+L during output flood. |
| **Up/Down Arrow** | Cycle command history. | Reuse recent cmds: Up arrow, Enter. |

**Tips:** Run `history | tail` to see past cmds.

---

## Sample Exercises

1. Create a file using nano, add content, and save it.
2. Open a file in vim, navigate to a specific line, and make edits.
3. Use vim to search and replace text in a configuration file.
4. Use Terminal Shortcuts

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

3. **Search and replace in vim:**
   ```bash
   vim config.conf
   /old_value                      # Search
   n                               # Next match
   :%s/old_value/new_value/g       # Replace all
   :wq                             # Save and quit
   ```

4: Use Terminal Shortcuts
```bash
   ping google.com                 # Start ping
   Ctrl+C                          # Interrupt (stops it)
   ls /etc/pa                      # Partial command
   Ctrl+R                          # Search history (type "ls /etc/p", Enter)
   clear                           # Or Ctrl+L to clear screen
   !!                              # Rerun last command
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
- [ ] Use common terminal shortcuts for efficiency (Ctrl+C, Ctrl+R, Tab)
---

## Next Steps
Proceed to [Day 9: File Transfer](../Day_09/notes_and_exercises.md) to learn secure file transfer methods like SCP and rsync.
