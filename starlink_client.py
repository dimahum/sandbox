#!/usr/bin/env python3
"""
Starlink gRPC Client

This module provides functionality to connect to a Starlink terminal via gRPC
and read status information.

Usage:
    python starlink_client.py [--host HOST] [--port PORT]

Default connection: 192.168.100.1:9200 (standard Starlink terminal address)
"""

import argparse
import grpc
import json
import sys
import time
from typing import Optional, Dict, Any

# Import generated protobuf classes
from starlink_grpc import starlink_pb2
from starlink_grpc import starlink_pb2_grpc


class StarlinkClient:
    """Client for connecting to Starlink terminal via gRPC."""
    
    def __init__(self, host: str = "192.168.100.1", port: int = 9200):
        """
        Initialize Starlink client.
        
        Args:
            host: Starlink terminal IP address (default: 192.168.100.1)
            port: gRPC port (default: 9200)
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        
    def connect(self) -> bool:
        """
        Establish connection to Starlink terminal.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
            self.stub = starlink_pb2_grpc.DeviceStub(self.channel)
            
            # Test connection with a simple call
            grpc.channel_ready_future(self.channel).result(timeout=2)
            print(f"Successfully connected to Starlink terminal at {self.host}:{self.port}")
            return True
            
        except grpc.RpcError as e:
            print(f"Failed to connect to Starlink terminal: {e}")
            return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close the gRPC channel."""
        if self.channel:
            self.channel.close()
            print("Disconnected from Starlink terminal")
    
    def get_status(self) -> Optional[Dict[str, Any]]:
        """
        Get current status from Starlink terminal.
        
        Returns:
            Dict containing status information, or None if failed
        """
        if not self.stub:
            print("Not connected to Starlink terminal")
            return None
            
        try:
            # Create status request
            request = starlink_pb2.Request()
            request.id = int(time.time() * 1000)  # Use timestamp as ID
            request.get_status.CopyFrom(starlink_pb2.GetStatusRequest())
            
            # Make the request
            response = self.stub.Handle(request)
            
            # Parse response
            if response.HasField('get_status'):
                status_data = {
                    'device_info': {
                        'id': response.get_status.device_info.id,
                        'hardware_version': response.get_status.device_info.hardware_version,
                        'software_version': response.get_status.device_info.software_version,
                        'country_code': response.get_status.device_info.country_code,
                        'utc_offset_s': response.get_status.device_info.utc_offset_s,
                    },
                    'device_state': {
                        'uptime_s': response.get_status.device_state.uptime_s,
                    },
                    'timestamp': time.time()
                }
                return status_data
            else:
                print("No status data in response")
                return None
                
        except grpc.RpcError as e:
            print(f"gRPC error getting status: {e}")
            return None
        except Exception as e:
            print(f"Error getting status: {e}")
            return None
    
    def get_history(self) -> Optional[Dict[str, Any]]:
        """
        Get performance history from Starlink terminal.
        
        Returns:
            Dict containing history data, or None if failed
        """
        if not self.stub:
            print("Not connected to Starlink terminal")
            return None
            
        try:
            # Create history request
            request = starlink_pb2.Request()
            request.id = int(time.time() * 1000)  # Use timestamp as ID
            request.get_history.CopyFrom(starlink_pb2.GetHistoryRequest())
            
            # Make the request
            response = self.stub.Handle(request)
            
            # Parse response
            if response.HasField('get_history'):
                history_data = {
                    'current_time': response.get_history.current_time,
                    'pop_ping_drop_rate': list(response.get_history.pop_ping_drop_rate),
                    'pop_ping_latency_ms': list(response.get_history.pop_ping_latency_ms),
                    'downlink_throughput_bps': list(response.get_history.downlink_throughput_bps),
                    'uplink_throughput_bps': list(response.get_history.uplink_throughput_bps),
                    'timestamp': time.time()
                }
                return history_data
            else:
                print("No history data in response")
                return None
                
        except grpc.RpcError as e:
            print(f"gRPC error getting history: {e}")
            return None
        except Exception as e:
            print(f"Error getting history: {e}")
            return None


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Starlink gRPC Client")
    parser.add_argument("--host", default="192.168.100.1", 
                       help="Starlink terminal IP address (default: 192.168.100.1)")
    parser.add_argument("--port", type=int, default=9200,
                       help="gRPC port (default: 9200)")
    parser.add_argument("--status", action="store_true",
                       help="Get status information")
    parser.add_argument("--history", action="store_true", 
                       help="Get performance history")
    parser.add_argument("--continuous", action="store_true",
                       help="Continuously monitor status (every 10 seconds)")
    
    args = parser.parse_args()
    
    # Default to status if no specific option given
    if not args.status and not args.history and not args.continuous:
        args.status = True
    
    # Create client and connect
    client = StarlinkClient(args.host, args.port)
    
    try:
        if not client.connect():
            sys.exit(1)
        
        if args.continuous:
            print("Starting continuous monitoring (Ctrl+C to stop)...")
            try:
                while True:
                    status = client.get_status()
                    if status:
                        print(f"\n--- Status Update {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
                        print(json.dumps(status, indent=2))
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\nStopping continuous monitoring...")
        
        else:
            if args.status:
                print("Getting Starlink status...")
                status = client.get_status()
                if status:
                    print("Status:")
                    print(json.dumps(status, indent=2))
            
            if args.history:
                print("Getting Starlink performance history...")
                history = client.get_history()
                if history:
                    print("History:")
                    print(json.dumps(history, indent=2))
    
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()