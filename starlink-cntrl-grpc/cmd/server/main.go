package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"time"

	"google.golang.org/grpc"
	pb "starlink-cntrl-grpc/proto"
)

type server struct {
	pb.UnimplementedStarlinkControlServer
}

// GetSatelliteStatus implements the GetSatelliteStatus RPC
func (s *server) GetSatelliteStatus(ctx context.Context, req *pb.SatelliteRequest) (*pb.SatelliteResponse, error) {
	log.Printf("Received request for satellite: %s", req.SatelliteId)
	
	// Mock satellite data
	return &pb.SatelliteResponse{
		SatelliteId: req.SatelliteId,
		Status:      "operational",
		Latitude:    45.5017,
		Longitude:   -73.5673,
		Altitude:    550000, // 550 km
		Timestamp:   time.Now().Unix(),
	}, nil
}

// UpdateSatelliteConfig implements the UpdateSatelliteConfig RPC
func (s *server) UpdateSatelliteConfig(ctx context.Context, req *pb.ConfigUpdateRequest) (*pb.ConfigUpdateResponse, error) {
	log.Printf("Updating config for satellite: %s", req.SatelliteId)
	log.Printf("Config updates: %v", req.Config)
	
	// Mock configuration update
	return &pb.ConfigUpdateResponse{
		Success: true,
		Message: fmt.Sprintf("Configuration updated successfully for satellite %s", req.SatelliteId),
	}, nil
}

// StreamTelemetry implements the StreamTelemetry RPC
func (s *server) StreamTelemetry(req *pb.TelemetryRequest, stream pb.StarlinkControl_StreamTelemetryServer) error {
	log.Printf("Starting telemetry stream for satellite: %s", req.SatelliteId)
	
	interval := time.Duration(req.IntervalSeconds) * time.Second
	if interval == 0 {
		interval = 5 * time.Second // default interval
	}
	
	ticker := time.NewTicker(interval)
	defer ticker.Stop()
	
	for i := 0; i < 10; i++ { // Send 10 telemetry messages
		select {
		case <-stream.Context().Done():
			return stream.Context().Err()
		case <-ticker.C:
			telemetry := &pb.TelemetryData{
				SatelliteId:    req.SatelliteId,
				Temperature:    -45.5 + float64(i)*2.1, // Mock temperature
				PowerLevel:     85.5 - float64(i)*0.5,  // Mock power level
				SignalStrength: "strong",
				Timestamp:      time.Now().Unix(),
			}
			
			if err := stream.Send(telemetry); err != nil {
				return err
			}
			
			log.Printf("Sent telemetry data for satellite: %s", req.SatelliteId)
		}
	}
	
	return nil
}

func main() {
	port := ":50051"
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterStarlinkControlServer(s, &server{})

	log.Printf("Starlink Control gRPC server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}