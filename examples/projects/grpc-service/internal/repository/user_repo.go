package repository

import (
	"context"
	"errors"
	"sync"

	userv1 "github.com/agentic-canon/examples/grpc-service/api/proto/user/v1"
	"github.com/google/uuid"
	"google.golang.org/protobuf/proto"
)

// ErrUserNotFound indicates the requested user does not exist.
var ErrUserNotFound = errors.New("user not found")

// UserRepository provides CRUD operations for users.
type UserRepository struct {
	mu    sync.RWMutex
	users map[string]*userv1.User
}

// NewUserRepository returns an in-memory repository implementation.
func NewUserRepository() *UserRepository {
	return &UserRepository{users: make(map[string]*userv1.User)}
}

// Create stores a new user and returns it.
func (r *UserRepository) Create(_ context.Context, user *userv1.User) (*userv1.User, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	if user.GetId() == "" {
		user.Id = uuid.NewString()
	}

	copy := protoClone(user)
	r.users[user.GetId()] = copy
	return protoClone(copy), nil
}

// List returns all users.
func (r *UserRepository) List(_ context.Context) ([]*userv1.User, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	result := make([]*userv1.User, 0, len(r.users))
	for _, user := range r.users {
		copy := *user
		result = append(result, &copy)
	}
	return result, nil
}

// Get returns a user by ID.
func (r *UserRepository) Get(_ context.Context, id string) (*userv1.User, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if user, ok := r.users[id]; ok {
		copy := *user
		return &copy, nil
	}
	return nil, ErrUserNotFound
}

// Update modifies an existing user.
func (r *UserRepository) Update(_ context.Context, id string, req *userv1.UpdateUserRequest) (*userv1.User, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	existing, ok := r.users[id]
	if !ok {
		return nil, ErrUserNotFound
	}

	if req.GetEmail() != "" {
		existing.Email = req.GetEmail()
	}
	if req.GetName() != "" {
		existing.Name = req.GetName()
	}
	if req.GetRole() != "" {
		existing.Role = req.GetRole()
	}
	existing.Deactivated = req.GetDeactivated()

	return protoClone(existing), nil
}

// Delete removes a user by ID.
func (r *UserRepository) Delete(_ context.Context, id string) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, ok := r.users[id]; !ok {
		return ErrUserNotFound
	}
	delete(r.users, id)
	return nil
}

func protoClone(user *userv1.User) *userv1.User {
	if user == nil {
		return nil
	}
	return proto.Clone(user).(*userv1.User)
}
