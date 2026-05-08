

## Table of Contents

  - [Detailed Phase Explanations (Optional)](#detailed-phase-explanations-optional)
    - [1. Power & Reset Vector](#1.-power-&-reset-vector)
    - [2. Firmware (BIOS vs UEFI)](#2.-firmware-bios-vs-uefi)
    - [3. Disk Structure & Loader Entry](#3.-disk-structure-&-loader-entry)
    - [4. GRUB2 Bootloader](#4.-grub2-bootloader)
    - [5. Kernel Load & Decompression](#5.-kernel-load-&-decompression)
    - [6. Initramfs (Early User Space)](#6.-initramfs-early-user-space)
    - [7. Switch Root](#7.-switch-root)
    - [8. PID 1 (systemd)](#8.-pid-1-systemd)
    - [9. Services & Targets](#9.-services-&-targets)
    - [10. User Interaction](#10.-user-interaction)

- **What is the Linux Boot Process?**
  - The boot process is the sequence of steps the system takes to start up and become ready for use.
  - Understanding the boot process is crucial for troubleshooting startup issues and managing services.
  <img width="800" height="800" alt="0213-linux-boot-process-explained" src="https://github.com/user-attachments/assets/75e328e4-52f5-4e4b-a0d2-a680d87ce03c" />
1. Power & Reset Vector  
   System receives stable power; CPU jumps to the architecture-defined reset vector and begins executing firmware code.
2. Firmware (BIOS or UEFI)  
   Performs POST, minimal hardware initialization, enumerates bootable devices, chooses a boot entry (boot order / NVRAM).
3. Disk Structure & Loader Entry  
   - Legacy BIOS path: Read MBR (LBA 0) → tiny bootstrap → load GRUB core.  
   - UEFI path: Read GPT, mount/scan ESP (FAT32), load EFI executable (e.g. `grubx64.efi` or shim chain).
4. GRUB2 Bootloader  
   Loads modules, parses `grub.cfg`, presents menu (if enabled), selects kernel + initramfs, constructs kernel command line.
5. Kernel Load & Decompression  
   Kernel image is copied into RAM, decompressed, establishes CPU modes (protected/long), sets up early memory management & interrupts.
6. Initramfs (Early User Space)  
   Temporary cpio archive with minimal user space tools: loads storage/crypto drivers, assembles RAID/LVM, unlocks LUKS, locates real root.
7. Switch to Real Root Filesystem  
   Root filesystem is mounted; `switch_root` (or older `pivot_root`) transitions from initramfs to the actual root; initramfs is freed.
8. Init Process (PID 1: systemd)  
   `systemd` starts as PID 1, parses dependency graph, mounts additional filesystems, activates sockets, timers, and services in parallel.
9. Services & Targets Reached  
   Network stack, logging, display manager (if graphical), and other units come online; default target (`multi-user.target` or `graphical.target`) is achieved.
10. User Interaction  
    TTY login prompts (`agetty`), SSH access, and/or graphical greeter become available—the system is ready for workload and users.

---

## Detailed Phase Explanations (Optional)

### 1. Power & Reset Vector
- Hardware initializes base electrical conditions.
- CPU fetches first instruction at fixed physical address.
- Corruption here = pre-boot failure (no firmware banner, no beeps).

### 2. Firmware (BIOS vs UEFI)
| Aspect | BIOS (Legacy) | UEFI (Modern) |
|--------|---------------|---------------|
| Execution Mode | 16‑bit real mode | 32/64‑bit native |
| Disk Interface | INT 13h | Drivers + EFI protocols |
| Partition Scheme | MBR only | GPT (with protective MBR) |
| Secure Boot | Not available | Supported |
| Extensibility | Minimal | Shell, diagnostics, network stack |
| Boot Entries | Sequential scan | NVRAM-managed entries |
Tasks: POST, memory sizing, basic device presence, choose boot entry.

### 3. Disk Structure & Loader Entry
- **MBR Layout (512 bytes)**: 446 boot code + 64 partition table + 0x55AA signature.
- **GPT Advantages**: Redundancy (primary + backup headers), CRC32 integrity, large partition count.
- **ESP**: Dedicated FAT32 partition (usually 100–500 MB) containing EFI executables (`/EFI/<vendor>/*.efi`).

### 4. GRUB2 Bootloader
Responsibilities:
- Build boot menu (multi-OS or multi-kernel).
- Load kernel (`/boot/vmlinuz-*`) + initramfs (`/boot/initramfs-*`).
- Pass kernel parameters (command line).
Key Files:
- `/etc/default/grub` → human-editable defaults.
- Generated config: `/boot/grub2/grub.cfg` (BIOS / many RPM distros) or `/boot/efi/EFI/<distro>/grub.cfg` (some UEFI layouts).

### 5. Kernel Load & Decompression
Sequence:
1. Decompress kernel to RAM.
2. Initialize memory management (page tables, zones).
3. Bring up interrupts, timers, CPU cores (SMP).
4. Initialize essential buses (PCI enumeration).
5. Register base drivers (others deferred).
6. Jump into initramfs `/init`.

### 6. Initramfs (Early User Space)
Contains:
- BusyBox or minimal utilities.
- Storage/crypto modules not built into kernel.
- Scripts for: RAID assembly (`mdadm`), LVM activation, LUKS unlock (`cryptsetup`), filesystem detection (UUID/LABEL).
Inspection:
```bash
lsinitrd /boot/initramfs-$(uname -r).img | less    # dracut-based
```
Rebuild:
- RHEL/Fedora: `dracut -f`
- Debian/Ubuntu: `update-initramfs -u`
Failure Symptoms:
- Dropped to `(initramfs)` shell.
- “Cannot find root device” / “Unable to mount root fs”.

### 7. Switch Root
- `switch_root` replaces the temporary initramfs root with the real root, freeing RAM.
- Mounts from `/etc/fstab` proceed via systemd mount units.
- If encrypted: unlock → map → mount → switch.

### 8. PID 1 (systemd)
Core Roles:
- Dependency resolution graph (units with `Requires=`, `Wants=`, `Before=`/`After=`).
- Parallel startup (faster than sequential SysVinit).
- Activation methods (socket, bus, path, timer).
- Supervision (restarts, failure isolation).
- Integrated logging via `journald`.
Primary Unit Types:
`service`, `socket`, `mount`, `automount`, `timer`, `path`, `target`, `device`, `swap`, `slice`, `scope`.

### 9. Services & Targets
Runlevel Mapping (for legacy reference):
| Legacy Runlevel | systemd Target | Meaning |
|-----------------|----------------|---------|
| 0 | `poweroff.target` | Halt system |
| 1 | `rescue.target` | Single-user (maintenance) |
| 3 | `multi-user.target` | Non-graphical multi-user |
| 5 | `graphical.target` | Multi-user + GUI |
| 6 | `reboot.target` | Reboot |
| S/Emergency | `emergency.target` | Minimal root shell |
Default target symlink: `/etc/systemd/system/default.target`.

### 10. User Interaction
- TTY login: `agetty` spawns `/bin/login`.
- GUI: Display manager (GDM/SDDM/LightDM) started as a service.
- Remote: `sshd.service` often comes online before graphics (headless administration).

---
