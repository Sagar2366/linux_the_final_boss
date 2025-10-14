# Day 09: File Transfer (SCP, SFTP, rsync, FTP, NFS)

## Table of Contents

- [Day 09: File Transfer (SCP, SFTP, rsync, FTP, NFS)](#day-09-file-transfer-scp-sftp-rsync-ftp-nfs)
  - [Learning Objectives](#learning-objectives)
  - [Sample Environment Setup](#sample-environment-setup)
- [Update and install basics (run on all three machines)](#update-and-install-basics-run-on-all-three-machines)
- [Enable services (run on all three machines)](#enable-services-run-on-all-three-machines)
- [Firewall (allow SSH, NFS, FTP from local subnet; adjust 192.168.56.0/24 to your VirtualBox network) (run on all three machines)](#firewall-allow-ssh-nfs-ftp-from-local-subnet;-adjust-192.168.56.024-to-your-virtualbox-network-run-on-all-three-machines)
- [Create test data](#create-test-data)
- [View initial state](#view-initial-state)
- [Create matching test dirs (run on both servers)](#create-matching-test-dirs-run-on-both-servers)
- [Mirror a sample file for testing](#mirror-a-sample-file-for-testing)
  - [Notes](#notes)
    - [Top File Transfer Commands](#top-file-transfer-commands)
    - [SSH (Secure Shell)](#ssh-secure-shell)
    - [SCP (Secure Copy)](#scp-secure-copy)
    - [SFTP (SSH File Transfer Protocol)](#sftp-ssh-file-transfer-protocol)
    - [rsync (Remote Sync)](#rsync-remote-sync)
    - [NFS (Network File System)](#nfs-network-file-system)
    - [FTP (File Transfer Protocol) - Legacy Warning](#ftp-file-transfer-protocol---legacy-warning)
  - [Sample Exercises](#sample-exercises)
  - [Solutions](#solutions)
  - [Completion Checklist](#completion-checklist)
  - [Next Steps](#next-steps)


## Learning Objectives
By the end of Day 9, you will:
- Master secure file transfer protocols (SCP, SFTP, rsync)
- Understand network file systems (NFS)
- Configure and troubleshoot file sharing services
- Apply security best practices for file transfers
- Automate file synchronization tasks

**Estimated Time:** 1-2 hours

## Sample Environment Setup
For hands-on exercises, use your **local machine** (e.g., Ubuntu/Mac) as the "client" and two VirtualBox VMs as **server1** (for NFS/FTP) and **server2** (for SSH/SCP/SFTP/rsync demos). Assume all run Ubuntu 22.04 LTS. Replace `server1-ip` and `server2-ip` with actual IPs (e.g., 192.168.56.101 for server1, 192.168.56.102 for server2). Use username `ubuntu` on VMs.

**Prep Steps:**

**On Local Machine, server1, and server2:**
```bash
# Update and install basics (run on all three machines)
sudo apt update && sudo apt upgrade -y
sudo apt install openssh-server openssh-client rsync nfs-kernel-server nfs-common vsftpd sshfs -y

# Enable services (run on all three machines)
sudo systemctl enable --now ssh nfs-kernel-server vsftpd

# Firewall (allow SSH, NFS, FTP from local subnet; adjust 192.168.56.0/24 to your VirtualBox network) (run on all three machines)
sudo ufw allow from 192.168.56.0/24 to any port 22    # SSH
sudo ufw allow from 192.168.56.0/24 to any port 2049  # NFS
sudo ufw allow from 192.168.56.0/24 to any port 21    # FTP
sudo ufw enable
```
**On Local Machine:**
```bash
# Create test data
mkdir -p ~/test_transfer/{docs,backups,shared}
echo "Local document v1" > ~/test_transfer/docs/report.txt
echo "Config data" > ~/test_transfer/config.ini
echo "Shared file" > ~/test_transfer/shared/demo.txt

# View initial state
ls -la ~/test_transfer/
```

**On server1 and server2 (via initial SSH login with password, or console):**
```bash
# Create matching test dirs (run on both servers)
mkdir -p ~/test_transfer/{docs,backups,shared}

# Mirror a sample file for testing
echo "Server document v1" > ~/test_transfer/docs/server_report.txt
```


**VM Networking:** In VirtualBox, set both VMs to "Bridge Adapter". Get IPs on each VM: `ip addr show`. Test connectivity from local: `ping server1-ip` and `ping server2-ip`.

**Security Note:** On local, generate SSH keys: `ssh-keygen -t ed25519 -C "day9-key" -f ~/.ssh/day9_key` (no passphrase for tests). Then copy to servers: `ssh-copy-id -i ~/.ssh/day9_key.pub ubuntu@server1-ip` and `ssh-copy-id -i ~/.ssh/day9_key.pub ubuntu@server2-ip`. Test: `ssh ubuntu@server1-ip` (passwordless).

## Notes
- **Why File Transfer & Remote Access Matter:**
  - Essential for system administration, automation, backups, and collaboration.
  - Secure and efficient file transfer is a core DevOps/SRE skill.

### Top File Transfer Commands

| Command | Simple Description | Examples |
|---------|--------------------|----------|
| **SSH**<br>`$ ssh user@host` | Secure remote login/commands over encrypted channel. Foundation for other transfers. | 1. Connect: `ssh ubuntu@server1-ip`<br>2. Run cmd: `ssh ubuntu@server1-ip 'ls ~/test_transfer'`<br>3. Key/port: `ssh -i ~/.ssh/day9_key -p 2222 ubuntu@server1-ip` |
| **SCP**<br>`$ scp file user@host:/path` | Secure, non-interactive file/dir copy over SSH. | 1. Upload: `scp ~/test_transfer/report.txt ubuntu@server2-ip:~/test_transfer/docs/`<br>2. Download: `scp ubuntu@server2-ip:~/test_transfer/server_report.txt .`<br>3. Dir: `scp -r ~/test_transfer/backups/ ubuntu@server2-ip:~/test_transfer/` |
| **SFTP**<br>`$ sftp user@host` | Interactive file transfer over SSH (browse dirs, multi-ops). | 1. Session: `sftp ubuntu@server2-ip`<br>2. Upload: `put ~/test_transfer/config.ini`<br>3. Download: `get server_report.txt`; Multi: `mput *.txt` |
| **RSYNC**<br>`$ rsync -avz source/ dest/` | Efficient sync—transfers only changes over SSH, preserves metadata. | 1. Sync: `rsync -avz --progress ~/test_transfer/ ubuntu@server2-ip:~/backup/`<br>2. Dry run: `rsync -n -avz ~/test_transfer/ ubuntu@server2-ip:~/backup/`<br>3. Delete: `rsync -avz --delete ~/test_transfer/ ubuntu@server2-ip:~/backup/` |
| **MOUNT** (NFS)<br>`$ sudo mount -t nfs host:/share /mnt` | Mount remote NFS share as local filesystem for seamless access. (Server setup on server1 first.) | 1. Mount: `sudo mount -t nfs server1-ip:/shared/demo /mnt/nfs`<br>2. Test: `ls /mnt/nfs`<br>3. Unmount: `sudo umount /mnt/nfs` |
| **FTP**<br>`$ ftp host` | Legacy interactive file transfer (insecure; avoid in prod). (Server setup on server1 first.) | 1. Connect: `ftp server1-ip` (login ubuntu/pw)<br>2. Upload: `put ~/test_transfer/report.txt`<br>3. Download: `get demo.txt`; Batch: `echo -e "user ubuntu\n[pw]\nput config.ini\nquit" | ftp server1-ip`

---

### SSH (Secure Shell)
**Concept:** Encrypted remote access and command execution. Foundation for SCP, SFTP, rsync.

**Step-by-Step (Local to server1):**
1. **On Local Machine:** Generate key: `ssh-keygen -t ed25519 -f ~/.ssh/day9_key` (no passphrase for tests; press Enter for defaults).
2. **On Local Machine:** Copy key to server1: `ssh-copy-id -i ~/.ssh/day9_key.pub ubuntu@server1-ip` (enter server1 password once if needed).
3. **On Local Machine:** Connect and test: `ssh ubuntu@server1-ip` (passwordless; run `whoami` to verify, then `exit`).
4. **On Local Machine:** Run remote command: `ssh ubuntu@server1-ip 'ls ~/test_transfer && uptime'` (executes on server1, shows output on local).
5. **On Local Machine (Optional):** Port forward: `ssh -L 8080:localhost:80 ubuntu@server1-ip` (forwards local port 8080 to server1's port 80; test with browser at localhost:8080).
6. **On server1 (via SSH from local):** Edit config: `sudo nano /etc/ssh/sshd_config` (uncomment/add `Port 2222`), save, then `sudo systemctl restart ssh`. Test from local: `ssh -p 2222 ubuntu@server1-ip`.

**Tips:** **On Local Machine:** Verbose debug: `ssh -v ubuntu@server1-ip`. To disable password auth on server1: SSH in, add `PasswordAuthentication no` to `/etc/ssh/sshd_config`, then `sudo systemctl restart ssh`.

---

### SCP (Secure Copy)
**Concept:** Non-interactive secure file copy over SSH.

**Step-by-Step (Local to server2):**
1. **On Local Machine:** Upload single file: `scp ~/test_transfer/docs/report.txt ubuntu@server2-ip:~/test_transfer/docs/`.
2. **On Local Machine:** Download single file: `scp ubuntu@server2-ip:~/test_transfer/docs/server_report.txt .` (saves to current local dir).
3. **On Local Machine:** Recursive dir copy: `scp -r ~/test_transfer/backups/ ubuntu@server2-ip:~/test_transfer/` (copies contents of backups to server2's test_transfer).
4. **On Local Machine:** With options (e.g., custom port/key/compress): First change port on server2 as in SSH steps, then `scp -P 2222 -i ~/.ssh/day9_key -C ~/test_transfer/config.ini ubuntu@server2-ip:/tmp/`.
5. **On Local Machine:** Verify upload: `ssh ubuntu@server2-ip 'ls -la ~/test_transfer/docs/'` (lists report.txt on server2). **On Local Machine:** Verify download: `md5sum server_report.txt` (check hash matches).

**Tips:** **On Local Machine:** For progress: `scp -v ~/test_transfer/docs/report.txt ubuntu@server2-ip:~/`. Use rsync for large/interrupted transfers.

---

### SFTP (SSH File Transfer Protocol)
**Concept:** Interactive, SSH-based file ops with browsing.

**Step-by-Step (Local to server2):**
1. **On Local Machine:** Start session: `sftp ubuntu@server2-ip` (passwordless if keys set).
2. **In SFTP Session (Remote on server2):** Navigate remote: `ls` (list server2's current dir), `cd ~/test_transfer/docs` (change to docs), `pwd` (show remote path).
3. **In SFTP Session:** Navigate local: `lls` (list local current dir), `lcd ~/test_transfer/backups` (change local to backups), `lpwd` (show local path).
4. **In SFTP Session:** Transfer files: `put report.txt` (upload from local to remote current dir), `get server_report.txt` (download to local current dir), `mput *.txt` (upload multiple .txt from local), `mget *.ini` (download multiple .ini to local).
5. **In SFTP Session:** Other ops: `mkdir newdir` (create on remote/server2), `rm oldfile.txt` (delete on remote), `rename old.txt new.txt` (rename on remote).
6. **In SFTP Session:** Exit: `exit` or Ctrl+D.
7. **On Local Machine:** Batch transfer: `echo -e "put ~/test_transfer/config.ini\nexit" | sftp ubuntu@server2-ip` (uploads config.ini non-interactively).

**Tips:** **In SFTP Session:** Use `!ls` (run local shell command). Verify post-transfer: **On Local Machine:** `ls ~/test_transfer/backups/`; **On server2 (via SSH):** `ls ~/test_transfer/docs/`.

---

### rsync (Remote Sync)
**Concept:** Efficient sync with deltas, preserves metadata.

**Step-by-Step (Local to server2):**
1. Confirm install: Already in setup; test **On Local Machine:** `rsync --version`.
2. **On Local Machine:** Dry run (preview): `rsync -n -avz ~/test_transfer/ ubuntu@server2-ip:~/backup/` (trailing / syncs contents only; -n=no changes, -a=archive/perms, -v=verbose, -z=compress).
3. **On Local Machine:** Full sync: `rsync -avz --progress ~/test_transfer/ ubuntu@server2-ip:~/backup/` (shows progress bar).
4. **On Local Machine:** Local-only sync (no remote): `rsync -avz ~/test_transfer/docs/ ~/test_transfer/backups/` (syncs docs contents to backups).
5. **On Local Machine:** Advanced sync: `rsync -avz --delete --exclude='*.tmp' ~/test_transfer/ ubuntu@server2-ip:~/backup/` (--delete removes extras on dest, --exclude skips patterns). Verify integrity: `rsync -avz --checksum ~/test_transfer/ ubuntu@server2-ip:~/backup/` (checks hashes, no transfer).
6. **On Local Machine:** Custom SSH (e.g., key/port): `rsync -e "ssh -i ~/.ssh/day9_key -p 2222" -avz ~/test_transfer/shared/ ubuntu@server2-ip:~/backup/shared/`.

**Tips:** **On Local Machine:** Automate with cron: `crontab -e`, add `0 3 * * * rsync -avz --delete ~/test_transfer/ ubuntu@server2-ip:~/backup/` (runs daily at 3 AM). Verify: **On server2 (via SSH):** `ls -la ~/backup/`.

---

### NFS (Network File System)
**Concept:** Mount remote dirs as local filesystem (Unix-focused).

**Step-by-Step (Server Setup on server1; Client on Local):**
1. **On server1 (via SSH from local):** Create share: `sudo mkdir -p /shared/demo; sudo cp ~/test_transfer/shared/demo.txt /shared/demo/; sudo chown -R nobody:nogroup /shared/demo; sudo chmod 755 /shared/demo`.
2. **On server1 (via SSH from local):** Config exports: `echo "/shared/demo 192.168.56.0/24(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports` (replace subnet if needed).
3. **On server1 (via SSH from local):** Apply changes: `sudo exportfs -ra; sudo systemctl restart nfs-kernel-server`.
4. **On server1 (via SSH from local):** Verify server: `showmount -e localhost` (should list /shared/demo).

**Client Steps (on Local Machine):**
1. **On Local Machine:** Create mount point: `sudo mkdir /mnt/nfs`.
2. **On Local Machine:** Mount: `sudo mount -t nfs server1-ip:/shared/demo /mnt/nfs`.
3. **On Local Machine:** Test access: `df -h /mnt/nfs` (shows mounted size), `ls /mnt/nfs` (lists demo.txt), `echo "Client edit v1" | sudo tee /mnt/nfs/edit.txt` (write file).
4. **On server1 (via SSH from local):** Verify sync: `cat /shared/demo/edit.txt` (shows "Client edit v1").
5. **On Local Machine:** Unmount: `sudo umount /mnt/nfs`.

**Tips:** **On Local Machine:** For persistent mount, add to `/etc/fstab`: `server1-ip:/shared/demo /mnt/nfs nfs defaults 0 0`, then `sudo mount -a`. Use Kerberos for advanced auth.

---

### FTP (File Transfer Protocol) - Legacy Warning
**Concept:** Basic file transfer; insecure (plain text). Use only for air-gapped or FTPS. Avoid in production.

**Step-by-Step (Server Setup on server1; Client on Local):**
1. **On server1 (via SSH from local):** Config vsftpd: `sudo nano /etc/vsftpd.conf` (uncomment/add: `local_enable=YES`, `write_enable=YES`, `chroot_local_user=YES`; save/exit).
2. **On server1 (via SSH from local):** Apply: `sudo systemctl restart vsftpd`.
3. **On server1 (via SSH from local):** Test server: `ftp localhost` (login as ubuntu/pw, `ls`, `quit`).

**Client Steps (on Local Machine):**
1. **On Local Machine:** Connect interactively: `ftp server1-ip` (login: ubuntu / pw; at ftp> prompt).
2. **In FTP Session:** Commands: `binary` (set mode for non-text), `put ~/test_transfer/docs/report.txt` (upload), `get ~/test_transfer/shared/demo.txt` (download to local), `ls` (list remote), `cd /home/ubuntu/test_transfer` (remote dir), `quit` (exit).
3. **On Local Machine:** Batch transfer: `echo -e "user ubuntu\n[password]\ncd /home/ubuntu/test_transfer\nput ~/test_transfer/config.ini\nquit" | ftp server1-ip` (replace [password]; uploads config.ini).

**Tips:** **On Local Machine:** For secure FTPS: `sudo apt install lftp; lftp -u ubuntu ftps://server1-ip` (then `put file.txt`). Disable FTP in prod by commenting lines in vsftpd.conf and restarting.

**Security:** Risks: Eavesdropping (plain text creds/files). Mitigate: Restrict with firewall, use FTPS, or switch to SFTP.

---

## Sample Exercises
1. **On Local and server1:** Set up SSH key-based authentication (generate on local, copy to server1).
2. **On Local and server2:** Transfer a directory recursively to server2 using `scp`.
3. **On Local and server2:** Synchronize ~/test_transfer on local to ~/backup on server2 using `rsync` and verify changes.
4. **On server1 (server) and Local (client):** Mount an NFS share from server1 on local.
5. **On Local and server2:** Use SFTP to upload report.txt from local and download server_report.txt from server2 interactively.
6. **On Local and server2:** Perform a dry run with `rsync` before syncing ~/test_transfer to server2.
7. **On server2:** Restrict SSH access to only user 'ubuntu' (edit sshd_config).
8. **On server1 (server) and Local (client):** Set up FTP server on server1 and transfer report.txt from local (note insecurities).
9. **On Local and server1:** Mount SSHFS for /home/ubuntu/test_transfer from server1 to /mnt/sshfs on local.

## Solutions
1. **SSH Key Setup (Local to server1):**
   **On Local Machine:**
   ```bash
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/day9_key  # Generate key pair (no passphrase)
   ssh-copy-id -i ~/.ssh/day9_key.pub ubuntu@server1-ip  # Copy public key
   ssh ubuntu@server1-ip  # Test passwordless login (run 'exit' after)
   ```

2. **SCP Directory Transfer (Local to server2):**
   **On Local Machine:**
   ```bash
   scp -r ~/test_transfer/backups/ ubuntu@server2-ip:~/test_transfer/  # Recursive upload
   scp -P 2222 -r ~/test_transfer/shared/ ubuntu@server2-ip:/tmp/  # Custom port example
   ```

3. **rsync Synchronization (Local to server2):**
   **On Local Machine:**
   ```bash
   rsync -avz --progress ~/test_transfer/ ubuntu@server2-ip:~/backup/  # Sync with progress
   rsync -n -avz ~/test_transfer/ ubuntu@server2-ip:~/backup/  # Dry run first
   rsync -avz --delete ~/test_transfer/ ubuntu@server2-ip:~/backup/  # Delete extra files on dest
   ```
   **On server2 (via SSH):** `ls -la ~/backup/` (verify).

4. **NFS Mount (server1 as server, Local as client):**
   **On server1:**
   ```bash
   # /etc/exports addition
   echo "/shared/data 192.168.56.0/24(rw,sync,no_root_squash)" | sudo tee -a /etc/exports
   sudo exportfs -ra
   ```
   **On Local Machine:**
   ```bash
   sudo mount -t nfs server1-ip:/shared/data /mnt/nfs
   ls /mnt/nfs  # Test
   sudo umount /mnt/nfs
   ```

5. **SFTP Session (Local to server2):**
   **On Local Machine:**
   ```bash
   sftp ubuntu@server2-ip
   # In session:
   put ~/test_transfer/report.txt               # Upload
   get ~/test_transfer/server_report.txt        # Download
   mput ~/test_transfer/*.txt                   # Upload multiple
   exit                                         # Close session
   ```

6. **rsync Dry Run (Local to server2):**
   **On Local Machine:**
   ```bash
   rsync -n -avz ~/test_transfer/ ubuntu@server2-ip:~/backup/  # Preview changes
   rsync -avz ~/test_transfer/ ubuntu@server2-ip:~/backup/     # Execute
   ```

7. **SSH Access Restriction (on server2):**
   **On server2 (via SSH):**
   ```bash
   # Edit /etc/ssh/sshd_config
   echo "AllowUsers ubuntu" | sudo tee -a /etc/ssh/sshd_config
   sudo systemctl restart ssh
   ```

8. **FTP Transfer (server1 as server, Local as client):**
   **On server1:**
   ```bash
   sudo nano /etc/vsftpd.conf  # Enable local_enable=YES, write_enable=YES
   sudo systemctl restart vsftpd
   ```
   **On Local Machine:**
   ```bash
   ftp server1-ip  # Login ubuntu/pw, then put ~/test_transfer/report.txt, quit
   # Batch: echo -e "user ubuntu\n[pw]\nput ~/test_transfer/config.ini\nquit" | ftp server1-ip
   ```

9. **SSHFS Mount (Local to server1):**
   **On Local Machine:**
   ```bash
   sudo mkdir /mnt/sshfs
   sshfs ubuntu@server1-ip:/home/ubuntu/test_transfer /mnt/sshfs -o IdentityFile=~/.ssh/day9_key
   ls /mnt/sshfs  # Access files
   fusermount -u /mnt/sshfs  # Unmount
   ```

## Completion Checklist
- [ ] Can transfer files securely using SCP and SFTP (local to server2)
- [ ] Understand rsync for efficient synchronization (local to server2)
- [ ] Know how to mount and use NFS shares (server1 to local)
- [ ] Configured SSH key-based authentication (local to servers)
- [ ] Understand security implications of each method
- [ ] Set up and tested FTP (server1 to local, with warnings)
- [ ] Automated a rsync task via cron (on local)

---

**End of Day 9!** You've nailed secure transfers and sharing—time to streamline your workflow.

## Next Steps
Proceed to [Day 10: Environment Variables, Aliases & Shell Customization](../Day_10/notes_and_exercises.md) to customize your shell environment.�
