package integration_test

import (
	"context"
	"net"
	"testing"

	"github.com/sirupsen/logrus"
	"github.com/stretchr/testify/require"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/test/bufconn"

	userv1 "github.com/agentic-canon/examples/grpc-service/api/proto/user/v1"
	"github.com/agentic-canon/examples/grpc-service/internal/repository"
	"github.com/agentic-canon/examples/grpc-service/internal/service"
)

const bufSize = 1024 * 1024

func TestUserService_GrpcRoundTrip(t *testing.T) {
	repo := repository.NewUserRepository()
	log := logrus.New()

	svc := service.NewUserService(repo, log)
	grpcServer := grpc.NewServer()
	listener := bufconn.Listen(bufSize)
	go func() {
		_ = grpcServer.Serve(listener)
	}()
	t.Cleanup(func() {
		grpcServer.Stop()
		listener.Close()
	})

	userv1.RegisterUserServiceServer(grpcServer, svc)

	conn, err := grpc.DialContext(
		context.Background(),
		"bufnet",
		grpc.WithContextDialer(func(ctx context.Context, s string) (net.Conn, error) {
			return listener.Dial()
		}),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	require.NoError(t, err)
	t.Cleanup(func() { _ = conn.Close() })

	client := userv1.NewUserServiceClient(conn)

	createResp, err := client.CreateUser(context.Background(), &userv1.CreateUserRequest{
		Email: "integration@example.com",
		Name:  "Integration User",
		Role:  "Engineer",
	})
	require.NoError(t, err)
	require.NotEmpty(t, createResp.GetUser().GetId())

	getResp, err := client.GetUser(context.Background(), &userv1.GetUserRequest{Id: createResp.User.Id})
	require.NoError(t, err)
	require.Equal(t, "Integration User", getResp.User.Name)
}
