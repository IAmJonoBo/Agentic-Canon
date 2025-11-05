package main

import (
	"context"

	"github.com/agentic-canon/examples/grpc-service/internal/config"
	"github.com/agentic-canon/examples/grpc-service/internal/pkg/logger"
	"github.com/agentic-canon/examples/grpc-service/internal/server"
)

func main() {
	cfg := config.Load()
	log := logger.New("grpc-user-service")

	srv, err := server.New(cfg, log)
	if err != nil {
		log.WithError(err).Fatal("failed to initialise server")
	}

	if err := srv.Run(context.Background()); err != nil {
		log.WithError(err).Fatal("server exited with error")
	}
}
