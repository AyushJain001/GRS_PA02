#!/bin/bash
# MT25066 - Network Namespace Setup for PA02
# This script creates separate network namespaces for client and server

set -e

# Clean up existing namespaces if they exist
cleanup() {
    echo "Cleaning up existing namespaces..."
    sudo ip netns del server_ns 2>/dev/null || true
    sudo ip netns del client_ns 2>/dev/null || true
    sudo ip link del veth-server 2>/dev/null || true
}

setup() {
    echo "Setting up network namespaces..."
    
    # Create namespaces
    sudo ip netns add server_ns
    sudo ip netns add client_ns
    
    # Create veth pair
    sudo ip link add veth-server type veth peer name veth-client
    
    # Move interfaces to namespaces
    sudo ip link set veth-server netns server_ns
    sudo ip link set veth-client netns client_ns
    
    # Configure server namespace (10.0.0.1)
    sudo ip netns exec server_ns ip addr add 10.0.0.1/24 dev veth-server
    sudo ip netns exec server_ns ip link set veth-server up
    sudo ip netns exec server_ns ip link set lo up
    
    # Configure client namespace (10.0.0.2)
    sudo ip netns exec client_ns ip addr add 10.0.0.2/24 dev veth-client
    sudo ip netns exec client_ns ip link set veth-client up
    sudo ip netns exec client_ns ip link set lo up
    
    echo "Namespace setup complete!"
    echo "  Server namespace: server_ns (IP: 10.0.0.1)"
    echo "  Client namespace: client_ns (IP: 10.0.0.2)"
    
    # Test connectivity
    echo "Testing connectivity..."
    sudo ip netns exec client_ns ping -c 1 10.0.0.1 && echo "✓ Connectivity OK"
}

case "$1" in
    setup)
        cleanup
        setup
        ;;
    cleanup)
        cleanup
        echo "Cleanup complete"
        ;;
    status)
        echo "=== Namespaces ==="
        ip netns list
        echo ""
        echo "=== Server NS IPs ==="
        sudo ip netns exec server_ns ip addr show 2>/dev/null || echo "server_ns not found"
        echo ""
        echo "=== Client NS IPs ==="
        sudo ip netns exec client_ns ip addr show 2>/dev/null || echo "client_ns not found"
        ;;
    *)
        echo "Usage: $0 {setup|cleanup|status}"
        exit 1
        ;;
esac
