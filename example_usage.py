#!/usr/bin/env python3
"""
Example usage of Starlink gRPC client

This example demonstrates how to use the StarlinkClient class
in your own Python applications.
"""

import json
import time
from starlink_client import StarlinkClient


def example_status_check():
    """Example: Get status information once."""
    print("Example: Getting Starlink status...")
    
    # Create client with default settings (192.168.100.1:9200)
    client = StarlinkClient()
    
    try:
        # Connect to Starlink terminal
        if client.connect():
            # Get status
            status = client.get_status()
            if status:
                print("Status received:")
                print(json.dumps(status, indent=2))
            else:
                print("Failed to get status")
        else:
            print("Failed to connect")
    
    finally:
        client.disconnect()


def example_custom_host():
    """Example: Connect to custom host/port."""
    print("\nExample: Connecting to custom host...")
    
    # Create client with custom host/port
    client = StarlinkClient(host="192.168.1.100", port=9200)
    
    try:
        if client.connect():
            print("Connected to custom host")
            # Could get status here
        else:
            print("Connection failed (expected if no Starlink at that address)")
    
    finally:
        client.disconnect()


def example_performance_monitoring():
    """Example: Monitor performance history."""
    print("\nExample: Getting performance history...")
    
    client = StarlinkClient()
    
    try:
        if client.connect():
            history = client.get_history()
            if history:
                print("Performance history:")
                # Show summary statistics
                if history['pop_ping_latency_ms']:
                    avg_latency = sum(history['pop_ping_latency_ms']) / len(history['pop_ping_latency_ms'])
                    print(f"Average ping latency: {avg_latency:.2f} ms")
                
                if history['pop_ping_drop_rate']:
                    avg_drop_rate = sum(history['pop_ping_drop_rate']) / len(history['pop_ping_drop_rate'])
                    print(f"Average drop rate: {avg_drop_rate:.2%}")
            else:
                print("Failed to get history")
        else:
            print("Failed to connect")
    
    finally:
        client.disconnect()


if __name__ == "__main__":
    print("Starlink gRPC Client Examples")
    print("=" * 30)
    
    # Note: These examples will fail without a real Starlink terminal
    # but demonstrate the proper usage patterns
    
    example_status_check()
    example_custom_host()
    example_performance_monitoring()
    
    print("\nNote: These examples require a Starlink terminal on the network.")
    print("Connection failures are expected without actual hardware.")