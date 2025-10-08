# Day 07: Users, Groups & Permissions

## Learning Objectives
By the end of Day 7, you will:
- Understand Linux user and group concepts, including UID/GID and system vs. regular users
- Create, modify, and delete users and groups using interactive and scripted methods
- Manage file ownership and permissions with chown, chmod, and chgrp
- Configure special permissions (SUID, SGID, Sticky Bit) and demonstrate their effects
- Apply Access Control Lists (ACLs) with setfacl and getfacl for fine-grained access
- Apply security best practices for user management, including locking accounts and auditing
- Explore key configuration files like /etc/passwd, /etc/shadow, and /etc/sudoers for user control

**Estimated Time:** 1 hour

## Sample Environment Setup
For exercises, we'll use a test setup. Run these commands to prepare (as root or with sudo):

```bash
# Create test users and groups (if not existing)
sudo useradd -m -s /bin/bash testuser1
sudo useradd -m -s /bin/bash testuser2
sudo groupadd testgroup

# Create a test file and directory
touch testfile.txt
mkdir testdir
echo "Sample content" > testfile.txt

# Enable ACLs on filesystem if needed (e.g., for ext4)
sudo mount -o remount,acl /

# View initial state
ls -la testfile.txt testdir
id testuser1
getent group testgroup
```

This creates users `testuser1` and `testuser2`, group `testgroup`, and sample files for permission demos. ACL support requires filesystem mount option (acl).

## Notes

- **Why User & Group Management Matters?**
  - Controls access to resources, enforces least privilege, and prevents unauthorized actions in multi-user environments.
  - Critical for DevOps/SRE: Automate provisioning, secure shared systems, and audit compliance.

### Top 8 User & Permission Management Commands

To mirror Day 6's log parsing table, here's a quick-reference table for core commands in user/group/permissions. Each includes a simple description and key examples for hands-on use.

| Command | Simple Description | Examples |
|---------|--------------------|----------|
| **USERADD**<br>`$ sudo useradd -m user` | Creates a new user account (non-interactive). | 1. Basic user with home: `sudo useradd -m testuser`<br>2. With shell and groups: `sudo useradd -m -s /bin/bash -G sudo testuser`<br>3. Custom UID: `sudo useradd -u 2000 -m testuser` |
| **ADDUSER**<br>`$ sudo adduser user` | Creates a new user interactively (prompts for details). | 1. Full interactive: `sudo adduser testuser` (sets pw, home, etc.)<br>2. Skip prompts: `sudo adduser --disabled-password testuser`<br>3. System user: `sudo adduser --system --group myservice` |
| **PASSWD**<br>`$ sudo passwd user` | Sets or changes a user's password. | 1. Set pw: `sudo passwd testuser`<br>2. Expire pw: `sudo passwd -e testuser`<br>3. Lock/unlock: `sudo passwd -l testuser` (lock) |
| **USERMOD**<br>`$ sudo usermod -aG group user` | Modifies an existing user's attributes. | 1. Add to group: `sudo usermod -aG docker testuser`<br>2. Change shell: `sudo usermod -s /bin/zsh testuser`<br>3. Lock account: `sudo usermod -L testuser` |
| **GROUPADD**<br>`$ sudo groupadd group` | Creates a new group. | 1. Basic group: `sudo groupadd testgroup`<br>2. With GID: `sudo groupadd -g 2000 testgroup`<br>3. System group: `sudo groupadd --system syslog` |
| **CHOWN**<br>`$ sudo chown user:group file` | Changes file ownership (user and/or group). | 1. Change user/group: `sudo chown testuser:testgroup file.txt`<br>2. Recursive: `sudo chown -R testuser: /home/testuser`<br>3. User only: `sudo chown testuser file.txt` |
| **CHMOD**<br>`$ chmod 755 file` | Changes file permissions (numeric or symbolic). | 1. Numeric: `chmod 644 file.txt` (rw-r--r--)<br>2. Symbolic: `chmod u+x,g-w file.txt`<br>3. Recursive: `chmod -R 755 /dir` |
| **SETFACL**<br>`$ setfacl -m u:user:rwx file` | Sets Access Control Lists for fine-grained permissions. | 1. Add user ACL: `setfacl -m u:testuser2:r file.txt`<br>2. Default for dir: `setfacl -m d:g:testgroup:rwx /dir`<br>3. Remove: `setfacl -x u:testuser2 file.txt` |

---

### User Concepts & Management
Users are identified by UID (User ID); groups by GID (Group ID). System users (UID < 1000) run services; regular users (UID >= 1000) are for humans. 

- **Key Files:**
  - **/etc/passwd:** Stores user account info (non-sensitive). World-readable for compatibility (e.g., for mailers). Each line is colon-separated fields. Format: `username:password:UID:GID:GECOS:home:shell`.
    - **Fields:** 
      - `username`: Unique login name.
      - `password`: 'x' (shadowed; actual hash in /etc/shadow).
      - `UID`: Numeric user ID (0=root, <1000=system).
      - `GID`: Primary group ID.
      - `GECOS`: Comment/info (e.g., full name).
      - `home`: Home directory path.
      - `shell`: Default shell (e.g., /bin/bash).
    - **Example:** `testuser1:x:1001:1001:Test User:/home/testuser1:/bin/bash`
    - **DevOps Note:** Parse with `awk -F: '{print $1, $3, $6}' /etc/passwd` to list users, UIDs, homes.
  - **/etc/shadow:** Secure storage for passwords and aging (sensitive). Root-only readable (mode 000640). Each line: colon-separated. Format: `username:encrypted_passwd:last_change:min:max:warn:inactive:expire:reserved`.
    - **Fields:**
      - `username`: Matches /etc/passwd.
      - `encrypted_passwd`: Hashed password ('!' or '*' = locked/disabled; starts with $ for algorithms like SHA-512).
      - `last_change`: Days since Jan 1, 1970, when pw changed.
      - `min`: Min days between changes (0=no min).
      - `max`: Max days before expiration.
      - `warn`: Days to warn before expiration.
      - `inactive`: Days inactive after expiration before lock.
      - `expire`: Days since epoch when account expires.
      - `reserved`: Unused (future).
    - **Example:** `testuser1:$6$salt$hash...:19500:0:99999:7:::`
    - **DevOps Note:** Audit expired pwds: `sudo awk -F: '$5==0 || $3 < (mktime("now")/86400 - 30)' /etc/shadow` (simplified check).
  - **/etc/sudoers:** Defines sudo rules (sensitive). Mode 0440, root/group sudo readable. Edit only with `visudo` (syntax check, lock). Format: `who where=(as_whom) tags command`. Lines can include users, groups (%group), hosts, runas (user/group), tags (NOPASSWD), commands (ALL or paths).
    - **Key Elements:**
      - `who`: User (%group for groups).
      - `where`: Host (ALL=any).
      - `=(as_whom)`: Run as user/group (ALL=any).
      - `tags`: NOPASSWD (no pw prompt), PASSWD (require pw).
      - `command`: ALL (any cmd), /path/to/cmd, NOEXEC (no shell exec).
    - **Examples:**
      - `root ALL=(ALL:ALL) ALL`: Root can sudo anything as anyone (default).
      - `%sudo ALL=(ALL:ALL) ALL`: Sudo group members full access.
      - `devops1 ALL=(root) NOPASSWD: /usr/bin/docker *`: devops1 runs docker as root without pw, any args.
      - `testuser1 localhost=/bin/systemctl restart nginx`: Restricted: only restart nginx on local host.
    - **DevOps Note:** For teams, use groups: `%devops ALL=(ALL) NOPASSWD: /usr/bin/ansible-playbook`. Include files (/etc/sudoers.d/) for modular configs: `echo "user ALL=(ALL) ALL" | sudo tee /etc/sudoers.d/user`.

```bash
# View files (as root for shadow)
sudo cat /etc/passwd | head -5                   # Sample users
sudo cat /etc/shadow | grep testuser1             # Password hash/info
sudo visudo -c                                    # Validate sudoers
sudo visudo                                       # Safe edit sudoers
```

User data: `/etc/passwd` (info), `/etc/shadow` (hashed passwords, root-only).

```bash
# Create user interactively (recommended for beginners)
sudo adduser testuser3

# Create user non-interactively
sudo useradd -m -s /bin/bash -G sudo testuser4  # -m: home dir, -s: shell, -G: secondary groups

# Set/change password
sudo passwd testuser1

# Modify user
sudo usermod -aG docker testuser1                # -aG: append to group
sudo usermod -L testuser2                        # Lock account
sudo usermod -U testuser2                        # Unlock
sudo usermod -d /new/home -s /bin/zsh testuser1  # Change home/shell

# Delete user
sudo userdel -r testuser3                        # -r: remove home dir

# View user info
id testuser1                                     # UID, GID, groups
groups testuser1                                 # Groups only
getent passwd testuser1                          # Full entry
awk -F: '$1=="testuser1"' /etc/passwd            # Query with awk
```

---

### Group Concepts & Management
Groups simplify permissions for multiple users. Primary group (set at creation); secondary for extras. Data in `/etc/group`.

```bash
# Create/modify group
sudo groupadd newgroup
sudo groupmod -n renamedgroup newgroup           # Rename

# Manage members
sudo gpasswd -a testuser1 testgroup              # Add user
sudo gpasswd -d testuser2 testgroup              # Remove user
sudo gpasswd -M user1,user2 testgroup            # Set members list

# Delete group (must be empty)
sudo groupdel testgroup

# View groups
getent group testgroup                           # Full entry
grep '^testgroup' /etc/group                     # From file
```

---

### File Ownership & Permissions
Every file has an owner (user), group, and permissions that control access for the owner, group, and others (everyone else). Permissions are represented as `rwxrwxrwx` (or `-` for none), where the first three chars are for owner (u), next for group (g), last for others (o). Each position: r=read (view content), w=write (modify), x=execute (run as program or enter dir).

Permissions can be set using two modes:
- **Numeric (Octal) Mode:** A 3-digit octal number (000-777) where each digit represents perms for owner/group/other. Calculate by adding: r=4, w=2, x=1 (e.g., rwx=7, rw-=6, r-x=5). Leading 4/2/1 for special perms (SUID/SGID/Sticky). Quick for scripts/automation.
- **Symbolic Mode:** Specify target (u=owner, g=group, o=others, a=all), operator (+=add, -=remove, ==set exactly), and perms (r/w/x). E.g., `a+rx` adds read/exec for all. Flexible for incremental changes; recursive with `-R`.

Use `ls -l` to view: `-rwxr-xr-x 1 owner group 1024 Oct 8 10:00 file.txt` (first `-` = regular file, then perms, owner, group, size, date, name). A '+' at end (e.g., `rw-r--r--+`) indicates ACLs are present.

#### Numeric Mode Combinations
All possible combinations for a single triad (owner/group/other) are based on binary bits (3 bits per category: rwx). Below is a table of all 8 (000-777) for one category (e.g., owner); apply the same logic to group/other for the full 3-digit mode.

| Octal | Symbolic Equivalent | Meaning | Use Case |
|-------|---------------------|---------|----------|
| 0 (---) | --- | No permissions | Block access entirely (rare for owner) |
| 1 (--x) | --x | Execute only | Scripts/binaries (no read needed) |
| 2 (-w-) | -w- | Write only | Temp files (dangerous without read) |
| 3 (-wx) | -wx | Write + execute | Rarely used standalone |
| 4 (r--) | r-- | Read only | View-only files (e.g., configs) |
| 5 (r-x) | r-x | Read + execute | Shared scripts/binaries |
| 6 (rw-) | rw- | Read + write | Editable files (no exec) |
| 7 (rwx) | rwx | Full access | Owner/executables |

**Full Mode Examples:** Combine for 3 digits (owner-group-other). E.g., 644 = owner rw- (6) + group r-- (4) + other r-- (4) = `rw-r--r--` (common for docs).

| Full Octal | Perm String | Owner | Group | Other | Common Use |
|------------|-------------|-------|-------|-------|------------|
| 000 | --------- | --- | --- | --- | No access (locked files) |
| 400 | r-------- | r-- | --- | --- | Owner read-only (private) |
| 600 | rw------- | rw- | --- | --- | Owner read/write (secrets) |
| 644 | rw-r--r-- | rw- | r-- | r-- | Standard files (readable by all) |
| 700 | rwx------ | rwx | --- | --- | Owner full (personal dirs) |
| 755 | rwxr-xr-x | rwx | r-x | r-x | Executables/dirs (shared run) |
| 775 | rwxrwxr-x | rwx | rwx | r-x | Group collaboration (team dirs) |
| 777 | rwxrwxrwx | rwx | rwx | rwx | World-writable (avoid; e.g., /tmp with sticky) |

**Note:** For special perms, prefix: 4755 (SUID + 755), 2755 (SGID + 755), 1755 (Sticky + 755).

#### Symbolic Mode Examples
| Command | Effect | Result Perms (from 644 base) | Notes |
|---------|--------|------------------------------|-------|
| `chmod u+x file` | Add execute to owner | rwxr--r-- | Makes executable |
| `chmod g-w file` | Remove write from group | rw-r--r-- | Restrict group edits |
| `chmod o= file` | Set others to none | rw-r----- | Block public access |
| `chmod a+rx file` | Add read/exec to all | rwxr-xr-x | Broad sharing |
| `chmod -R g+w dir` | Recursively add group write | Applies to dir & contents | For team folders |

| Command | Purpose | Example / Notes |
|---------|---------|-----------------|
| `chown user:group file` | Change owner and/or group | `sudo chown testuser1:testgroup testfile.txt` (full change); use `:group` for group only |
| `chgrp group file` | Change group only | `sudo chgrp testgroup testdir` (shorter than chown) |
| `chmod numeric file` | Set permissions numerically | `chmod 755 testfile.txt` (rwxr-xr-x: owner full, others read/exec); common: 644 (rw-r--r-- for files), 755 (for dirs/scripts) |
| `chmod symbolic file` | Modify permissions symbolically | `chmod u+x,g-w,o-r testfile.txt` (+ add, - remove, = exact set; u=owner, g=group, o=others, a=all); recursive: `-R` |
| `ls -l file` | View ownership & permissions | Shows `drwxr-xr-x` (d=dir); pipe to `grep` for audits |
| `stat file` | Detailed metadata | Includes exact perms (e.g., 0755), times, inode; useful for forensics |

#### Access Control Lists (ACLs)
ACLs extend basic permissions by allowing specific users/groups beyond owner/group/other. Useful for DevOps: granular access in shared repos or configs without changing ownership. Requires filesystem support (e.g., ext4 with `acl` mount option; check `tune2fs -l /dev/sda1 | grep acl`).

- **Basic vs. ACL:** Basic = 3 slots (u/g/o); ACL = unlimited entries. ACLs shown as `+` in `ls -l`. Mask limits effective group/other ACL perms.
- **Types:** Access ACLs (file access); Default ACLs (inherit to new files in dir).
- **Commands:** `getfacl` views; `setfacl` modifies. Install if needed: `apt install acl`.

| Command | Purpose | Example / Notes |
|---------|---------|-----------------|
| `getfacl file` | View ACL entries | `getfacl testfile.txt` (shows owner, group, mask, other, +entries like `user::rw-`, `user:testuser2:r--`) |
| `setfacl -m entry file` | Modify/add ACL | `setfacl -m u:testuser2:rwx testfile.txt` (add rwx for testuser2); `m:g:team:r--` for group; `d:u:testuser1:rwx testdir` for default |
| `setfacl -x entry file` | Remove ACL entry | `setfacl -x u:testuser2 testfile.txt` (remove testuser2 entry) |
| `setfacl -b file` | Remove all ACLs | `setfacl -b testfile.txt` (back to basic perms) |
| `setfacl -R -m entry dir` | Recursive modify | Applies to dir & contents; use `-d` for default only |
| `setfacl --set-file=ref file` | Copy ACLs from ref | `setfacl --set-file=template.txt testfile.txt` (clone ACLs) |

**DevOps Note:** For CI/CD shares: `setfacl -R -m g:devops:rwx /shared/repo` (team read/write). Audit: `getfacl /shared/* | grep user:`. Conflicts: Effective perms = min of basic + ACL + mask.

---

### Special Permissions
Special permissions override standard ones for security/collaboration. Set like regular (symbolic: `u+s` for SUID) or numeric (add to octal: 4xxx for SUID). View in `ls -l`: uppercase S/T if no x bit (e.g., `rws` = SUID with x).

| Permission | Purpose | Example / Notes |
|------------|---------|-----------------|
| **SUID (Set User ID)** | Executes as file owner (not caller), even if no perms. Risky: potential escalation. Numeric: 4xxx (e.g., 4755). Symbolic: `u+s`. | `chmod u+s testfile.txt` (ls: `-rwsr-xr-x`); Real: `/usr/bin/passwd` (runs as root to edit shadow) |
| **SGID (Set Group ID)** | On files: runs as group owner. On dirs: new files inherit dir's group (for team shares). Numeric: 2xxx (e.g., 2755). Symbolic: `g+s`. | `chmod g+s testdir` (ls: `drwxr-sr-x`); Useful for collaborative dirs like `/var/mail` |
| **Sticky Bit** | On dirs: only owner/root can delete files (others can't rm even if w perm). Numeric: 1xxx (e.g., 1755). Symbolic: `+t`. | `chmod +t testdir` (ls: `drwxr-xr-t`); Real: `/tmp` (prevents cross-user deletion) |

```bash
# Set special perms
chmod u+s testfile.txt                           # SUID: run as owner
chmod g+s testdir                                # SGID: inherit group
chmod +t testdir                                 # Sticky: restrict delete in dir

# Numeric: 4755 for SUID+755, 2755 for SGID+755, 1755 for Sticky+755
chmod 4755 testfile.txt

# View (s/t appear in ls -l)
ls -la testfile.txt testdir

# Examples:
# SUID: /usr/bin/passwd (users change own password as root)
# SGID: /usr/bin/wall (broadcast as group)
# Sticky: /tmp (users can't delete others' files)
```

---

### Account Security & Switching
- Lock: `usermod -L user` or `passwd -l user` (blocks login).
- Policies: Use `chage -M 90 user` (max age), `/etc/login.defs` for defaults.
- Switching: `su - user` (full session), `sudo -u user cmd` (single cmd). Controlled by /etc/sudoers.

```bash
# Lock/unlock
sudo usermod -L testuser1
sudo usermod -U testuser1

# Enforce policy
sudo chage -l testuser1                          # View policy
sudo chage -M 30 -m 7 testuser1                  # Max 30 days, min 7

# Switch
sudo -u testuser1 whoami                         # Run as user
su - testuser1                                   # Switch session
```

---

## Sample Exercises

1. Create a user `devops1` with home directory and bash shell, set a password, and add to `sudo` and `docker` groups.
2. Create a group `projectX` and add `testuser1` and `testuser2` to it; verify membership.
3. Change the default shell for `testuser1` to `/bin/zsh` and lock/unlock the account.
4. Set SUID on `testfile.txt`, SGID on `testdir`, and Sticky Bit on `testdir`; show with `ls -l`.
5. List all regular users (UID >= 1000) and count groups with more than 3 members.
6. Change ownership of `testfile.txt` to `testuser1:testgroup` and permissions to 660 (rw-rw----).
7. Remove `testuser4` and their home directory; find and list all files owned by `testuser1`.
8. Enforce a password policy: Set max age to 90 days for `testuser2`.
9. Switch to `testuser1` and create a file in `testdir`; verify group inheritance (if SGID set).
10. Audit: List all SUID files on the system; view /etc/shadow entry for `testuser1`; edit /etc/sudoers to allow `testuser1` passwordless sudo.
11. Set an ACL on `testfile.txt` giving `testuser2` read access; view with `getfacl`; remove it.
12. Set a default ACL on `testdir` for new files to give `testgroup` rwx; create a file inside and verify.

---

## Solutions

1. **Create user with groups:**
   ```bash
   sudo adduser devops1                           # Interactive
   # OR
   sudo useradd -m -s /bin/bash devops1           # Non-interactive
   sudo passwd devops1
   sudo usermod -aG sudo,docker devops1
   id devops1                                      # Verify
   ```

2. **Create group and add users:**
   ```bash
   sudo groupadd projectX
   sudo gpasswd -a testuser1 projectX
   sudo gpasswd -a testuser2 projectX
   getent group projectX                           # Verify
   ```

3. **Change shell and lock/unlock:**
   ```bash
   sudo usermod -s /bin/zsh testuser1
   sudo usermod -L testuser1                       # Lock
   sudo usermod -U testuser1                       # Unlock
   ```

4. **Special permissions:**
   ```bash
   chmod u+s testfile.txt
   chmod g+s testdir
   chmod +t testdir
   ls -l testfile.txt testdir                      # Output: -rwsr-xr-x for SUID, drwxr-sr-t for Sticky+SGID
   ```

5. **List regular users and group count:**
   ```bash
   awk -F: '$3 >= 1000 {print $1}' /etc/passwd     # Users
   awk -F: '$4 ~ /,/ {if (gsub(/,/,"&")+1 > 3) print $1}' /etc/group | wc -l  # Groups with >3 members
   ```

6. **Ownership and permissions:**
   ```bash
   sudo chown testuser1:testgroup testfile.txt
   chmod 660 testfile.txt
   ls -l testfile.txt                              # -rw-rw---- 1 testuser1 testgroup ...
   ```

7. **Remove user and find files:**
   ```bash
   sudo userdel -r testuser4
   find /home -user testuser1 2>/dev/null          # List files
   ```

8. **Password policy:**
   ```bash
   sudo chage -M 90 testuser2
   chage -l testuser2                              # Verify
   ```

9. **Switch and create file:**
   ```bash
   sudo -u testuser1 touch testdir/newfile.txt
   ls -l testdir/newfile.txt                       # Should inherit testgroup if SGID
   ```

10. **Audit and config:**
    ```bash
    find / -perm -4000 2>/dev/null                  # SUID files
    sudo grep testuser1 /etc/shadow                  # Shadow entry
    sudo visudo                                      # Edit sudoers: Add "testuser1 ALL=(ALL) NOPASSWD:ALL"
    ```

11. **ACL on file:**
    ```bash
    setfacl -m u:testuser2:r testfile.txt
    getfacl testfile.txt                            # Shows user:testuser2:r--
    setfacl -x u:testuser2 testfile.txt             # Remove
    ```

12. **Default ACL on dir:**
    ```bash
    setfacl -m d:g:testgroup:rwx testdir
    sudo -u testuser1 touch testdir/newfile.txt     # Create as testuser1
    getfacl testdir/newfile.txt                     # Shows group:testgroup:rwx (inherited)
    ```

---

## Completion Checklist
- [ ] Understand UID/GID concepts and system vs regular users
- [ ] Can create, modify, and delete users and groups with options like -m, -aG, -r
- [ ] Know the difference between primary and secondary groups; manage with gpasswd
- [ ] Understand file ownership and permission models (rwx, numeric/symbolic)
- [ ] Can set and identify special permissions (SUID, SGID, Sticky) via chmod and ls -l
- [ ] Can manage ACLs with setfacl/getfacl for extended access control
- [ ] Familiar with user account security practices: locking, policies, auditing
- [ ] Know roles of /etc/passwd, /etc/shadow, and /etc/sudoers; can view/edit safely

---

## Key Command Combinations

```bash
# Create user, add to group, set perms on shared dir
sudo useradd -m newuser; sudo gpasswd -a newuser sharedgroup; sudo chmod g+rw /shared/dir

# Audit users in group and their files
getent group devgroup | cut -d: -f4 | tr ',' '\n' | xargs -I {} find /home/{} -type f 2>/dev/null

# Bulk lock expired accounts (example with awk)
awk -F: '$8=="*' {print $1}' /etc/shadow | xargs -I {} sudo usermod -L {}

# Find and remove orphaned SUID files (careful!)
find / -perm -4000 -user nobody 2>/dev/null | xargs ls -l

# Set ACL for team on shared dir, view inheritance
setfacl -R -m g:devops:rwx /shared; find /shared -exec getfacl {} \; | grep mask
```

---

## Best Practices
- Test commands with test users/files first to avoid locking yourself out
- Use `--help` or `man` (e.g., `man useradd`) for full options
- Always use `sudo` for management; avoid direct root login
- Set umask 022 (or 077 for secure) in `/etc/profile` for default perms
- Audit regularly: `lastlog`, `faillog`, `grep` /etc/shadow for expired pwds
- Enforce policies via PAM (`/etc/pam.d`) and `chage`; rotate service accounts
- Backup `/etc/passwd`, `/etc/group`, `/etc/shadow` before changes
- Edit /etc/sudoers only with `visudo`; use groups for scalable privileges
- For ACLs: Use sparingly (complexity); document entries; combine with basic perms (e.g., chmod 640 + ACL for extras)

---

## Sample Interview Questions

1. What is the difference between `useradd` and `adduser`?
2. How do you add a user to multiple groups at once?
3. What is the purpose of the `/etc/shadow` file?
4. How do you enforce password policies for users?
5. Explain SUID, SGID, and Sticky Bit with real-world examples.
6. How do you list all members of a group?
7. What happens if you delete a user but not their files?
8. How do you switch to another user without knowing their password?
9. How do you find all files owned by a specific user?
10. What are the security risks of improper user/group management?
11. How do you check if a user's password is expired?
12. What's the difference between `su` and `sudo`?
13. Describe the contents and security of /etc/passwd, /etc/shadow, and /etc/sudoers.
14. What are ACLs, and when would you use setfacl over chmod?
15. How do you view and remove an ACL entry for a specific user?

---

## Interview Question Answers

1. **`useradd` vs `adduser`:** `useradd` is low-level/scriptable (manual home/passwd setup); `adduser` is interactive wrapper (handles home, prompts for passwd).
2. **Multiple groups:** `sudo usermod -aG group1,group2,group3 username` (comma-separated).
3. **`/etc/shadow`:** Stores hashed passwords, aging info; root-only readable for security (vs. world-readable `/etc/passwd`).
4. **Password policies:** Use `chage` (e.g., `-M 90` for max age), `/etc/login.defs` for defaults, PAM modules in `/etc/pam.d/common-password`.
5. **Special perms:** SUID (run as owner, e.g., `passwd` changes root-owned files); SGID (inherit group, e.g., shared dirs); Sticky (restrict delete, e.g., `/tmp` prevents cross-user rm).
6. **Group members:** `getent group groupname` or `grep '^groupname:' /etc/group` (members in field 4).
7. **Orphaned files:** Files persist with numeric UID (unresolvable name); risks include access leaks—use `find -uid <num>` to locate/reassign.
8. **Switch without password:** `sudo -u username cmd` or `sudo su - username` (if sudoers allow nopasswd for you).
9. **Find user files:** `find / -user username 2>/dev/null` (suppress errors).
10. **Security risks:** Escalation (weak groups), orphans (data leaks), over-perms (unauth access), expired pwds (brute-force vuln).
11. **Expired password:** `chage -l username` (shows dates) or `grep username /etc/shadow` (check ! for locked).
12. **`su` vs `sudo`:** `su` switches full session (needs target pw); `sudo` runs cmds as another user (uses your pw, auditable via logs).
13. **Key files:** `/etc/passwd` (user info, world-readable); `/etc/shadow` (hashed pwds/policies, root-only); `/etc/sudoers` (sudo rules, edit with `visudo` for syntax checks).
14. **ACLs:** Extended perms for specific users/groups beyond basic u/g/o; use setfacl for granular (e.g., one dev read-only on prod config) without ownership changes.
15. **View/remove ACL:** `getfacl file` (lists entries); `setfacl -x u:user file` (removes specific); `setfacl -b file` (clears all).

---

## Command Summary

| Category | Command | Description | Common Options/Usage |
|----------|---------|-------------|----------------------|
| **User Creation** | `adduser` | Interactive user creation | `sudo adduser username` (prompts for details) |
| | `useradd` | Non-interactive user creation | `sudo useradd -m -s /bin/bash username` (-m: home, -s: shell) |
| **Password Management** | `passwd` | Set/change password | `sudo passwd username` |
| **User Modification** | `usermod` | Modify user attributes | `-aG group username` (add group), `-L` (lock), `-U` (unlock), `-s shell` (shell) |
| **User Deletion** | `userdel` | Delete user | `sudo userdel -r username` (-r: remove home) |
| **Group Creation** | `groupadd` | Create group | `sudo groupadd groupname` |
| **Group Modification** | `groupmod` | Modify group | `-n newname groupname` (rename) |
| **Group Deletion** | `groupdel` | Delete group | `sudo groupdel groupname` (must be empty) |
| **Group Membership** | `gpasswd` | Manage group members | `-a user group` (add), `-d user group` (remove), `-M user1,user2 group` (set list) |
| **User Info** | `id` | Show UID/GID/groups | `id username` |
| | `groups` | List user's groups | `groups username` |
| | `getent` | Query user/group DB | `getent passwd username`, `getent group groupname` |
| **Ownership** | `chown` | Change owner/group | `sudo chown user:group file` |
| | `chgrp` | Change group only | `sudo chgrp group file` |
| **Permissions** | `chmod` | Change permissions | `chmod 755 file` (numeric), `chmod u+x file` (symbolic) |
| **Special Permissions** | `chmod` (special) | Set SUID/SGID/Sticky | `u+s` (SUID), `g+s` (SGID), `+t` (Sticky) |
| **ACLs** | `getfacl` | View ACL entries | `getfacl file` (shows owner/group/mask/ACLs) |
| | `setfacl` | Modify ACLs | `-m u:user:rwx file` (add/mod), `-x u:user file` (remove), `-b file` (clear all), `-d g:group:rwx dir` (default) |
| **Account Policies** | `chage` | Manage password aging | `sudo chage -M 90 username` (max age) |
| **Switching** | `su` | Switch user session | `su - username` |
| | `sudo` | Run as another user | `sudo -u username cmd` |
| **File Viewing** | `ls` | List with permissions | `ls -la file` |
| | `stat` | Detailed file stats | `stat file` |
| **Config Files** | `cat`/`grep` | View /etc files | `sudo cat /etc/shadow`, `grep user /etc/passwd` |
| | `visudo` | Edit sudoers safely | `sudo visudo` |

---

## Next Steps
Proceed to [Day 8: File Management & Editors](../Day_08/notes_and_exercises.md) to learn advanced file operations and text editors.

---
