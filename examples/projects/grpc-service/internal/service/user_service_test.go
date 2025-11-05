package service_test

import (
	"context"
	"testing"

	"github.com/sirupsen/logrus"
	"github.com/stretchr/testify/require"

	userv1 "github.com/agentic-canon/examples/grpc-service/api/proto/user/v1"
	"github.com/agentic-canon/examples/grpc-service/internal/repository"
	"github.com/agentic-canon/examples/grpc-service/internal/service"
)

func TestCreateUser(t *testing.T) {
	repo := repository.NewUserRepository()
	log := logrus.New()
	svc := service.NewUserService(repo, log)

	resp, err := svc.CreateUser(context.Background(), &userv1.CreateUserRequest{
		Email: "dev@example.com",
		Name:  "Dev User",
		Role:  "Engineer",
	})

	require.NoError(t, err)
	require.NotNil(t, resp)
	require.NotEmpty(t, resp.User.GetId())
}

func TestCreateUserValidation(t *testing.T) {
	repo := repository.NewUserRepository()
	log := logrus.New()
	svc := service.NewUserService(repo, log)

	_, err := svc.CreateUser(context.Background(), &userv1.CreateUserRequest{})
	require.Error(t, err)
}
