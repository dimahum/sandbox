package main

import (
	"context"
	"io"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	pb "starlink-cntrl-grpc/proto"
)

func main() {
	// Connect to the server
	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer conn.Close()

	client := pb.NewStarlinkControlClient(conn)

	// Test GetSatelliteStatus
	log.Println("=== Testing GetSatelliteStatus ===")
	statusReq := &pb.SatelliteRequest{
		SatelliteId: "starlink-1234",
	}
	
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
	defer cancel()
	
	statusResp, err := client.GetSatelliteStatus(ctx, statusReq)
	if err != nil {
		log.Fatalf("GetSatelliteStatus failed: %v", err)
	}
	
	log.Printf("Satellite Status: %+v", statusResp)

	// Test UpdateSatelliteConfig
	log.Println("\n=== Testing UpdateSatelliteConfig ===")
	configReq := &pb.ConfigUpdateRequest{
		SatelliteId: "starlink-1234",
		Config: map[string]string{
			"transmission_power": "75",
			"frequency":          "12.5GHz",
			"mode":              "active",
		},
	}
	
	configResp, err := client.UpdateSatelliteConfig(ctx, configReq)
	if err != nil {
		log.Fatalf("UpdateSatelliteConfig failed: %v", err)
	}
	
	log.Printf("Config Update Response: %+v", configResp)

	// Test StreamTelemetry
	log.Println("\n=== Testing StreamTelemetry ===")
	telemetryReq := &pb.TelemetryRequest{
		SatelliteId:     "starlink-1234",
		IntervalSeconds: 2,
	}
	
	stream, err := client.StreamTelemetry(ctx, telemetryReq)
	if err != nil {
		log.Fatalf("StreamTelemetry failed: %v", err)
	}
	
	for {
		telemetry, err := stream.Recv()
		if err == io.EOF {
			log.Println("Telemetry stream ended")
			break
		}
		if err != nil {
			log.Fatalf("Failed to receive telemetry: %v", err)
		}
		
		log.Printf("Received telemetry: %+v", telemetry)
	}

	log.Println("Client finished successfully")
}