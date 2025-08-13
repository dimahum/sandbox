# Starlink Control gRPC

A Go-based gRPC service for controlling and monitoring Starlink satellites.

## Overview

This project provides a gRPC API for:
- Getting satellite status information
- Updating satellite configurations
- Streaming real-time telemetry data

## Features

- **Satellite Status**: Get current position, status, and timestamp of satellites
- **Configuration Management**: Update satellite parameters remotely
- **Telemetry Streaming**: Real-time telemetry data streaming with configurable intervals

## Prerequisites

- Go 1.19 or later
- Protocol Buffers compiler (protoc)
- protoc-gen-go and protoc-gen-go-grpc plugins

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   cd starlink-cntrl-grpc
   go mod tidy
   ```

## Usage

### Running the Server

```bash
go run cmd/server/main.go
```

The server will start listening on port 50051.

### Running the Client

In a separate terminal:

```bash
go run cmd/client/main.go
```

The client will connect to the server and demonstrate all available RPC calls.

## Project Structure

```
starlink-cntrl-grpc/
├── cmd/
│   ├── server/          # gRPC server implementation
│   └── client/          # gRPC client example
├── proto/               # Protocol buffer definitions and generated code
├── pkg/                 # Shared packages
└── go.mod              # Go module definition
```

## API Reference

### StarlinkControl Service

#### GetSatelliteStatus
- **Request**: `SatelliteRequest` with satellite ID
- **Response**: `SatelliteResponse` with status, position, and timestamp

#### UpdateSatelliteConfig
- **Request**: `ConfigUpdateRequest` with satellite ID and configuration map
- **Response**: `ConfigUpdateResponse` with success status and message

#### StreamTelemetry
- **Request**: `TelemetryRequest` with satellite ID and interval
- **Response**: Stream of `TelemetryData` with temperature, power level, and signal strength

## Development

### Regenerating Protocol Buffers

If you modify the `.proto` files, regenerate the Go code:

```bash
protoc --go_out=. --go_opt=paths=source_relative \
       --go-grpc_out=. --go-grpc_opt=paths=source_relative \
       proto/starlink.proto
```

## License

This project is provided as-is for demonstration purposes.