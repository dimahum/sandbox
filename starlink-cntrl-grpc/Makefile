.PHONY: build clean server client proto

# Build all binaries
build:
	go build -o bin/server ./cmd/server
	go build -o bin/client ./cmd/client

# Run the server
server:
	go run cmd/server/main.go

# Run the client
client:
	go run cmd/client/main.go

# Generate protobuf files
proto:
	protoc --go_out=. --go_opt=paths=source_relative \
		--go-grpc_out=. --go-grpc_opt=paths=source_relative \
		proto/starlink.proto

# Clean build artifacts
clean:
	rm -rf bin/

# Install dependencies
deps:
	go mod tidy

# Test build
test-build: deps
	go build ./cmd/server
	go build ./cmd/client
	@echo "Build successful!"