#!/usr/bin/env python3
"""
Test script for Starlink gRPC client

This script tests the basic functionality of the Starlink client
without requiring actual hardware.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from starlink_client import StarlinkClient


def test_client_initialization():
    """Test client can be initialized with default parameters."""
    print("Testing client initialization...")
    client = StarlinkClient()
    assert client.host == "192.168.100.1"
    assert client.port == 9200
    print("✓ Client initialization successful")


def test_client_custom_params():
    """Test client can be initialized with custom parameters."""
    print("Testing client with custom parameters...")
    client = StarlinkClient("192.168.1.100", 9201)
    assert client.host == "192.168.1.100"
    assert client.port == 9201
    print("✓ Custom parameters set correctly")


def test_connection_attempt():
    """Test connection attempt (will fail but should handle gracefully)."""
    print("Testing connection attempt (expected to fail)...")
    client = StarlinkClient("127.0.0.1", 9999)  # Use localhost on unused port
    result = client.connect()
    assert result == False  # Should fail gracefully
    client.disconnect()
    print("✓ Connection failure handled gracefully")


def test_protobuf_imports():
    """Test that protobuf classes can be imported and used."""
    print("Testing protobuf imports...")
    from starlink_grpc import starlink_pb2
    from starlink_grpc import starlink_pb2_grpc
    
    # Test creating request objects
    request = starlink_pb2.Request()
    request.id = 12345
    request.get_status.CopyFrom(starlink_pb2.GetStatusRequest())
    
    assert request.id == 12345
    assert request.HasField('get_status')
    print("✓ Protobuf classes working correctly")


def main():
    """Run all tests."""
    print("Running Starlink gRPC client tests...\n")
    
    try:
        test_client_initialization()
        test_client_custom_params()
        test_connection_attempt()
        test_protobuf_imports()
        
        print("\n✓ All tests passed!")
        return 0
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())