package server

import (
	"context"
	"errors"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	grpc_recovery "github.com/grpc-ecosystem/go-grpc-middleware/v2/interceptors/recovery"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"

	userv1 "github.com/agentic-canon/examples/grpc-service/api/proto/user/v1"
	"github.com/agentic-canon/examples/grpc-service/internal/config"
	"github.com/agentic-canon/examples/grpc-service/internal/middleware"
	"github.com/agentic-canon/examples/grpc-service/internal/repository"
	"github.com/agentic-canon/examples/grpc-service/internal/service"
)

// Server encapsulates the gRPC and HTTP servers.
type Server struct {
	cfg        config.Config
	log        *logrus.Logger
	grpcServer *grpc.Server
	httpServer *http.Server
	listener   net.Listener
}

// New creates a configured Server.
func New(cfg config.Config, log *logrus.Logger) (*Server, error) {
	listener, err := net.Listen("tcp", fmt.Sprintf(":%s", cfg.GRPCPort))
	if err != nil {
		return nil, fmt.Errorf("listen on %s: %w", cfg.GRPCPort, err)
	}

	repo := repository.NewUserRepository()
	userSvc := service.NewUserService(repo, log)

	unaryInterceptors := append(
		middleware.UnaryServerInterceptors(log),
		grpc_recovery.UnaryServerInterceptor(),
	)

	streamInterceptors := append(
		middleware.StreamServerInterceptors(log),
		grpc_recovery.StreamServerInterceptor(),
	)

	grpcServer := grpc.NewServer(
		grpc.ChainUnaryInterceptor(unaryInterceptors...),
		grpc.ChainStreamInterceptor(streamInterceptors...),
	)

	userv1.RegisterUserServiceServer(grpcServer, userSvc)

	mux := runtime.NewServeMux()
	ctx := context.Background()
	if err := userv1.RegisterUserServiceHandlerServer(ctx, mux, userSvc); err != nil {
		return nil, fmt.Errorf("register gateway handler: %w", err)
	}

	httpServer := &http.Server{
		Addr:              fmt.Sprintf(":%s", cfg.HTTPPort),
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
		WriteTimeout:      30 * time.Second,
	}

	return &Server{
		cfg:        cfg,
		log:        log,
		grpcServer: grpcServer,
		httpServer: httpServer,
		listener:   listener,
	}, nil
}

// Run starts the gRPC and HTTP servers and blocks until graceful shutdown.
func (s *Server) Run(ctx context.Context) error {
	s.log.WithFields(logrus.Fields{
		"grpc_port": s.cfg.GRPCPort,
		"http_port": s.cfg.HTTPPort,
	}).Info("starting gRPC service")

	errCh := make(chan error, 2)

	go func() {
		if err := s.grpcServer.Serve(s.listener); err != nil {
			errCh <- fmt.Errorf("gRPC server: %w", err)
		}
	}()

	go func() {
		if err := s.httpServer.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			errCh <- fmt.Errorf("HTTP gateway: %w", err)
		}
	}()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	select {
	case <-ctx.Done():
	case sig := <-sigCh:
		s.log.WithField("signal", sig.String()).Info("received shutdown signal")
	case err := <-errCh:
		return err
	}

	shutdownCtx, cancel := context.WithTimeout(context.Background(), s.cfg.GracefulShutdown)
	defer cancel()

	s.grpcServer.GracefulStop()
	if err := s.httpServer.Shutdown(shutdownCtx); err != nil {
		return fmt.Errorf("http shutdown: %w", err)
	}

	s.log.Info("shutdown complete")
	return nil
}
