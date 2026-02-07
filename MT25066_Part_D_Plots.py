# MT25066
# Hardcoded experimental data from MT25066_Part_C_Summary.csv
# DO NOT modify - these values are from actual experiments

import matplotlib.pyplot as plt
import numpy as np

SYSTEM_INFO = "Ubuntu 24.04 | Intel (Dual E-core/P-core) | Network Namespaces"

# ============================================================================
# HARDCODED EXPERIMENTAL DATA (from CSV)
# Format: data[impl][msg_size][threads] = value
# Message sizes: 64, 256, 1024, 4096 bytes
# Thread counts: 1, 2, 4, 8
# ============================================================================

# Throughput (Gbps)
THROUGHPUT = {
    'A1': {
        64:   {1: 0.076512, 2: 0.149765, 4: 0.279624, 8: 0.421397},
        256:  {1: 0.313363, 2: 0.518509, 4: 0.858253, 8: 1.213421},
        1024: {1: 1.102493, 2: 1.969955, 4: 3.199413, 8: 4.964732},
        4096: {1: 4.180957, 2: 7.912216, 4: 11.549147, 8: 18.824091},
    },
    'A2': {
        64:   {1: 0.077140, 2: 0.147145, 4: 0.269664, 8: 0.404766},
        256:  {1: 0.298153, 2: 0.529199, 4: 0.821832, 8: 1.150880},
        1024: {1: 1.119344, 2: 1.958527, 4: 3.154346, 8: 5.084193},
        4096: {1: 4.049338, 2: 7.607299, 4: 12.017162, 8: 18.851234},
    },
    'A3': {
        64:   {1: 0.066025, 2: 0.128925, 4: 0.228326, 8: 0.269525},
        256:  {1: 0.258133, 2: 0.453857, 4: 0.708057, 8: 1.040414},
        1024: {1: 0.967934, 2: 1.734383, 4: 2.745186, 8: 4.241239},
        4096: {1: 3.919599, 2: 6.775767, 4: 10.711051, 8: 16.387320},
    },
}

# Average Latency (microseconds)
LATENCY = {
    'A1': {
        64:   {1: 6.668, 2: 6.809, 4: 7.283, 8: 9.666},
        256:  {1: 6.511, 2: 7.871, 4: 9.491, 8: 13.427},
        1024: {1: 7.405, 2: 8.287, 4: 10.186, 8: 13.129},
        4096: {1: 7.812, 2: 8.254, 4: 11.290, 8: 13.854},
    },
    'A2': {
        64:   {1: 6.613, 2: 6.934, 4: 7.551, 8: 10.063},
        256:  {1: 6.845, 2: 7.712, 4: 9.912, 8: 14.159},
        1024: {1: 7.294, 2: 8.334, 4: 10.332, 8: 12.819},
        4096: {1: 8.066, 2: 8.585, 4: 10.851, 8: 13.835},
    },
    'A3': {
        64:   {1: 7.731, 2: 7.917, 4: 8.925, 8: 15.127},
        256:  {1: 7.910, 2: 8.996, 4: 11.515, 8: 15.675},
        1024: {1: 8.438, 2: 9.416, 4: 11.882, 8: 15.380},
        4096: {1: 8.335, 2: 9.643, 4: 12.184, 8: 15.923},
    },
}

# CPU Cycles
CYCLES = {
    'A1': {
        64:   {1: 5969284529, 2: 12105165925, 4: 24747459378, 8: 47172926564},
        256:  {1: 6056496887, 2: 10852227644, 4: 19270539752, 8: 33559877399},
        1024: {1: 5701131473, 2: 10678931369, 4: 18983523701, 8: 36128072909},
        4096: {1: 7375784236, 2: 14179448511, 4: 23988024998, 8: 44893103814},
    },
    'A2': {
        64:   {1: 6163132962, 2: 11905751370, 4: 23377008438, 8: 43772732446},
        256:  {1: 6022696047, 2: 10747366999, 4: 18869544979, 8: 32648922859},
        1024: {1: 5483215659, 2: 10575674904, 4: 19166768156, 8: 34873761110},
        4096: {1: 7260063227, 2: 14048236363, 4: 24714250137, 8: 45149652833},
    },
    'A3': {
        64:   {1: 5872137432, 2: 12295995668, 4: 23286031848, 8: 35863382485},
        256:  {1: 5896509605, 2: 10816342348, 4: 18462259042, 8: 34076345164},
        1024: {1: 5813816044, 2: 11053478917, 4: 20011326868, 8: 36129260231},
        4096: {1: 6831976554, 2: 13115099988, 4: 22946374011, 8: 42838808105},
    },
}

# L1 Data Cache Misses
L1_MISSES = {
    'A1': {
        64:   {1: 95790117, 2: 187832134, 4: 351236218, 8: 656536113},
        256:  {1: 95678404, 2: 169021439, 4: 278494289, 8: 515284237},
        1024: {1: 111110785, 2: 181073586, 4: 336682034, 8: 607046117},
        4096: {1: 190998009, 2: 349277805, 4: 556703336, 8: 1041250902},
    },
    'A2': {
        64:   {1: 91681735, 2: 187834218, 4: 344167428, 8: 673563238},
        256:  {1: 94212463, 2: 165837919, 4: 282687636, 8: 512187813},
        1024: {1: 119673456, 2: 198893324, 4: 321871944, 8: 646809563},
        4096: {1: 191035851, 2: 345673257, 4: 559162192, 8: 1037553119},
    },
    'A3': {
        64:   {1: 109522240, 2: 200960747, 4: 392772273, 8: 553633259},
        256:  {1: 116676196, 2: 190118201, 4: 316393673, 8: 575101910},
        1024: {1: 120672867, 2: 217463350, 4: 355790570, 8: 655456695},
        4096: {1: 195281418, 2: 352381801, 4: 583715561, 8: 1028588811},
    },
}

# LLC (Last Level Cache) Misses
LLC_MISSES = {
    'A1': {
        64:   {1: 8595, 2: 3087, 4: 6242, 8: 13563},
        256:  {1: 1725, 2: 4224, 4: 7078, 8: 68693},
        1024: {1: 11616, 2: 9998, 4: 11536, 8: 22813},
        4096: {1: 10671, 2: 10052, 4: 80352, 8: 34135},
    },
    'A2': {
        64:   {1: 3149, 2: 1995, 4: 3841, 8: 18375},
        256:  {1: 2782, 2: 2089, 4: 7773, 8: 79426},
        1024: {1: 10363, 2: 13775, 4: 12493, 8: 27834},
        4096: {1: 8411, 2: 12171, 4: 14761, 8: 33210},
    },
    'A3': {
        64:   {1: 3624, 2: 3259, 4: 12082, 8: 10105},
        256:  {1: 3976, 2: 3694, 4: 7600, 8: 21307},
        1024: {1: 9551, 2: 9869, 4: 12153, 8: 31738},
        4096: {1: 7313, 2: 8969, 4: 15363, 8: 43284},
    },
}

# Context Switches
CONTEXT_SWITCHES = {
    'A1': {
        64:   {1: 448293, 2: 877573, 4: 1638546, 8: 2470384},
        256:  {1: 459016, 2: 759601, 4: 1257351, 8: 1779364},
        1024: {1: 403741, 2: 721472, 4: 1171948, 8: 1819634},
        4096: {1: 382801, 2: 724362, 4: 1057999, 8: 1725089},
    },
    'A2': {
        64:   {1: 451974, 2: 862214, 4: 1580156, 8: 2372981},
        256:  {1: 436748, 2: 775338, 4: 1204062, 8: 1688427},
        1024: {1: 409882, 2: 717292, 4: 1155347, 8: 1863703},
        4096: {1: 370786, 2: 696363, 4: 1100522, 8: 1727674},
    },
    'A3': {
        64:   {1: 386867, 2: 755485, 4: 1337972, 8: 1580167},
        256:  {1: 378122, 2: 664995, 4: 1037349, 8: 1525439},
        1024: {1: 354673, 2: 635198, 4: 1005531, 8: 1554582},
        4096: {1: 358805, 2: 620356, 4: 980892, 8: 1502063},
    },
}

# Constants
MSG_SIZES = [64, 256, 1024, 4096]
THREAD_COUNTS = [1, 2, 4, 8]
IMPLS = ['A1', 'A2', 'A3']

# ============================================================================
# PLOT FUNCTIONS
# ============================================================================

def plot_throughput_vs_msg_size():
    """Plot 1: Throughput vs Message Size (2x2 grid for all thread counts)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, threads in enumerate(THREAD_COUNTS):
        tp_a1 = [THROUGHPUT['A1'][sz][threads] for sz in MSG_SIZES]
        tp_a2 = [THROUGHPUT['A2'][sz][threads] for sz in MSG_SIZES]
        tp_a3 = [THROUGHPUT['A3'][sz][threads] for sz in MSG_SIZES]
        
        axes[idx].plot(MSG_SIZES, tp_a1, marker='o', linewidth=2, markersize=8, label='A1: Two-copy')
        axes[idx].plot(MSG_SIZES, tp_a2, marker='s', linewidth=2, markersize=8, label='A2: One-copy')
        axes[idx].plot(MSG_SIZES, tp_a3, marker='^', linewidth=2, markersize=8, label='A3: Zero-copy')
        axes[idx].set_title(f'Thread Count: {threads}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Message size (bytes)', fontsize=11)
        axes[idx].set_ylabel('Throughput (Gbps)', fontsize=11)
        axes[idx].legend(fontsize=9, loc='best')
        axes[idx].grid(True, linestyle='--', alpha=0.5)
        axes[idx].set_xscale('log')
    
    fig.suptitle(f'Throughput vs Message Size\n{SYSTEM_INFO}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plot1_throughput_vs_msg.png', dpi=150)
    plt.close()
    print("✓ Plot 1 saved: plot1_throughput_vs_msg.png")

def plot_latency_vs_thread_count():
    """Plot 2: Latency vs Thread Count (2x2 grid for all message sizes)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, msg_size in enumerate(MSG_SIZES):
        lat_a1 = [LATENCY['A1'][msg_size][t] for t in THREAD_COUNTS]
        lat_a2 = [LATENCY['A2'][msg_size][t] for t in THREAD_COUNTS]
        lat_a3 = [LATENCY['A3'][msg_size][t] for t in THREAD_COUNTS]
        
        axes[idx].plot(THREAD_COUNTS, lat_a1, marker='o', linewidth=2, markersize=8, label='A1: Two-copy')
        axes[idx].plot(THREAD_COUNTS, lat_a2, marker='s', linewidth=2, markersize=8, label='A2: One-copy')
        axes[idx].plot(THREAD_COUNTS, lat_a3, marker='^', linewidth=2, markersize=8, label='A3: Zero-copy')
        axes[idx].set_title(f'Message Size: {msg_size} bytes', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Thread count', fontsize=11)
        axes[idx].set_ylabel('Average latency (µs)', fontsize=11)
        axes[idx].legend(fontsize=9, loc='best')
        axes[idx].grid(True, linestyle='--', alpha=0.5)
        axes[idx].set_xticks(THREAD_COUNTS)
    
    fig.suptitle(f'Latency vs Thread Count\n{SYSTEM_INFO}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plot2_latency_vs_threads.png', dpi=150)
    plt.close()
    print("✓ Plot 2 saved: plot2_latency_vs_threads.png")

def plot_throughput_scaling():
    """Plot 3: Throughput Scaling vs Thread Count (2x2 grid for all message sizes)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, msg_size in enumerate(MSG_SIZES):
        tp_a1 = [THROUGHPUT['A1'][msg_size][t] for t in THREAD_COUNTS]
        tp_a2 = [THROUGHPUT['A2'][msg_size][t] for t in THREAD_COUNTS]
        tp_a3 = [THROUGHPUT['A3'][msg_size][t] for t in THREAD_COUNTS]
        
        axes[idx].plot(THREAD_COUNTS, tp_a1, marker='o', linewidth=2, markersize=8, label='A1: Two-copy')
        axes[idx].plot(THREAD_COUNTS, tp_a2, marker='s', linewidth=2, markersize=8, label='A2: One-copy')
        axes[idx].plot(THREAD_COUNTS, tp_a3, marker='^', linewidth=2, markersize=8, label='A3: Zero-copy')
        axes[idx].set_title(f'Message Size: {msg_size} bytes', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Thread count', fontsize=11)
        axes[idx].set_ylabel('Throughput (Gbps)', fontsize=11)
        axes[idx].legend(fontsize=9, loc='best')
        axes[idx].grid(True, linestyle='--', alpha=0.5)
        axes[idx].set_xticks(THREAD_COUNTS)
    
    fig.suptitle(f'Throughput Scaling vs Thread Count\n{SYSTEM_INFO}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plot3_throughput_scaling.png', dpi=150)
    plt.close()
    print("✓ Plot 3 saved: plot3_throughput_scaling.png")

def plot_implementation_comparison():
    """Plot 4: Implementation Comparison Bar Chart (2x2 grid for all message sizes)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    x = np.arange(len(THREAD_COUNTS))
    width = 0.25
    
    for idx, msg_size in enumerate(MSG_SIZES):
        tp_a1 = [THROUGHPUT['A1'][msg_size][t] for t in THREAD_COUNTS]
        tp_a2 = [THROUGHPUT['A2'][msg_size][t] for t in THREAD_COUNTS]
        tp_a3 = [THROUGHPUT['A3'][msg_size][t] for t in THREAD_COUNTS]
        
        axes[idx].bar(x - width, tp_a1, width, label='A1: Two-copy', color='steelblue')
        axes[idx].bar(x, tp_a2, width, label='A2: One-copy', color='darkorange')
        axes[idx].bar(x + width, tp_a3, width, label='A3: Zero-copy', color='forestgreen')
        axes[idx].set_title(f'Message Size: {msg_size} bytes', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Thread count', fontsize=11)
        axes[idx].set_ylabel('Throughput (Gbps)', fontsize=11)
        axes[idx].set_xticks(x)
        axes[idx].set_xticklabels(THREAD_COUNTS)
        axes[idx].legend(fontsize=9, loc='best')
        axes[idx].grid(True, linestyle='--', alpha=0.5, axis='y')
    
    fig.suptitle(f'Implementation Comparison\n{SYSTEM_INFO}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plot4_comparison.png', dpi=150)
    plt.close()
    print("✓ Plot 4 saved: plot4_comparison.png")

def plot_cache_misses():
    """Plot 5: Cache Misses vs Message Size (2x2 grid for L1 and LLC)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Top row: L1 cache misses
    for idx, threads in enumerate([1, 8]):
        l1_a1 = [L1_MISSES['A1'][sz][threads] / 1e6 for sz in MSG_SIZES]
        l1_a2 = [L1_MISSES['A2'][sz][threads] / 1e6 for sz in MSG_SIZES]
        l1_a3 = [L1_MISSES['A3'][sz][threads] / 1e6 for sz in MSG_SIZES]
        
        axes[0, idx].plot(MSG_SIZES, l1_a1, marker='o', linewidth=2, markersize=8, label='A1: Two-copy')
        axes[0, idx].plot(MSG_SIZES, l1_a2, marker='s', linewidth=2, markersize=8, label='A2: One-copy')
        axes[0, idx].plot(MSG_SIZES, l1_a3, marker='^', linewidth=2, markersize=8, label='A3: Zero-copy')
        axes[0, idx].set_title(f'L1 Cache Misses ({threads} thread{"s" if threads > 1 else ""})', fontsize=12, fontweight='bold')
        axes[0, idx].set_xlabel('Message size (bytes)', fontsize=11)
        axes[0, idx].set_ylabel('L1 Cache Misses (millions)', fontsize=11)
        axes[0, idx].legend(fontsize=9, loc='best')
        axes[0, idx].grid(True, linestyle='--', alpha=0.5)
        axes[0, idx].set_xscale('log')
    
    # Bottom row: LLC misses
    for idx, threads in enumerate([1, 8]):
        llc_a1 = [LLC_MISSES['A1'][sz][threads] / 1e3 for sz in MSG_SIZES]
        llc_a2 = [LLC_MISSES['A2'][sz][threads] / 1e3 for sz in MSG_SIZES]
        llc_a3 = [LLC_MISSES['A3'][sz][threads] / 1e3 for sz in MSG_SIZES]
        
        axes[1, idx].plot(MSG_SIZES, llc_a1, marker='o', linewidth=2, markersize=8, label='A1: Two-copy')
        axes[1, idx].plot(MSG_SIZES, llc_a2, marker='s', linewidth=2, markersize=8, label='A2: One-copy')
        axes[1, idx].plot(MSG_SIZES, llc_a3, marker='^', linewidth=2, markersize=8, label='A3: Zero-copy')
        axes[1, idx].set_title(f'LLC Misses ({threads} thread{"s" if threads > 1 else ""})', fontsize=12, fontweight='bold')
        axes[1, idx].set_xlabel('Message size (bytes)', fontsize=11)
        axes[1, idx].set_ylabel('LLC Misses (thousands)', fontsize=11)
        axes[1, idx].legend(fontsize=9, loc='best')
        axes[1, idx].grid(True, linestyle='--', alpha=0.5)
        axes[1, idx].set_xscale('log')
    
    fig.suptitle(f'Cache Misses vs Message Size\n{SYSTEM_INFO}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plot5_cache_misses.png', dpi=150)
    plt.close()
    print("✓ Plot 5 saved: plot5_cache_misses.png")

def plot_cycles_per_byte():
    """Plot 6: Cycles per Byte (2x2 grid for all thread counts)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    # Total bytes transferred = msg_size * 8 fields * NUM_MESSAGES (1000000)
    NUM_MESSAGES = 1000000
    
    for idx, threads in enumerate(THREAD_COUNTS):
        cpb_a1 = [CYCLES['A1'][sz][threads] / (sz * 8 * NUM_MESSAGES) for sz in MSG_SIZES]
        cpb_a2 = [CYCLES['A2'][sz][threads] / (sz * 8 * NUM_MESSAGES) for sz in MSG_SIZES]
        cpb_a3 = [CYCLES['A3'][sz][threads] / (sz * 8 * NUM_MESSAGES) for sz in MSG_SIZES]
        
        axes[idx].plot(MSG_SIZES, cpb_a1, marker='o', linewidth=2, markersize=8, label='A1: Two-copy')
        axes[idx].plot(MSG_SIZES, cpb_a2, marker='s', linewidth=2, markersize=8, label='A2: One-copy')
        axes[idx].plot(MSG_SIZES, cpb_a3, marker='^', linewidth=2, markersize=8, label='A3: Zero-copy')
        axes[idx].set_title(f'Thread Count: {threads}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Message size (bytes)', fontsize=11)
        axes[idx].set_ylabel('Cycles per Byte', fontsize=11)
        axes[idx].legend(fontsize=9, loc='best')
        axes[idx].grid(True, linestyle='--', alpha=0.5)
        axes[idx].set_xscale('log')
    
    fig.suptitle(f'Cycles per Byte vs Message Size\n{SYSTEM_INFO}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('plot6_cycles_per_byte.png', dpi=150)
    plt.close()
    print("✓ Plot 6 saved: plot6_cycles_per_byte.png")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MT25066 - PA02 Plot Generation (Hardcoded Data)")
    print("=" * 60)
    print(f"System: {SYSTEM_INFO}")
    print(f"Message sizes: {MSG_SIZES}")
    print(f"Thread counts: {THREAD_COUNTS}")
    print(f"Implementations: {IMPLS}")
    print("=" * 60)
    
    print("\nGenerating plots...")
    plot_throughput_vs_msg_size()
    plot_latency_vs_thread_count()
    plot_throughput_scaling()
    plot_implementation_comparison()
    plot_cache_misses()
    plot_cycles_per_byte()
    
    print("\n" + "=" * 60)
    print("All 6 plots generated successfully!")
    print("=" * 60)
