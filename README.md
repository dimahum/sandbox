# Sandbox

This repository contains various projects and experiments.

## Starlink gRPC Client

A Python client for connecting to Starlink terminals via gRPC to read status and performance information.

### Requirements

- Python 3.7+
- grpcio >= 1.60.0
- grpcio-tools >= 1.60.0
- protobuf >= 4.25.0

### Installation

```bash
pip install -r requirements.txt
```

### Usage

#### Basic Status Check
```bash
python starlink_client.py --status
```

#### Get Performance History
```bash
python starlink_client.py --history
```

#### Continuous Monitoring
```bash
python starlink_client.py --continuous
```

#### Custom Host/Port
```bash
python starlink_client.py --host 192.168.1.100 --port 9200 --status
```

### Default Connection

The client defaults to connecting to `192.168.100.1:9200`, which is the standard Starlink terminal address when connected to the Starlink network.

### Features

- Connect to Starlink terminal via gRPC
- Read device status information (hardware version, software version, uptime, etc.)
- Get performance history (ping latency, throughput, drop rates)
- Continuous monitoring mode
- Configurable host and port
- JSON output format
- Proper error handling and connection management

### Note

This client requires access to a Starlink terminal on the network. The terminal must have gRPC API enabled (which is the default for most Starlink terminals).

## Other Projects

- **PlayerMovement**: Unity game project with player movement mechanics
