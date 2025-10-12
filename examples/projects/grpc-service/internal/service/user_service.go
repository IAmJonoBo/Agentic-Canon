package service

import (
	"context"
	"errors"
	"fmt"
	"strings"

	"github.com/sirupsen/logrus"
	"google.golang.org/protobuf/types/known/timestamppb"

	userv1 "github.com/agentic-canon/examples/grpc-service/api/proto/user/v1"
	repo "github.com/agentic-canon/examples/grpc-service/internal/repository"
)

// UserService implements the user.v1.UserService gRPC contract.
type UserService struct {
	userv1.UnimplementedUserServiceServer
	repo *repo.UserRepository
	log  *logrus.Logger
}

// NewUserService constructs a new service with the supplied dependencies.
func NewUserService(repo *repo.UserRepository, log *logrus.Logger) *UserService {
	return &UserService{repo: repo, log: log}
}

// CreateUser handles user creation requests.
func (s *UserService) CreateUser(ctx context.Context, req *userv1.CreateUserRequest) (*userv1.CreateUserResponse, error) {
	if err := validateCreateRequest(req); err != nil {
		return nil, err
	}

	now := timestamppb.Now()
	user := &userv1.User{
		Email:     sanitize(req.GetEmail()),
		Name:      sanitize(req.GetName()),
		Role:      sanitize(req.GetRole()),
		CreatedAt: now,
		UpdatedAt: now,
	}

	created, err := s.repo.Create(ctx, user)
	if err != nil {
		return nil, fmt.Errorf("create user: %w", err)
	}

	s.log.WithFields(logrus.Fields{"user_id": created.GetId(), "email": created.GetEmail()}).Info("user created")

	return &userv1.CreateUserResponse{User: created}, nil
}

func (s *UserService) GetUser(ctx context.Context, req *userv1.GetUserRequest) (*userv1.GetUserResponse, error) {
	if req.GetId() == "" {
		return nil, errors.New("id is required")
	}

	user, err := s.repo.Get(ctx, req.GetId())
	if err != nil {
		return nil, mapRepositoryError(err)
	}

	return &userv1.GetUserResponse{User: user}, nil
}

func (s *UserService) ListUsers(ctx context.Context, _ *userv1.ListUsersRequest) (*userv1.ListUsersResponse, error) {
	users, err := s.repo.List(ctx)
	if err != nil {
		return nil, fmt.Errorf("list users: %w", err)
	}
	return &userv1.ListUsersResponse{Users: users}, nil
}

func (s *UserService) UpdateUser(ctx context.Context, req *userv1.UpdateUserRequest) (*userv1.UpdateUserResponse, error) {
	if req.GetId() == "" {
		return nil, errors.New("id is required")
	}

	updated, err := s.repo.Update(ctx, req.GetId(), req)
	if err != nil {
		return nil, mapRepositoryError(err)
	}

	updated.UpdatedAt = timestamppb.Now()
	return &userv1.UpdateUserResponse{User: updated}, nil
}

func (s *UserService) DeleteUser(ctx context.Context, req *userv1.DeleteUserRequest) (*userv1.DeleteUserResponse, error) {
	if req.GetId() == "" {
		return nil, errors.New("id is required")
	}

	if err := s.repo.Delete(ctx, req.GetId()); err != nil {
		return nil, mapRepositoryError(err)
	}

	s.log.WithField("user_id", req.GetId()).Info("user deleted")
	return &userv1.DeleteUserResponse{}, nil
}

func validateCreateRequest(req *userv1.CreateUserRequest) error {
	if req.GetEmail() == "" {
		return errors.New("email is required")
	}
	if !strings.Contains(req.GetEmail(), "@") {
		return errors.New("email must be valid")
	}
	if strings.TrimSpace(req.GetName()) == "" {
		return errors.New("name is required")
	}
	return nil
}

func sanitize(value string) string {
	return strings.TrimSpace(value)
}

func mapRepositoryError(err error) error {
	if errors.Is(err, repo.ErrUserNotFound) {
		return fmt.Errorf("user not found: %w", err)
	}
	return err
}
