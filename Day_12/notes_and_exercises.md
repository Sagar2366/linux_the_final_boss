# Day 12: Compression, Archiving, and Backups

## Learning Objectives
By the end of Day 12, you will:
- Master compression and archiving tools
- Implement effective backup strategies
- Automate backup processes
- Verify backup integrity
- Understand different backup types and use cases

**Estimated Time:** 30 mins

## Sample Environment Setup
Exercises are local, no VMs needed. Use your local machine (e.g., Ubuntu/Mac with Bash).
```
mkdir -p ~/day12_test/{data,backups,scripts}
echo "Important data line 1" > ~/day12_test/data/file1.txt
echo "Important data line 2" >> ~/day12_test/data/file1.txt
echo "Sample config" > ~/day12_test/data/config.ini
echo "Binary-like data" > ~/day12_test/data/binary.dat
cp ~/day12_test/data/file1.txt ~/day12_test/data/file2.txt
touch ~/day12_test/data/{temp.tmp,junk.log}
echo '#!/bin/bash\necho "Backup starting at $(date)"\ntar -czf /tmp/backup.tar.gz ~/day12_test/data/' > ~/day12_test/scripts/backup.sh
chmod +x ~/day12_test/scripts/backup.sh

# View initial state
ls -la ~/day12_test/data/
du -sh ~/day12_test/data/
```

## Why These Tools Matter:
  - Essential for saving space, protecting data, and efficient transfers in Linux environments.
  - Critical for DevOps, SRE, and sysadmin roles to prevent data loss and optimize storage.

| Command | Simple Description | Examples |
|---------|--------------------|----------|
| **COMPRESSION**<br>`$ gzip file.txt` | Reduce file size. | 1. Basic: `gzip file.txt` (creates file.txt.gz)<br>2. Decompress: `gunzip file.txt.gz`<br>3. Keep original: `gzip -k file.txt` |
| **ARCHIVING**<br>`$ tar -cvf archive.tar dir/` | Bundle files into one. | 1. Create: `tar -czvf archive.tar.gz dir/`<br>2. Extract: `tar -xzvf archive.tar.gz`<br>3. List: `tar -tzf archive.tar.gz` |
| **BACKUP**<br>`$ rsync -av src/ dest/` | Sync/copy with smarts. | 1. Mirror: `rsync -av --delete ~/data/ ~/backup/`<br>2. Progress: `rsync -av --progress src/ dest/`<br>3. Exclude: `rsync -av --exclude='*.tmp' src/ dest/` |
| **VERIFY**<br>`$ sha256sum file` | Check integrity. | 1. Generate: `sha256sum archive.tar.gz > checksum.sha256`<br>2. Check: `sha256sum -c checksum.sha256`<br>3. Tar test: `tar -tzf archive.tar.gz` |

- **Compression Tools:**
  - Shrink files for storage/transfer. gzip (fast, good for text), bzip2 (better ratio, slower), xz (best ratio, slowest).
  - Parallel variants: pigz (parallel gzip), pbzip2 (parallel bzip2) for multi-core speed.

  **Examples:**
  - gzip: `gzip ~/day12_test/data/file1.txt` (compresses to .gz). Decompress: `gunzip ~/day12_test/data/file1.txt.gz`.
  - bzip2: `bzip2 ~/day12_test/data/file2.txt` (to .bz2). Decompress: `bunzip2 ~/day12_test/data/file2.txt.bz2`.
  - xz: `xz ~/day12_test/data/config.ini` (to .xz). Decompress: `unxz ~/day12_test/data/config.ini.xz`.
  - Compare: `ls -lh ~/day12_test/data/` before/after to see size diffs.
  - zip (cross-platform): `zip archive.zip ~/day12_test/data/*.txt`; `unzip archive.zip`.

---

- **Archiving Tools:**
- tar (Tape ARchive) bundles files/directories, often with compression. Flags: c (create), x (extract), v (verbose), f (file), z (gzip), j (bzip2), J (xz).

| Operator | Description | Example |
|----------|-------------|---------|
| `-cvf` | Create verbose archive | `tar -cvf archive.tar ~/day12_test/data/` (bundles without compression) |
| `-xvf` | Extract verbose | `tar -xvf archive.tar` (unpacks to current dir) |
| `-czvf` | Create gzip-compressed | `tar -czvf archive.tar.gz ~/day12_test/data/` |
| `-xzvf` | Extract gzip | `tar -xzvf archive.tar.gz -C ~/extracted/` (to specific dir) |
| `-tzf` | List contents | `tar -tzf archive.tar.gz \| head -5` |

### Advanced tar:
- Exclude: `tar -czvf backup.tar.gz --exclude='*.tmp' --exclude='junk.log' ~/day12_test/data/`.
- Specific extract: `tar -xzvf archive.tar.gz data/file1.txt` (one file).

**Example:**
  - Create: `tar -czvf ~/day12_test/backups/data.tar.gz ~/day12_test/data/`.
  - List: `tar -tzf ~/day12_test/backups/data.tar.gz`.
  - Extract: `mkdir ~/day12_test/extracted && tar -xzvf ~/day12_test/backups/data.tar.gz -C ~/day12_test/extracted/`.

---

- **Backup Tools:**
  - rsync: rsync (remote sync) is a versatile file synchronization tool that copies files and directories efficiently, often over networks, by transferring only differences (delta-transfer algorithm). It's ideal for backups because it minimizes bandwidth/data usage, handles interruptions (resumable), and preserves file attributes like permissions, timestamps, ownership, and symlinks.
  - cp: Simple copy (`cp -a` for archive mode).

  **Examples:**
  - rsync basic: `rsync -av ~/day12_test/data/ ~/day12_test/backups/mirror/`.
  - With delete: `rsync -av --delete ~/day12_test/data/ ~/day12_test/backups/mirror/` (removes extras in dest).
  - Strategies: Full (all data), Incremental (changes since last), Differential (changes since full).

---

- **Automation & Verification:**
  - Cron: Schedule jobs (`crontab -e`).
  - Checksums: sha256sum/md5sum for integrity.

  **Examples:**
  - Cron daily: `0 2 * * * ~/day12_test/scripts/backup.sh` (2 AM daily).
  - Verify: `find ~/day12_test/backups -type f -exec sha256sum {} \; > ~/day12_test/checksums.txt`. Then `sha256sum -c ~/day12_test/checksums.txt`.
  - Tar integrity: `tar -tzf ~/day12_test/backups/data.tar.gz > /dev/null && echo "OK" || echo "Corrupt"`.

  **3-2-1 Rule:** 3 copies of data, on 2 different media, 1 offsite.

---

- **Best Practices:**
  - Compress before archiving for efficiency.
  - Test restores quarterly, don't trust untested backups.
  - Use rsync for live syncs; tar for snapshots.
  - Encrypt (gpg) sensitive data: `tar -czvf - data/ | gpg -c > backup.gpg`.
  - Log everything: Redirect script output to logs.

## Sample Exercises
1. Compress and decompress a file using gzip and bzip2.
2. Create a tar archive of a directory and extract it.
3. Use rsync to backup your home directory to another location.
4. Schedule a daily backup using cron.
5. Verify the integrity of a backup file using checksums.
6. Create an incremental backup system.
7. Exclude specific file types from a backup.

## Solutions
1. **Compression/Decompression:**
   ```bash:disable-run
   # gzip
   gzip file.txt                        # Creates file.txt.gz
   gunzip file.txt.gz                   # Restores file.txt
   
   # bzip2
   bzip2 file.txt                       # Creates file.txt.bz2
   bunzip2 file.txt.bz2                 # Restores file.txt
   
   # Keep original
   gzip -k file.txt                     # Keep original file
   ```

2. **Tar operations:**
   ```bash
   # Create archive
   tar -czvf backup.tar.gz mydir/
   
   # Extract archive
   tar -xzvf backup.tar.gz
   
   # List contents
   tar -tzf backup.tar.gz
   ```

3. **rsync backup:**
   ```bash
   rsync -av --progress ~/ /backup/home_backup/
   rsync -av --delete ~/ /backup/home_backup/  # Delete extra files
   ```

4. **Automated backup:**
   ```bash
   # Edit crontab
   crontab -e
   
   # Add daily backup at 2 AM
   0 2 * * * /usr/local/bin/backup_script.sh
   
   # Backup script example
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   tar -czf /backup/home_$DATE.tar.gz /home/user/
   ```

5. **Integrity verification:**
   ```bash
   # Generate checksum
   sha256sum backup.tar.gz > backup.sha256
   
   # Verify later
   sha256sum -c backup.sha256
   
   # Test archive integrity
   tar -tzf backup.tar.gz > /dev/null
   ```

6. **Incremental backup:**
   ```bash
   # Full backup with snapshot
   tar -czf full_backup.tar.gz -g backup.snar /home/user/
   
   # Incremental backup
   tar -czf incr_backup.tar.gz -g backup.snar /home/user/
   ```

7. **Exclude files:**
   ```bash
   # tar exclusions
   tar -czf backup.tar.gz --exclude='*.log' --exclude='tmp/*' /home/user/
   
   # rsync exclusions
   rsync -av --exclude='*.log' --exclude='tmp/' ~/ /backup/
   ```

## Sample Interview Questions
1. What is the difference between compression and archiving?
2. How do you create and extract a compressed tarball?
3. What are the advantages of using rsync for backups?
4. How do you automate backups in Linux?
5. How do you verify the integrity of a backup?
6. What is the risk of using `dd` for disk backups?
7. How do you exclude files from a tar or rsync backup?
8. What is the difference between gzip, bzip2, and xz?
9. How do you restore a single file from a tar archive?
10. Why is it important to test your backups?

## Interview Question Answers
1. **Compression vs Archiving:** Compression reduces file size; archiving combines multiple files. tar can do both
2. **Tarball Operations:** `tar -czvf archive.tar.gz files/` creates; `tar -xzvf archive.tar.gz` extracts
3. **rsync Advantages:** Incremental transfers, resume capability, preserves permissions, bandwidth efficient
4. **Automated Backups:** Use cron jobs, systemd timers, or backup software with scheduling
5. **Backup Verification:** Use checksums (sha256sum), test extractions, verify file counts and sizes
6. **dd Risks:** Can overwrite wrong disk, no compression, copies bad sectors, requires exact space
7. **File Exclusions:** Use `--exclude` with tar/rsync, or `.rsyncignore` files
8. **Compression Tools:** gzip (fast), bzip2 (better compression), xz (best compression, slowest)
9. **Single File Restore:** `tar -xzf archive.tar.gz path/to/file` extracts specific file
10. **Backup Testing:** Ensures recoverability, validates backup integrity, identifies corruption early

## Completion Checklist
- [ ] Can compress/decompress files with different tools
- [ ] Understand tar archiving and extraction
- [ ] Know how to use rsync for backups
- [ ] Can automate backups with cron
- [ ] Understand backup verification methods
- [ ] Know different backup strategies

## Next Steps
Proceed to [Day 13: Process Management & Scheduling](../Day_13/notes_and_exercises.md) to learn task automation and process control.
