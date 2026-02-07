#!/usr/bin/env bash
# MT25066 - Experiment Runner with Network Namespaces
set -euo pipefail

ROLL="MT25066"
PORT_BASE=5001
DURATION_SEC=3
TIMEOUT_SEC=20
MESSAGE_SIZES=(64 256 1024 4096)
THREAD_COUNTS=(1 2 4 8)

# Namespace config
SERVER_NS="server_ns"
CLIENT_NS="client_ns"
SERVER_IP="10.0.0.1"

HEADER="impl,msg_size,threads,throughput_gbps,avg_latency_us,cycles,l1_misses,llc_misses,context_switches"

echo "$HEADER" > "${ROLL}_Part_C_Summary.csv"

# Global port counter for unique ports
CURRENT_PORT=$PORT_BASE

parse_perf_value() {
    local file="$1"
    local event="$2"
    
    if [[ ! -f "$file" ]]; then
        echo "0"
        return
    fi
    
    local value
    value=$(grep "$event" "$file" 2>/dev/null | head -1 | cut -d',' -f1 | tr -d ' ' || echo "0")
    
    if [[ -z "$value" || "$value" == "<not" || "$value" == "not" ]]; then
        echo "0"
    else
        echo "$value"
    fi
}

run_one() {
    local impl="$1"
    local server_bin="$2"
    local client_bin="$3"
    local msg_size="$4"
    local threads="$5"
    
    # Use unique port for each run and increment
    CURRENT_PORT=$((CURRENT_PORT + 1))
    local port=$CURRENT_PORT

    local perf_out="${ROLL}_Part_C_${impl}_${msg_size}_${threads}.perf"
    local csv_out="${ROLL}_Part_C_${impl}_${msg_size}_${threads}.csv"

    rm -f "$perf_out" "$csv_out"

    echo "  Starting $impl (msg=$msg_size, threads=$threads, port=$port)..."
    
    # Run server in server namespace
    sudo ip netns exec $SERVER_NS timeout $TIMEOUT_SEC $(pwd)/$server_bin "$port" "$msg_size" > /dev/null 2>&1 &
    local server_pid=$!
    sleep 1

    set +e
    local client_output
    local client_status
    
    # Run client in client namespace with perf
    client_output=$(sudo ip netns exec $CLIENT_NS timeout $TIMEOUT_SEC perf stat -x, -e cpu_core/cycles/,context-switches,cpu_core/L1-dcache-load-misses/,cpu_core/LLC-load-misses/ \
        -- timeout $TIMEOUT_SEC $(pwd)/$client_bin "$SERVER_IP" "$port" "$msg_size" "$threads" "$DURATION_SEC" \
        2> "$perf_out")
    client_status=$?
    
    set -e

    sudo kill $server_pid >/dev/null 2>&1 || true
    wait $server_pid >/dev/null 2>&1 || true
    sleep 1

    local throughput="0"
    local latency="0"
    
    if echo "$client_output" | grep -q "THROUGHPUT_GBPS"; then
        throughput=$(echo "$client_output" | grep -oE 'THROUGHPUT_GBPS=[0-9.]+' | cut -d= -f2 || echo "0")
        latency=$(echo "$client_output" | grep -oE 'AVG_LATENCY_US=[0-9.]+' | cut -d= -f2 || echo "0")
    fi

    local cycles=$(parse_perf_value "$perf_out" "cycles")
    local l1_misses=$(parse_perf_value "$perf_out" "L1-dcache-load-misses")
    local llc_misses=$(parse_perf_value "$perf_out" "LLC-load-misses")
    local ctx_switches=$(parse_perf_value "$perf_out" "context-switches")

    echo "$impl,$msg_size,$threads,$throughput,$latency,$cycles,$l1_misses,$llc_misses,$ctx_switches" | tee -a "${ROLL}_Part_C_Summary.csv"
    
    echo "$HEADER" > "$csv_out"
    echo "$impl,$msg_size,$threads,$throughput,$latency,$cycles,$l1_misses,$llc_misses,$ctx_switches" >> "$csv_out"
}

cd "$(dirname "$0")" || exit 1

echo "=========================================="
echo "MT25066 - PA02 Experiment Runner"
echo "=========================================="
echo "Using Network Namespaces:"
echo "  Server: $SERVER_NS ($SERVER_IP)"
echo "  Client: $CLIENT_NS"
echo "=========================================="

# Check namespaces exist
if ! ip netns list | grep -q $SERVER_NS; then
    echo "ERROR: Namespace $SERVER_NS not found!"
    echo "Run: sudo ./setup_namespaces.sh setup"
    exit 1
fi

echo "Building..."
make clean > /dev/null 2>&1
make

echo ""
echo "Starting experiments..."
echo "Duration per run: $DURATION_SEC seconds"
echo "Timeout: $TIMEOUT_SEC seconds"
echo ""

TOTAL=$((${#MESSAGE_SIZES[@]} * ${#THREAD_COUNTS[@]} * 3))
COUNT=0

for msg_size in "${MESSAGE_SIZES[@]}"; do
    for threads in "${THREAD_COUNTS[@]}"; do
        echo "--- Message Size: $msg_size bytes, Threads: $threads ---"
        
        run_one "A1" "MT25066_Part_A1_Server" "MT25066_Part_A1_Client" "$msg_size" "$threads"
        COUNT=$((COUNT + 1))
        echo "  Progress: $COUNT/$TOTAL"
        
        run_one "A2" "MT25066_Part_A2_Server" "MT25066_Part_A2_Client" "$msg_size" "$threads"
        COUNT=$((COUNT + 1))
        echo "  Progress: $COUNT/$TOTAL"
        
        run_one "A3" "MT25066_Part_A3_Server" "MT25066_Part_A3_Client" "$msg_size" "$threads"
        COUNT=$((COUNT + 1))
        echo "  Progress: $COUNT/$TOTAL"
        
        echo ""
    done
done

echo "=========================================="
echo "EXPERIMENT COMPLETE"
echo "=========================================="
echo "Summary: ${ROLL}_Part_C_Summary.csv"
echo ""
echo "Results:"
cat "${ROLL}_Part_C_Summary.csv"
