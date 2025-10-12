package middleware

import (
	"context"
	"time"

	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
)

// UnaryLoggingInterceptor logs request information and latency.
func UnaryLoggingInterceptor(log *logrus.Logger) grpc.UnaryServerInterceptor {
	return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
		start := time.Now()
		resp, err := handler(ctx, req)
		entry := log.WithFields(logrus.Fields{
			"method":   info.FullMethod,
			"duration": time.Since(start).String(),
		})
		if err != nil {
			entry.WithError(err).Error("request failed")
		} else {
			entry.Info("request completed")
		}
		return resp, err
	}
}

// StreamLoggingInterceptor logs streaming calls.
func StreamLoggingInterceptor(log *logrus.Logger) grpc.StreamServerInterceptor {
	return func(srv interface{}, ss grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
		start := time.Now()
		err := handler(srv, ss)
		entry := log.WithFields(logrus.Fields{
			"method":   info.FullMethod,
			"duration": time.Since(start).String(),
		})
		if err != nil {
			entry.WithError(err).Error("stream failed")
		} else {
			entry.Info("stream completed")
		}
		return err
	}
}

// UnaryServerInterceptors returns default unary interceptors.
func UnaryServerInterceptors(log *logrus.Logger) []grpc.UnaryServerInterceptor {
	return []grpc.UnaryServerInterceptor{
		UnaryLoggingInterceptor(log),
	}
}

// StreamServerInterceptors returns default stream interceptors.
func StreamServerInterceptors(log *logrus.Logger) []grpc.StreamServerInterceptor {
	return []grpc.StreamServerInterceptor{StreamLoggingInterceptor(log)}
}
