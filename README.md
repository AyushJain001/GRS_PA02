# MT25066
# PA02: Analysis of Network I/O Primitives using perf

## Overview
This project implements and compares three TCP socket communication strategies:
- **A1: Two-copy** - Standard `send()`/`recv()` system calls
- **A2: One-copy** - `sendmsg()` with scatter/gather iovec buffers
- **A3: Zero-copy** - `sendmsg()` with `MSG_ZEROCOPY` flag

## Files Structure
```
MT25066_Part_A1_Server.c / Client.c  - Two-copy implementation
MT25066_Part_A2_Server.c / Client.c  - One-copy implementation  
MT25066_Part_A3_Server.c / Client.c  - Zero-copy implementation
MT25066_Part_A_Common.h / .c         - Shared message structure and helpers
MT25066_Part_C_Experiment.sh         - Automated experiment runner
MT25066_Part_D_Plots.py              - Plot generation (hardcoded data)
MT25066_Part_E_Report.md             - Analysis report
setup_namespaces.sh                  - Network namespace setup script
Makefile                             - Build configuration
```

## Build
```bash
make
```

## Clean
```bash
make clean
```

## Network Namespace Setup (Required)
The experiments run on separate network namespaces as required by the assignment.

```bash
# Setup namespaces (creates server_ns @ 10.0.0.1, client_ns @ 10.0.0.2)
sudo ./setup_namespaces.sh setup

# Check status
sudo ./setup_namespaces.sh status

# Cleanup after experiments
sudo ./setup_namespaces.sh cleanup
```

## Run Automated Experiments
```bash
sudo ./MT25066_Part_C_Experiment.sh
```
This runs 48 experiments (3 implementations × 4 message sizes × 4 thread counts) and generates:
- 48 individual CSV files: `MT25066_Part_C_{impl}_{msgsize}_{threads}.csv`
- 1 summary CSV: `MT25066_Part_C_Summary.csv`

## Generate Plots
```bash
python3 MT25066_Part_D_Plots.py
```
Generates 6 PNG plots from hardcoded experimental data.

## Manual Testing
**Server (in server namespace):**
```bash
sudo ip netns exec server_ns ./MT25066_Part_A1_Server <port> <msg_size>
```

**Client (in client namespace):**
```bash
sudo ip netns exec client_ns ./MT25066_Part_A1_Client 10.0.0.1 <port> <msg_size> <threads> <duration_sec>
```

### Example:
```bash
# Terminal 1 - Server
sudo ip netns exec server_ns ./MT25066_Part_A1_Server 5001 1024

# Terminal 2 - Client  
sudo ip netns exec client_ns ./MT25066_Part_A1_Client 10.0.0.1 5001 1024 4 5
```

## Parameters
- **Message sizes**: 64, 256, 1024, 4096 bytes
- **Thread counts**: 1, 2, 4, 8
- **Duration**: 3 seconds per experiment
- **Messages**: 1,000,000 per experiment

## Message Structure
Each message contains 8 dynamically allocated fields. The message size parameter is divided equally among all 8 fields (e.g., 1024 bytes → 128 bytes per field).

## Profiling Metrics (via perf)
- CPU cycles
- L1 data cache misses
- LLC (Last Level Cache) misses
- Context switches

## Quick Demo Commands
```bash
cd /home/iiitd/Desktop/PA_02/GRS_PA02
sudo ./setup_namespaces.sh setup
sudo ./MT25066_Part_C_Experiment.sh
python3 MT25066_Part_D_Plots.py
sudo ./setup_namespaces.sh cleanup
```

sudo ./setup_namespaces.sh setup && sudo ./MT25066_Part_C_Experiment.sh && python3 MT25066_Part_D_Plots.py

## Author
- **Roll Number**: MT25066
- **Course**: Graduate Systems (GRS)
- **Assignment**: PA02

## GitHub Repository
https://github.com/[YOUR_USERNAME]/GRS_PA02
