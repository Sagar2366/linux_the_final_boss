# Day 10: Environment Variables, Aliases & Shell Customization

## Table of Contents

- [Day 10: Environment Variables, Aliases & Shell Customization](#day-10-environment-variables-aliases-&-shell-customization)
  - [Learning Objectives](#learning-objectives)
  - [Notes](#notes)
    - [Top Shell Customization Commands](#top-shell-customization-commands)
    - [Environment Variables](#environment-variables)
    - [Aliases](#aliases)
    - [Shell Functions](#shell-functions)
  - [Sample Exercises](#sample-exercises)
  - [Sample Interview Questions](#sample-interview-questions)
  - [Interview Question Answers](#interview-question-answers)
  - [Completion Checklist](#completion-checklist)
  - [Next Steps](#next-steps)


## Learning Objectives
By the end of Day 10, you will:
- Understand and manage environment variables
- Create and manage shell aliases
- Configure shell startup files
- Create useful shell functions

**Estimated Time:** 30 mins

## Notes
- **Why Customize Your Shell?**
  - Boosts productivity, reduces repetitive typing, and personalizes your workflow.
  - Essential for DevOps, SRE, and power users.

- **Environment Variables:**
  - Environment variables in Linux are dynamic named values stored in the system's memory that influence how processes, shells, and applications behave. They're essentially key-value pairs (e.g., PATH=/usr/bin:/bin) that provide configuration data, like paths to executables or user-specific settings, without hardcoding them into scripts or programs
  - Store configuration and session info (e.g., PATH, HOME, USER, SHELL).
  - View all: `printenv` or `env`
  - View one: `echo $PATH`
  - Set for session: `export VAR=value`
  - Set permanently: add to `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc`
  - Remove: `unset VAR`

- **Common Environment Variables:**
  - `PATH`: Directories searched for executables
  - `HOME`: User's home directory
  - `USER`: Current username
  - `SHELL`: Default shell
  - `PS1`: Shell prompt format

- **Aliases:**
  - Shortcut for commands (e.g., `alias ll='ls -alF'`)
  - List all: `alias`
  - Remove: `unalias ll`
  - Make permanent: add to `~/.bashrc` or `~/.zshrc`

- **Shell Customization:**
  - Edit `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc` for custom settings
  - Add functions: e.g., `mkcd() { mkdir -p "$1" && cd "$1"; }`
  - Source file to apply changes: `source ~/.bashrc`

### Top Shell Customization Commands

| Command | Simple Description | Examples |
|---------|--------------------|----------|
| **EXPORT**<br>`$ export VAR=value` | Set an environment variable (session or permanent). | 1. Set: `export MYAPP=/opt/myapp`<br>2. View: `echo $MYAPP`<br>3. PATH add: `export PATH="$PATH:~/shell_custom_test/scripts"` |
| **PRINTENV**<br>`$ printenv [VAR]` | List all or specific environment variables. | 1. All: `printenv`<br>2. One: `printenv PATH`<br>3. Env all: `env` (alternative) |
| **UNSET**<br>`$ unset VAR` | Remove an environment variable from session. | 1. Remove: `unset MYAPP`<br>2. Verify: `echo $MYAPP` (empty)<br>3. Multiple: `unset VAR1 VAR2` |
| **ALIAS**<br>`$ alias name='cmd'` | Create shortcut for a command. | 1. Create: `alias ll='ls -la'`<br>2. List: `alias`<br>3. Remove: `unalias ll` |
| **SOURCE**<br>`$ source ~/.bashrc` | Reload shell config file to apply changes. | 1. Reload: `source ~/.bashrc`<br>2. Short: `. ~/.bashrc`<br>3. Test: Add alias, source, then use it

### Environment Variables
**Concept:** Key-value pairs that configure your shell session (e.g., PATH for command search). Local to session unless exported/permanent.

**Step-by-Step:**
1. View current vars: `printenv | grep PATH` (shows your PATH); `echo $HOME` (shows home dir).
2. Set temporary var: `export MYTEST="Hello World"` (session-only); `echo $MYTEST` (displays value).
3. Add to PATH: `export PATH="$PATH:~/shell_custom_test/scripts"`; `test.sh` (runs your sample script—proves PATH works); `echo $PATH` (verify addition).
4. Remove var: `unset MYTEST`; `echo $MYTEST` (empty now).
5. Make permanent: `echo 'export MYAPP="permanent value"' >> ~/.bashrc`; `source ~/.bashrc`; `echo $MYAPP` (persists in new terminals).
6. (Optional) System-wide: `sudo nano /etc/environment` (add `MYGLOBAL=value`), then log out/in.

**Tips:** Use `env | grep VAR` for quick search. Avoid overwriting PATH—always append (`$PATH:...`).

---

### Aliases
**Concept:** Shortcuts for long/frequent commands (e.g., ll for ls -la). Non-interactive, expand on use.

**Step-by-Step:**
1. Create temporary alias: `alias ll='ls -la'`; `ll` (lists detailed—shortcut works).
2. List aliases: `alias` (shows all, including ll).
3. Create another: `alias gs='git status'` (if Git installed); `gs` (runs git status).
4. Remove: `unalias ll`; `ll` (now errors—original ls runs).
5. Make permanent: `echo "alias ll='ls -la'" >> ~/.bashrc`; `echo "alias gs='git status'" >> ~/.bashrc`; `source ~/.bashrc`; open new terminal, `ll` (persists).
6. (Optional) Advanced: `alias rm='rm -i'` (prompts before delete—safety).

**Tips:** Bypass alias: `command ls` or `\ls`. Comment in ~/.bashrc: `# My ls alias: alias ll='ls -la'`.

---

### Shell Functions
**Concept:** Mini-scripts in your shell (like aliases but with logic/loops). Defined in config files.

**Step-by-Step:**
1. Create temporary function: `mkcd() { mkdir -p "$1" && cd "$1"; }`; `mkcd newdir` (creates/enters newdir).
2. Test: `pwd` (shows /home/user/newdir); `cd ~` (back home).
3. Another function: `backup() { cp "$1" "$1.backup.$(date +%Y%m%d_%H%M%S)"; echo "Backed up!"; }`; `backup ~/shell_custom_test/scripts/test.sh` (creates timestamped copy).
4. List functions: `declare -f | grep mkcd` (shows definition).
5. Make permanent: `echo 'mkcd() { mkdir -p "$1" && cd "$1"; }' >> ~/.bashrc`; `echo 'backup() { cp "$1" "$1.backup.$(date +%Y%m%d_%H%M%S)"; echo "Backed up!"; }' >> ~/.bashrc`; `source ~/.bashrc`.
6. (Optional) Extract function: Add the `extract()` from notes to ~/.bashrc, source, `extract file.zip` (unzips).

**Tips:** Use `$1` for first arg, `$@` for all. Test: `type mkcd` (shows it's a function).

---

## Sample Exercises
1. Add a directory to your PATH and verify it works.
2. Create an alias for a long command you use often.
3. Write a shell function to create and enter a directory in one step.
4. Change your shell prompt to show the current directory and username.
5. Make an environment variable permanent for all future sessions.

- **Shell Functions:**
  ```bash
  # Useful functions to add to ~/.bashrc
  mkcd() {
      mkdir -p "$1" && cd "$1"
  }
  
  backup() {
      cp "$1" "$1.backup.$(date +%Y%m%d_%H%M%S)"
  }
  
  extract() {
      case $1 in
          *.tar.gz) tar -xzf "$1" ;;
          *.zip) unzip "$1" ;;
          *.tar) tar -xf "$1" ;;
          *) echo "Unsupported format" ;;
      esac
  }
  ```

- **Shell Configuration Files:**
  - `~/.bashrc`: Interactive non-login shells (most terminal sessions)
  - `~/.bash_profile`: Login shells (SSH, console login)
  - `~/.zshrc`: Zsh configuration
  - `/etc/profile`: System-wide profile
  - `/etc/bash.bashrc`: System-wide bashrc

## Sample Interview Questions
1. What is the difference between a shell variable and an environment variable?
2. How do you make an environment variable available to all child processes?
3. How do you set a permanent alias?
4. What is the purpose of the PATH variable?
5. How do you customize your shell prompt?
6. How do you remove an environment variable?
7. What is the difference between `~/.bashrc` and `~/.bash_profile`?
8. How do you apply changes made to your shell configuration file?
9. How do you prevent accidental overwriting of important commands with aliases?
10. Why is it useful to keep your dotfiles under version control?

## Interview Question Answers
1. **Variables:** Shell variables are local to current shell; environment variables are inherited by child processes
2. **Export Variables:** Use `export VAR=value` to make variable available to child processes
3. **Permanent Alias:** Add alias to `~/.bashrc` or `~/.zshrc` and reload shell with `source ~/.bashrc`
4. **PATH Purpose:** Tells shell which directories to search for executable commands
5. **Custom Prompt:** Set PS1 variable in shell config file with escape sequences for colors/info
6. **Remove Variable:** Use `unset VARNAME` to remove environment variable from current session
7. **Config Files:** `~/.bashrc` for interactive non-login shells; `~/.bash_profile` for login shells
8. **Apply Changes:** Use `source ~/.bashrc` or `. ~/.bashrc` to reload configuration without restarting shell
9. **Safe Aliases:** Avoid common command names, use `command cmd` to bypass aliases, or use full paths
10. **Version Control:** Allows backup, sharing, and restoration of customizations across systems

## Completion Checklist
- [ ] Understand difference between shell and environment variables
- [ ] Can create and manage aliases
- [ ] Know how to customize shell prompt
- [ ] Can write and use shell functions
- [ ] Understand shell configuration files
- [ ] Can make changes permanent

## Next Steps
Proceed to [Day 11: Pipes, Redirects, Wildcards, and Links](../Day_11/notes_and_exercises.md) to master command chaining and I/O redirection.
