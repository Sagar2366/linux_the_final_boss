# Day 02: Virtualization & Setting Up Linux (Focus: VirtualBox Hands-On)

## Table of Contents

- [Day 02: Virtualization & Setting Up Linux (Focus: VirtualBox Hands-On)](#day-02-virtualization-&-setting-up-linux-focus-virtualbox-hands-on)
  - [Learning Objectives](#learning-objectives)
  - [Why Learn Virtualization?](#why-learn-virtualization)
    - [Why It Matters to You as a DevOps/SRE/Cloud Engineer](#why-it-matters-to-you-as-a-devopssrecloud-engineer)
  - [What is Virtualization?](#what-is-virtualization)
    - [Key Components and How It Works](#key-components-and-how-it-works)
      - [Benefits (Why Interviewers Love This)](#benefits-why-interviewers-love-this)
      - [Drawbacks (Show Balance)](#drawbacks-show-balance)
  - [Hypervisors: The Engine of Virtualization](#hypervisors-the-engine-of-virtualization)
    - [Type 1 vs. Type 2: The Big Divide](#type-1-vs.-type-2-the-big-divide)
    - [Emerging Trends in 2025](#emerging-trends-in-2025)
  - [Quick Peek: The Linux Boot Process](#quick-peek-the-linux-boot-process)
    - [Detailed Step-by-Step](#detailed-step-by-step)
  - [Step-by-Step: Installing Your First VM in VirtualBox](#step-by-step-installing-your-first-vm-in-virtualbox)
    - [Prerequisites](#prerequisites)
    - [Step 1: Launch VirtualBox & Create VM](#step-1-launch-virtualbox-&-create-vm)
    - [Step 2: Configure VM Settings](#step-2-configure-vm-settings)
    - [Step 3: Install Ubuntu in the VM](#step-3-install-ubuntu-in-the-vm)
    - [Step 4: First Tweaks in Your VM](#step-4-first-tweaks-in-your-vm)
  - [Playing with Your VM: Networking, Snapshots, & More](#playing-with-your-vm-networking-snapshots-&-more)
    - [Check Network Connectivity](#check-network-connectivity)
    - [Take & Use Snapshots](#take-&-use-snapshots)
    - [Quick Tweaks & Exploration](#quick-tweaks-&-exploration)
  - [Hands-on Exercises & Lab](#hands-on-exercises-&-lab)
    - [Part 1: VM Creation & First Boot](#part-1-vm-creation-&-first-boot)
    - [Part 2: Network Check & Fix](#part-2-network-check-&-fix)
    - [Part 3: Snapshot Practice](#part-3-snapshot-practice)
    - [Part 4: Simple Config Tweak](#part-4-simple-config-tweak)
    - [Part 5: Quick Challenge - Boot Observation](#part-5-quick-challenge---boot-observation)
    - [Part 6: Multi-VM Networking (Bridge Mode)](#part-6-multi-vm-networking-bridge-mode)
    - [Solutions](#solutions)
  - [Glossary of Key Terms](#glossary-of-key-terms)
  - [Completion Checklist](#completion-checklist)
  - [Troubleshooting](#troubleshooting)
  - [Sample Interview Questions](#sample-interview-questions)
  - [Interview Answers](#interview-answers)
  - [Resources](#resources)
  - [Reflection](#reflection)
  - [Share Your Learnings](#share-your-learnings)
  - [Next Steps](#next-steps)

![Free CKA Series (45)](https://github.com/user-attachments/assets/ace8e40c-8c73-4131-b198-577094e680e9)

## Learning Objectives
By the end of Day 2, you will:
- Understand basic virtualization concepts and hypervisor types
- Install and configure a Linux VM step-by-step in VirtualBox
- Play with your VM: Check network connectivity, take snapshots, and tweak settings
- Get a quick view of the Linux boot process
- Troubleshoot simple VM issues

**Estimated Time:** 1-2 hours

## Why Learn Virtualization?
Virtualization lets you create a "mini-computer" (VM) inside your real one—perfect for safely trying Linux without risking your main setup. Start here, and you're prepped for cloud magic.

### Why It Matters to You as a DevOps/SRE/Cloud Engineer
- **DevOps:** Test scripts in an isolated VM before deploying to real servers.
- **SRE:** Use snapshots to "undo" mistakes, like a time machine for troubleshooting.
- **Cloud Engineers:** Local VMs mimic cloud instances (e.g., AWS EC2) for free practice.
- **Quick Win:** VirtualBox is free and runs on any OS your portable Linux lab.

**Quick Fact:** Most cloud servers are VMs; mastering VirtualBox is like learning the alphabet before writing code.

## What is Virtualization?
Virtualization is the technology that creates **virtual versions of physical resources** (like servers, storage, or networks) on a single piece of hardware. It abstracts the underlying hardware, allowing multiple isolated environments—called **virtual machines (VMs)**—to run simultaneously without interfering.

### Key Components and How It Works
- **Host vs. Guest:** The host is your physical machine (e.g., your laptop). Guests are the VMs running on it (e.g., a Linux server VM).
- **Abstraction Layer:** The hypervisor (more on this below) emulates hardware for guests, allocating slices of CPU, RAM, disk, and network.
- **Types of Virtualization:**
  - **Server Virtualization:** Multiple OSes on one server (e.g., running Ubuntu and Windows VMs).
  - **Desktop Virtualization:** Remote access to VMs (e.g., VDI for secure desktops).
  - **Network/Storage Virtualization:** Pooling resources across devices.

#### Benefits (Why Interviewers Love This)
- **Efficiency:** One server runs 10+ VMs, cutting hardware costs by 70-80%.
- **Isolation:** A crash in one VM doesn't affect others—crucial for SRE reliability.
- **Scalability:** Spin up VMs on-demand (e.g., auto-scaling in AWS).
- **Testing/DevOps:** Reproducible environments; snapshot for "what if" scenarios.
- **Security:** Sandbox malware analysis or multi-tenant clouds.

In interviews, tie this to real-world: "Virtualization enables Kubernetes pods to run isolated on shared nodes, reducing overhead vs. bare metal."

#### Drawbacks (Show Balance)
- Overhead: 5-15% performance hit from emulation.
- Complexity: Managing hypervisors adds a layer (but tools like Kubernetes abstract it).

It's software (hypervisor) that tricks an OS into thinking it's on real hardware, so you can run Linux on Windows (or vice versa).

- **Hypervisors:** The "VM bosses."
  - **Type 1:** Hardware-direct (servers, e.g., VMware ESXi).
  - **Type 2:** On your OS (laptops, e.g., VirtualBox—we're using this!).

```mermaid
graph TD
    subgraph "Type 2 Hypervisor (VirtualBox)"
        A[Your Hardware] --> B[Your OS: Windows/macOS/Linux]
        B --> C[VirtualBox]
        C --> D[VM: Ubuntu Linux]
        C --> E[VM: Optional Windows Test]
    end
    style C fill:#3498db
```

***Analogy:** VirtualBox is your **personal hotel manager** —it books rooms (VMs) in your building (hardware) without you lifting a finger.

## Hypervisors: The Engine of Virtualization
A **hypervisor** (or Virtual Machine Monitor, VMM) is the software/firmware that creates, runs, and manages VMs. It's the "brain" allocating resources and enforcing isolation. As of 2025, hypervisors power 95%+ of cloud workloads.

### Type 1 vs. Type 2: The Big Divide
Hypervisors split into two camps based on where they run—interviewers often ask you to compare them.

| Aspect | Type 1 (Bare-Metal/Native) | Type 2 (Hosted) |
|--------|-----------------------------|-----------------|
| **Runs On** | Directly on hardware (no host OS). | On top of a host OS (e.g., Windows). |
| **Performance** | Near-native (1-5% overhead)—ideal for prod servers. | Higher overhead (5-20%)—fine for dev/testing. |
| **Security/Isolation** | Strongest; failures rarely affect hardware. | Depends on host OS; potential single point of failure. |
| **Use Cases** | Enterprise data centers, clouds (e.g., AWS Nitro). | Laptops for learning (e.g., VirtualBox for local labs). |
| **Examples (2025)** | VMware ESXi (vSphere 9.0 with AI optimizations), Microsoft Hyper-V (integrated in Azure), KVM (Linux kernel module, used in OpenStack), Citrix XenServer (now Citrix Hypervisor 8.3). | Oracle VirtualBox (7.0 with Wayland support), VMware Workstation 17 (Pro for teams), Parallels Desktop 20 (Apple Silicon focus). |
| **Pros** | Better scalability, efficiency for high-load (e.g., 1000+ VMs/node). | Easier setup, portable across OSes. |
| **Cons** | Harder to install (dedicated hardware); vendor lock-in risks. | Slower; host OS vulnerabilities expose VMs. |

**Interview Tip:** Say, "For prod SRE at scale, I'd pick Type 1 like KVM for cost/performance; for local dev, Type 2 VirtualBox for quick spins." Draw the table above on a whiteboard to impress.

### Emerging Trends in 2025
Merging Trends in 2025: Unikernels, GPU/ARM Hypervisors, and Open-Source Hybrids
Overview — why these three trends matter together

In 2025 the infrastructure landscape is shaped by two big forces:

Tighter specialization: workloads (microservices, edge functions, serverless) push OS/VM/runtime designs toward smaller, faster, more secure execution environments (unikernels, microVMs).

Heterogeneous compute & AI demand: AI/ML workloads require acceleration (GPUs, DPUs, specialized AI chips) and often run on ARM-based platforms at cloud scale, forcing hypervisor vendors and open-source stacks to add richer GPU/ARM support and GPU-sharing models.

Taken together, these forces drive more variety in “what a VM looks like” — from tiny unikernel images or Firecracker microVMs used for serverless, to full VMs with vGPUs orchestrated by platforms such as vSphere/VMware and KVM-based clouds. The rest of this note examines each trend, evidence, pros/cons, and how they interoperate.

**Unikernels** : tiny, purpose-built execution units (what & why)

What they are.
A unikernel is a single-purpose binary that combines application code and only the kernel/library components it needs, producing very small, specialized VMs that typically boot fast and have a small attack surface. MirageOS is one prominent project (OCaml-based) that builds unikernels for network services. 
mirage.io
+1

Why they’re attractive in 2025.

Footprint & boot time. Extremely compact images and near-instant start make them well suited for ephemeral microservices, cold-start sensitive serverless functions, and edge devices. (Research and surveys in 2025 continue to highlight the efficiency gains.) 
Fixstars Corporation Tech Blog
+1

Security. Eliminating unnecessary subsystems reduces attack surface (no shell, limited syscalls). MirageOS and contemporary surveys emphasize type-safety and smaller codebases as security benefits. 
Bobkonf

Deterministic resource usage. Because there’s no multipurpose OS with background tasks, resource consumption is easier to bound — useful at the edge and in real-time workloads. 
Fixstars Corporation Tech Blog

Where unikernels fit best

Highly specific networking services (DNS resolvers, small proxies, authentication validators).

Edge and constrained environments where minimal memory/boot latency matter.

Companies that can invest in tooling to build/test unikernels (language support and lib portability matter).

Limitations / adoption barriers

Ecosystem and tooling maturity. Containers and Linux have a huge ecosystem (packaging, observability, debugging). Unikernels still suffer tooling, debugging, and library porting gaps. (See state-of-play surveys.) 
Fixstars Corporation Tech Blog
+1

Compatibility & developer velocity. Rewriting or adapting apps to unikernel-friendly runtimes is non-trivial.

Operational complexity. Image build chains, debugging, and observability require reworking CI/CD and ops practices.

Practical hybrid approach (common in 2025)
Many organizations adopt unikernels selectively: for performance/security critical microservices at the edge while keeping mainstream app stacks in containers. The research/industry trend is toward selective unikernel adoption rather than full replacement. 
Fixstars Corporation Tech Blog

2) **GPU & ARM support in hypervisors: optimizing for AI workloads**

Context.
AI workloads are driving hypervisor evolution. Two important trends are: (a) better GPU integration (vGPU, passthrough, resource reservation, and orchestration for multi-tenant AI) and (b) wider ARM adoption (servers and cloud instances using Arm/Graviton families). Vendors and open stacks are adapting to both. 
NVIDIA Docs
+1

What vendors are doing (examples & capabilities):

vGPU & GPU orchestration in enterprise hypervisors. VMware and related stacks now surface features for reserving GPU slots, vGPU support for compute workloads, and deeper integrations in AI-focused releases. VMware’s Private AI/Foundation releases and vSphere updates include NVIDIA vGPU and AI-oriented features. These help guarantee GPU availability to latency-sensitive models and enable multi-tenant sharing of GPU resources. 
Broadcom TechDocs
+1

GPU virtualization models. There are several modes: full PCIe passthrough (dedicate entire GPU to a VM), vendor vGPU (time/memory sliced virtualization), and emerging disaggregated orchestration at rack scale. NVIDIA’s vGPU and NVIDIA AI Enterprise docs remain a key reference for deploying GPUs in virtualized environments. 
NVIDIA Docs
+1

ARM & heterogenous servers. Public clouds have accelerated ARM (Graviton) adoption; on-prem hypervisors and experimental arm ports (e.g., ESXi-ARM flings) demonstrate momentum for ARM in private/edge deployments. KVM-based clouds (and cloud-native orchestration) increasingly consider ARM-first instance types and tooling. 
ARM
+1

Why this matters for AI

Lower cost / better power efficiency. ARM-based servers (Graviton) often offer better perf/watt for certain workloads; heterogeneous setups let operators place parts of workloads on different accelerator types. 
Medium

Operational flexibility. vGPU and GPU orchestration let many AI teams share expensive GPUs, improving utilization while preserving isolation. VMware and other hypervisor vendors are expanding feature sets to meet enterprise AI needs. 
Broadcom TechDocs
+1

Caveats and practical concerns

Performance parity. Some vGPU or slicing modes may not match bare-metal performance (driver and scheduler behavior matters). Full passthrough still gives the best raw performance for large model training. Documentation and compatibility matrices (NVIDIA, VMware) are essential for production deployment choices. 
NVIDIA Docs
+1

Complex orchestration. Managing mixed fleets (x86, ARM, GPUs) increases scheduling complexity and tooling needs (node labelling, instance types, affinity rules).

3) **Open-source rise & container–hypervisor hybrids (KVM, Firecracker, Kata, gVisor)**

A short state of the landscape.
By 2025 KVM remains the dominant open-source hypervisor under the hood of many public clouds and virtualization platforms; large cloud providers and open-source projects continue to invest in KVM-based tooling and platforms (OpenShift Virtualization being one notable enterprise-level example of VM+container integration). 
Spectro Cloud
+1

Why KVM + open-source is gaining ground

Cloud-native integration. KVM integrates well into Linux-based cloud stacks and container ecosystems; projects such as OpenShift Virtualization bring VMs into Kubernetes control planes so teams can manage VMs and containers from a single platform. Adoption metrics for OpenShift Virtualization suggest strong growth. 
Red Hat

Community & ecosystem. KVM has broad vendor, distro, and cloud support; that makes it easier for cloud builders to standardize on open virtualization layers. 
Spectro Cloud

Container–hypervisor hybrids: what they are

MicroVMs & micro-hypervisors (Firecracker): tiny VM-like isolation units designed for serverless / fast-start functions. Firecracker, initially developed by AWS for Lambda and Fargate, is the archetype: microVMs provide stronger isolation than containers while keeping low overhead and fast startup times. 
firecracker-microvm.github.io
+1

Kata Containers / gVisor: offer different trade-offs: Kata uses lightweight VMs to run containers (stronger isolation, near-VM semantics); gVisor implements a user-space kernel for container isolation focusing on compatibility with existing container workflows. Comparison pieces in 2025 discuss tradeoffs between Firecracker, Kata, and gVisor for security, speed, and compatibility. 
Onidel Cloud
+1

Why container-hypervisor hybrids are popular now

Security & multitenancy. MicroVMs and VM-backed containers give stronger isolation for untrusted workloads (multi-tenant serverless, FaaS, managed runtimes).

Performance trade-offs. Firecracker’s microVM design provides acceptable cold-start performance with better isolation than plain containers, making it attractive for serverless platforms and edge compute that require multi-tenant security. 
firecracker-microvm.github.io
+1

How the three trends interact (practical convergence)

Unikernels + microVMs: unikernels can be packaged as minimal VM images (or microVMs) to get both the tiny binary/boot benefits of unikernels and the isolation/management of microVMs like Firecracker. This is an attractive stack for secure edge functions: unikernel binary + microVM runtime. (Research and community experiments show this as a logical combination.) 
Fixstars Corporation Tech Blog
+1

GPU/ARM in a mixed estate: organizations will run some workloads on KVM or VMware with vGPU support for heavy AI training, while using Firecracker or unikernels for low-latency inference or edge functions. Orchestration layers (Kubernetes/OpenShift) will increasingly need to reason about device topology (GPUs, DPUs, ARM vs x86) when scheduling. 
NVIDIA Docs
+1

Open-source ecosystems enable experimentation: KVM + Firecracker + Kata ecosystems allow developers to pick the isolation/performance profile they need, and OpenShift-like platforms make it possible to manage VMs and containers in a unified control plane. 
Spectro Cloud
+1

Real-world implications & adoption advice (for architects/engineers)

When to use unikernels

Use them for small, critical network/edge functions where boot time, small memory, and a minimized attack surface are decisive.

Prototype with MirageOS (or other unikernel toolchains) for targeted services, not as a wholesale container replacement. 
mirage.io
+1

When to pick Firecracker / microVMs / Kata

Choose Firecracker for serverless or multi-tenant function hosting where isolation matters but you still need high density and fast startup. Firecracker is battle-tested in serverless contexts (AWS). 
firecracker-microvm.github.io
+1

Consider Kata when you need full VM-level isolation for container workloads with compatibility for standard container tooling (but with VM security characteristics). 
Onidel Cloud

When you need full hypervisor features (vSphere / KVM + vGPU)

For heavy, GPU-bound AI training or production inference that requires predictable performance or vendor-certified stacks (NVIDIA vGPU), a full hypervisor with vGPU and enterprise support may be the right choice. Check vendor compatibility matrices and vGPU docs. 
NVIDIA Docs
+1

Operational note

Mixed-fleet scheduling (ARM + x86 + GPUs) is complex: plan for node labelling, affinity rules, multi-architecture CI pipelines, and image/build pipelines for each architecture. Public cloud providers already offer ARM-first instances; on-prem experimentation (ESXi-Arm flings, KVM on ARM hardware) demonstrates feasibility, but production readiness varies by vendor. 
WilliamLam.com
+1

Challenges, risks & gaps to watch

Tooling & debugging for unikernels. Expect continued friction: fewer off-the-shelf libraries, unique debugging traces, and bespoke CI. Research and community progress is closing gaps but not eliminating them yet. 
Fixstars Corporation Tech Blog

GPU virtualization complexity. vGPU behavior, drivers, and performance differences can surprise you: always validate with workload-representative benchmarks and consult vendor compatibility matrices. 
NVIDIA Docs

Portability & fragmentation. More runtime types (unikernel, microVM, VM, container) mean more build/test permutations and potential fragmentation unless platforms provide strong abstractions. 
Medium

## Quick Peek: The Linux Boot Process
When your VM starts, it "wakes up" in steps—watch it to feel the flow.

The Linux boot is a choreographed sequence turning hardware into a usable OS. It's interview gold—expect "Walk me through it" or "Debug a hang at stage X." As of 2025, systemd dominates (95% distros), but the core flow is timeless.

### Detailed Step-by-Step
<img width="1080" height="1080" alt="Blue White Colorful Townhall Meeting Instagram Post (7)" src="https://github.com/user-attachments/assets/2b22042a-500a-4ba9-b306-48788e2d2f75" />

1. **Power-On Self-Test (POST) & Firmware (BIOS/UEFI):** 
   - Hardware powers up; firmware (BIOS legacy or UEFI modern) tests components (CPU, RAM, disks). In VMs, hypervisor emulates this (~1-2s).
   - Locates boot device (e.g., /dev/sda in VM disk). UEFI uses GPT partitions; BIOS MBR.

2. **Bootloader Stage (GRUB2):**
   - GRUB (GNU GRand Unified Bootloader) loads from boot sector. Scans /boot/grub/grub.cfg for kernels (vmlinuz-*).
   - Shows menu (hold Shift); user selects entry. Passes params (e.g., root=/dev/sda1) to kernel.
   - Chains to other OSes if dual-boot. Time: <5s.

3. **Kernel Initialization:**
   - Kernel (bzImage) decompresses into RAM. Mounts initramfs (compressed FS with early drivers).
   - Probes hardware (via modules like virtio for VMs), sets up memory (paging), mounts real root FS (/).
   - Starts PID 1 (init). Logs to dmesg. Time: 5-20s.

4. **Init System (systemd):**
   - systemd reads /etc/fstab for mounts; parses units in /lib/systemd/system.
   - Reaches default target (multi-user.target for servers; graphical.target for desktops).
   - Starts services parallel (e.g., NetworkManager, sshd). Time: 10-60s.

5. **User Space & Login:**
   - getty spawns on tty/SSH; PAM authenticates user.
   - Shell (bash) loads ~/.profile; prompt appears. GUI: display manager (gdm) starts X11/Wayland.

**Total Time:** 30-90s on SSD; slower on HDD. In 2025, dracut optimizes initramfs for faster embedded boots.

**VM Nuances:** Hypervisor provides virtual BIOS (SeaBIOS) or UEFI (OVMF); boot faster sans real hardware checks.

**Debug Tips:** `journalctl -b` (systemd logs), `dmesg` (kernel), `systemd-analyze blame` (service timings)—interview gold for "slow boot?" scenarios.

Run `systemd-analyze` after boot to see timings—fun metric!

## Step-by-Step: Installing Your First VM in VirtualBox
Let's build an Ubuntu VM—follow along, pause if needed. We'll use Ubuntu 25.04 (Plucky Puffin) and username "linuxthefinalboss".

### Prerequisites
- Download: VirtualBox from virtualbox.org (install + Extension Pack).
- ISO: Visit https://ubuntu.com/download/desktop and download Ubuntu 25.04 Desktop (5.8 GB ISO for x86_64; requires 4 GB RAM, 25 GB disk min—adjust VM accordingly).

### Step 1: Launch VirtualBox & Create VM
1. Open VirtualBox → Click "New."
2. Name: "MyUbuntuLab" | Folder: Default | ISO Image: Select your Ubuntu 25.04 ISO | Type: Linux | Version: Ubuntu (64-bit) → Next.
3. Hardware: Base Memory: 4096 MB (4GB to match prereqs) → Next.
4. Processors: 2 CPUs → Next.
5. Hard Disk: Create new → VDI → Dynamically allocated → 30 GB (above min) → Create.

**Your VM is born!** (Takes ~2 min.)

### Step 2: Configure VM Settings
1. Select your VM → Settings.
2. **System:** Motherboard: Enable EFI (modern boot); Processor: 2 CPUs.
3. **Display:** Screen: 128 MB Video Memory; Enable 3D Acceleration (smoother GUI).
4. **Storage:** Under Controller: IDE → Empty → Optical Drive icon → Choose your Ubuntu 25.04 ISO.
5. **Network:** Adapter 1: Enable → Attached to: NAT (easy internet).
6. **USB:** Enable USB Controller.
7. OK → Start the VM.

### Step 3: Install Ubuntu in the VM
1. VM boots to ISO → "Try or Install Ubuntu" → Install.
2. Keyboard: English → Continue.
3. Updates: Normal → Continue.
4. Type: Erase disk & install → Continue (VM disk only!).
5. Location: Your region → Continue.
6. Who: Name "linuxthefinalboss", computer "lab-vm", username "linuxthefinalboss", password (simple for now) → Continue.
7. Wait ~10-15 min for install → Restart (remove ISO when prompted: Devices → Optical Drives → Remove).

**Success!** Log in as "linuxthefinalboss"—explore the desktop.

### Step 4: First Tweaks in Your VM
1. Open Terminal (Ctrl+Alt+T).
2. Update: `sudo apt update && sudo apt upgrade -y`.
3. Install basics: `sudo apt install curl htop -y`.
4. Reboot: `sudo reboot`—watch the boot flow.

**Pro Tip:** Install Guest Additions for clipboard sharing: Devices → Insert Guest Additions CD → Run in terminal: `sudo sh ./VBoxLinuxAdditions.run`.

## Playing with Your VM: Networking, Snapshots, & More
Now that it's running, let's experiment—like a playground.

### Check Network Connectivity
1. In VM Terminal: `ping google.com` (tests internet—should reply).
2. If fails: VM Settings → Network → Ensure NAT enabled → Restart adapter (right-click in Network menu).
3. Fun Test: `curl ifconfig.me` (shows VM's public IP via host).

**Question:** Why NAT? (Hides VM behind your IP—secure & simple.)

### Take & Use Snapshots
1. VM running? → Machine → Take Snapshot → Name: "Fresh Ubuntu" → Take.
2. Make a change: Create file `touch ~/experiment.txt` → ls ~ (see it).
3. Take another: "With File" → OK.
4. "Oops!" → Snapshots pane → Right-click "Fresh Ubuntu" → Restore.
5. Reboot/refresh—file gone!

**Why Cool?** Undo button for experiments—SREs use this for "before/after" deploys.

### Quick Tweaks & Exploration
- **Resize Window:** View → Auto-resize Guest Display (full-screen magic).
- **Shared Folders:** Settings → Shared Folders → Add host folder → Access in VM: `sudo mount -t vboxsf shared /mnt/shared`.
- **Boot Peek:** Reboot → Hold Shift for GRUB menu → Select Advanced → Recovery (safe mode fun).

## Hands-on Exercises & Lab
Step-by-step playtime—build confidence one tweak at a time.

### Part 1: VM Creation & First Boot
1. Follow Steps 1-3 above—get Ubuntu 25.04 installed & logged in as linuxthefinalboss.
2. **Exercise:** Run `neofetch` (install if needed: `sudo apt install neofetch`)—screenshot your system info.
3. **Question:** What kernel version shows? (Compare to Day 1's `uname -r`.)

### Part 2: Network Check & Fix
1. Ping test: `ping 8.8.8.8` (IP) & `ping google.com` (DNS).
2. **Exercise:** If DNS fails, edit /etc/resolv.conf (add `nameserver 8.8.8.8`) → Test again.
3. **Question:** How does VM networking differ from your host?

### Part 3: Snapshot Practice
1. Take "Baseline" snapshot.
2. **Exercise:** Install a fun tool (`sudo apt install cowsay -y; cowsay "Hello VM!"`) → Take "With Cow" snapshot.
3. Restore to Baseline—cow gone? Reinstall to confirm.
4. **Question:** Imagine a bad config change—how does snapshot save you?

### Part 4: Simple Config Tweak
1. **Exercise:** Change hostname: `sudo hostnamectl set-hostname my-lab-server` → Reboot → `hostname` confirms.
2. Add to snapshot chain: "Renamed Host."
3. **Question:** Why tweak hostname in a VM (e.g., for multi-VM testing)?

### Part 5: Quick Challenge - Boot Observation
- Reboot VM; time the boot (`time sleep 1` post-login for fun).
- **Exercise:** Run `journalctl -b -p err` (boot errors? Usually none!).
- **Question:** What service starts last (hint: `systemd-analyze blame`)?

### Part 6: Multi-VM Networking (Bridge Mode)
1. **Create Second VM:** Repeat Part 1 steps for a second Ubuntu VM ("VM2-Lab").
2. **Switch to Bridge:** For both VMs: Settings → Network → Adapter 1 → Attached to: Bridged Adapter → Name: Your WiFi/Ethernet interface (e.g., en0).
3. **Start Both:** Boot VM1 & VM2—note their IPs (`ip addr show` or `ifconfig`).
4. **Test Access:** From VM1: `ping <VM2-IP>` (should reply). From host terminal: `ping <VM1-IP>` (bridge exposes to network).
5. **Exercise:** Install netcat (`sudo apt install netcat -y`); in VM1: `nc -l 1234`; in VM2: `nc <VM1-IP> 1234` → Type message (transmits!).
6. **Question:** Why bridge over NAT for multi-VM? (Direct comms, like a LAN party.)

### Solutions
1. **First Boot:** Kernel like 6.14—matches Ubuntu 25.04.
2. **Network:** VM uses host's connection; DNS via resolv.conf.
3. **Snapshot:** Instant rollback—no data loss.
4. **Tweak:** Hostnames avoid confusion in teams/clusters.
5. **Boot:** Login managers last; blame shows timings.
6. **Multi-VM:** Bridge gives real IPs for peer-to-peer testing; NAT isolates (no direct VM-VM pings).

## Glossary of Key Terms
- **Hypervisor:** VM runner (VirtualBox = Type 2).
- **VM:** Your virtual Linux box.
- **Snapshot:** Save/restore point.
- **NAT:** Easy network mode.
- **GRUB:** Boot chooser.
- **systemd:** Service manager.

## Completion Checklist
- [ ] Installed VirtualBox & created Ubuntu 25.04 VM
- [ ] Booted, updated, and explored as linuxthefinalboss
- [ ] Tested network connectivity
- [ ] Took/restored snapshots
- [ ] Tweaked a simple setting
- [ ] Created multiple VMs and tested bridge networking

## Troubleshooting
- **VM Black Screen:** Increase video memory (Settings → Display).
- **No Internet:** NAT on; host online? Restart VM.
- **Slow GUI:** Enable 3D accel; use Server ISO for CLI-only.
- **Snapshot Error:** VM off; enough host disk space.
- **Install Stuck:** Check ISO download (re-download if corrupt).
- **Bridge No Ping:** Ensure adapter selected correctly; firewall off (`sudo ufw disable`).
  
## Sample Interview Questions
1. What's VirtualBox, and why use it for learning?
2. Step-by-step: How do you create a VM?
3. Why snapshots in virtualization?
4. Basic network check in a VM?
5. Quick boot overview?

## Interview Answers
1. **VirtualBox:** Free Type 2 hypervisor—easy local VMs for testing.
2. **Create VM:** New → ISO → RAM/Disk → Settings (Network/Storage) → Install.
3. **Snapshots:** Rollback changes safely.
4. **Network:** Ping IP/DNS; NAT for quick connect.
5. **Boot:** BIOS → GRUB → Kernel → Services → Login.

## Resources
- VirtualBox.org tutorials; ubuntu.com/download/desktop (Ubuntu 25.04).
- YouTube: @Sagar.Utekar VM guides.
- Discord: discord.gg/mNDm39qB8t; Google Group: groups.google.com/forum/#!forum/daily-devops-sre-challenge-series/join.

## Reflection
- What surprised you about VM setup?
- Ready to "play" more tomorrow?

## Share Your Learnings
Share your VM desktop pic with #LinuxFinalBoss! Tag @Sagar.Utekar.

## Next Steps
Proceed to [Day 3: Linux Folder Structure & File Types](../Day_03/notes_and_exercises.md) to explore the Linux filesystem.
