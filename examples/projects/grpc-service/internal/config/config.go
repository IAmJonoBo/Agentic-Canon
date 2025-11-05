package config

import (
	"fmt"
	"os"
	"time"
)

// Config holds runtime configuration for the service.
type Config struct {
	GRPCPort         string
	HTTPPort         string
	Environment      string
	GracefulShutdown time.Duration
}

// Load creates a Config by reading environment variables with sane defaults.
func Load() Config {
	cfg := Config{
		GRPCPort:         getEnv("GRPC_PORT", "9090"),
		HTTPPort:         getEnv("HTTP_PORT", "8080"),
		Environment:      getEnv("APP_ENV", "development"),
		GracefulShutdown: parseDuration(getEnv("GRACEFUL_SHUTDOWN", "15s")),
	}
	return cfg
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok && value != "" {
		return value
	}
	return fallback
}

func parseDuration(value string) time.Duration {
	d, err := time.ParseDuration(value)
	if err != nil {
		panic(fmt.Sprintf("invalid duration for GRACEFUL_SHUTDOWN: %s", value))
	}
	return d
}
