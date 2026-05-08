# Day 19: Advanced Linux Storage & Filesystems (ext4, xfs, btrfs, quotas, tuning)

## Table of Contents

- [Day 19: Advanced Linux Storage & Filesystems (ext4, xfs, btrfs, quotas, tuning)](#day-19-advanced-linux-storage-&-filesystems-ext4-xfs-btrfs-quotas-tuning)
  - [Learning Objectives](#learning-objectives)
  - [Notes](#notes)
  - [Sample Exercises](#sample-exercises)
  - [Solutions](#solutions)
  - [Sample Interview Questions](#sample-interview-questions)
  - [Interview Question Answers](#interview-question-answers)
  - [Completion Checklist](#completion-checklist)
  - [Key Commands Summary](#key-commands-summary)
- [Filesystem creation](#filesystem-creation)
- [Mounting](#mounting)
- [Quotas](#quotas)
- [Maintenance](#maintenance)
  - [Best Practices](#best-practices)
  - [Next Steps](#next-steps)


## Learning Objectives
By the end of Day 19, you will:
- Understand different Linux filesystems and their use cases
- Create, mount, and manage filesystems
- Implement disk quotas for users and groups
- Tune filesystem performance
- Troubleshoot storage issues

**Estimated Time:** 4-5 hours

## Notes
- **Why Advanced Storage Matters:**
  - Modern systems require robust, flexible, and high-performance storage solutions.
  - Understanding filesystems, quotas, and tuning is essential for reliability and scalability.

```mermaid
flowchart TD
    A[Linux Storage & Filesystems] --> B[Filesystem Types]
    A --> C[Storage Management]
    A --> D[Performance Tuning]
    A --> E[Advanced Features]
    
    B --> B1[ext4<br/>Reliable, Default]
    B --> B2[XFS<br/>High Performance]
    B --> B3[Btrfs<br/>Copy-on-Write]
    B --> B4[ZFS<br/>Enterprise]
    B --> B5[NTFS/FAT32<br/>Compatibility]
    
    C --> C1[Partitioning<br/>fdisk, parted]
    C --> C2[Formatting<br/>mkfs commands]
    C --> C3[Mounting<br/>mount, fstab]
    C --> C4[Disk Quotas<br/>User/Group limits]
    
    D --> D1[Mount Options<br/>noatime, barrier]
    D --> D2[I/O Schedulers<br/>deadline, noop]
    D --> D3[SSD Optimization<br/>TRIM, alignment]
    D --> D4[Block Size Tuning]
    
    E --> E1[Snapshots<br/>Point-in-time]
    E --> E2[Compression<br/>Space saving]
    E --> E3[Encryption<br/>LUKS, dm-crypt]
    E --> E4[Checksumming<br/>Data integrity]
    
    F[Storage Stack] --> F1[Applications]
    F1 --> F2[VFS Layer]
    F2 --> F3[Filesystem]
    F3 --> F4[Block Layer]
    F4 --> F5[Device Drivers]
    F5 --> F6[Physical Storage]
    
    style A fill:#f96
    style B fill:#9f6
    style F fill:#69f
```

- **Common Linux Filesystems:**
  - `ext4`: Default on most distros; journaling, large file support, stable.
  - `xfs`: High-performance, scalable, good for large files and parallel I/O.
  - `btrfs`: Advanced features (snapshots, compression, checksumming, subvolumes).
  - `vfat`, `ntfs`: For interoperability with Windows/external drives.

- **Creating & Managing Filesystems:**
  - `mkfs.ext4 /dev/sdX1` — Create ext4 filesystem
  - `mkfs.xfs /dev/sdX1` — Create xfs filesystem
  - `mkfs.btrfs /dev/sdX1` — Create btrfs filesystem
  - `mount /dev/sdX1 /mnt` — Mount filesystem
  - `umount /mnt` — Unmount
  - `/etc/fstab` — Persistent mounts

- **Filesystem Maintenance:**
  - `fsck /dev/sdX1` — Check and repair
  - `tune2fs` — Tune ext2/3/4 parameters (e.g., reserved blocks, labels)
  - `xfs_repair`, `xfs_growfs` — XFS repair and online resize
  - `btrfs scrub`, `btrfs balance`, `btrfs snapshot`

- **Quotas:**
  - Enforce disk usage limits per user/group
  - Enable in `/etc/fstab` with `usrquota,grpquota`
  - `quotacheck`, `edquota`, `quota`, `repquota` for management

- **Filesystem Tuning:**
  - Adjust mount options for performance: `noatime`, `data=writeback`, `barrier=0`
  - Use `iostat`, `iotop`, `dstat` for performance monitoring
  - Align partitions for SSDs, use TRIM (`fstrim`)

- **Best Practices:**
  - Choose the right filesystem for your workload
  - Regularly check and repair filesystems
  - Monitor disk usage and set quotas for multi-user systems
  - Document all changes and test before production



- **Filesystem Performance Tuning:**
  ```bash
  # Mount options for performance
  mount -o noatime,data=writeback /dev/sdb1 /mnt
  
  # /etc/fstab entry
  /dev/sdb1 /data ext4 defaults,noatime,data=writeback 0 2
  
  # SSD optimization
  mount -o noatime,discard /dev/sdb1 /mnt
  fstrim /mnt                      # Manual TRIM
  ```

- **Quota Management:**
  ```bash
  # Enable quotas in /etc/fstab
  /dev/sdb1 /home ext4 defaults,usrquota,grpquota 0 2
  
  # Initialize quota files
  quotacheck -cug /home
  quotaon /home
  
  # Set user quota (1GB soft, 1.2GB hard)
  edquota -u username
  ```

- **Btrfs Advanced Features:**
  ```bash
  # Create subvolumes
  btrfs subvolume create /mnt/data
  
  # Take snapshot
  btrfs subvolume snapshot /mnt/data /mnt/data-backup
  
  # Enable compression
  mount -o compress=zstd /dev/sdb1 /mnt
  ```

## Sample Exercises
1. Create and mount an ext4, xfs, and btrfs filesystem on loopback devices.
2. Set up user quotas on an ext4 filesystem and test enforcement.
3. Take a btrfs snapshot and restore from it.
4. Tune mount options for performance and measure the impact.
5. Repair a corrupted filesystem using the appropriate tool.

## Solutions
1. **Create filesystems:**
   ```bash
   # Create loop devices for testing
   dd if=/dev/zero of=/tmp/disk1.img bs=1M count=100
   losetup /dev/loop1 /tmp/disk1.img
   
   # Create different filesystems
   mkfs.ext4 /dev/loop1
   mkfs.xfs /dev/loop2
   mkfs.btrfs /dev/loop3
   
   # Mount them
   mkdir -p /mnt/{ext4,xfs,btrfs}
   mount /dev/loop1 /mnt/ext4
   ```

2. **Setup quotas:**
   ```bash
   # Edit /etc/fstab
   /dev/sdb1 /home ext4 defaults,usrquota,grpquota 0 2
   
   # Remount and initialize
   mount -o remount /home
   quotacheck -cug /home
   quotaon /home
   
   # Set limits
   edquota -u testuser
   ```

3. **Btrfs snapshots:**
   ```bash
   # Create subvolume
   btrfs subvolume create /mnt/data
   
   # Take snapshot
   btrfs subvolume snapshot /mnt/data /mnt/snapshots/data-$(date +%Y%m%d)
   
   # List snapshots
   btrfs subvolume list /mnt
   ```

4. **Performance tuning:**
   ```bash
   # Test current performance
   iostat -x 1 5
   
   # Add performance options to /etc/fstab
   /dev/sdb1 /data ext4 defaults,noatime,data=writeback 0 2
   
   # Remount and test again
   mount -o remount /data
   ```

5. **Filesystem repair:**
   ```bash
   # Unmount first
   umount /dev/sdb1
   
   # Check and repair
   fsck.ext4 -f /dev/sdb1          # ext4
   xfs_repair /dev/sdb1            # xfs
   btrfs check --repair /dev/sdb1  # btrfs (use carefully)
   ```

## Sample Interview Questions
1. What are the main differences between ext4, xfs, and btrfs?
2. How do you create and mount a new filesystem?
3. How do you enable and manage disk quotas?
4. What are filesystem snapshots and why are they useful?
5. How do you check and repair filesystem errors?
6. What mount options can improve performance?
7. How do you monitor disk I/O performance?
8. How do you migrate data between filesystems?
9. What are the risks of disabling journaling or barriers?
10. How do you automate filesystem checks and maintenance?

## Interview Question Answers
1. **Filesystem Comparison:** ext4 (stable, general-purpose), xfs (high-performance, large files), btrfs (advanced features, snapshots)
2. **Filesystem Creation:** Use mkfs.* to create, mount to attach, edit /etc/fstab for persistence
3. **Quota Management:** Enable in /etc/fstab with usrquota/grpquota, use quotacheck, edquota, quota commands
4. **Snapshots:** Point-in-time filesystem state capture; useful for backups, rollbacks, testing
5. **Filesystem Repair:** fsck for ext4, xfs_repair for xfs, btrfs check for btrfs (unmount first)
6. **Performance Options:** noatime, data=writeback improve speed but may risk data integrity
7. **I/O Monitoring:** iostat, iotop, dstat, sar for disk performance analysis
8. **Data Migration:** Use rsync, tar, or cp -a; verify integrity after migration
9. **Journaling Risks:** Disabling improves speed but increases data loss risk on crashes
10. **Automated Maintenance:** Use cron jobs or systemd timers for regular fsck and cleanup

## Completion Checklist
- [ ] Understand different filesystem types and use cases
- [ ] Can create, mount, and manage filesystems
- [ ] Know how to implement and manage quotas
- [ ] Familiar with performance tuning options
- [ ] Can troubleshoot filesystem issues
- [ ] Understand advanced features like snapshots

## Key Commands Summary
```bash
# Filesystem creation
mkfs.ext4 /dev/sdX1             # Create ext4
mkfs.xfs /dev/sdX1              # Create xfs
mkfs.btrfs /dev/sdX1            # Create btrfs

# Mounting
mount /dev/sdX1 /mnt            # Mount filesystem
umount /mnt                     # Unmount

# Quotas
quotacheck -cug /home           # Initialize quotas
edquota -u username             # Edit user quota
quota -u username               # Check quota usage

# Maintenance
fsck /dev/sdX1                  # Check filesystem
fstrim /mnt                     # SSD TRIM
```

## Best Practices
- Choose appropriate filesystem for workload
- Regular filesystem checks and maintenance
- Monitor disk usage and set quotas appropriately
- Use performance tuning carefully (test first)
- Backup before major filesystem operations
- Document filesystem configurations

## Next Steps
Proceed to [Day 20: Basic Shell Scripting](../Day_20/notes_and_exercises.md) to learn automation with scripts.
