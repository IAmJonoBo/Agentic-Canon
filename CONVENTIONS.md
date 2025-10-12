# Conventions - Best Practice Standards

**Version:** 1.0.0  
**Last Updated:** 2025-10-12  
**Purpose:** Comprehensive conventions and best practices for consistent software development  
**Standards Compliance:** Industry best practices, language idioms, and community standards

---

## Table of Contents

- [Overview](#overview)
- [Code Style Conventions](#code-style-conventions)
- [Naming Conventions](#naming-conventions)
- [Git Conventions](#git-conventions)
- [Documentation Conventions](#documentation-conventions)
- [Testing Conventions](#testing-conventions)
- [Security Conventions](#security-conventions)
- [API Conventions](#api-conventions)
- [Database Conventions](#database-conventions)
- [Configuration Conventions](#configuration-conventions)
- [Project Structure Conventions](#project-structure-conventions)
- [Communication Conventions](#communication-conventions)

---

## Overview

This document defines the **consistent conventions** used across all Agentic Canon projects. These conventions ensure:

- **Consistency**: Code looks like it's written by one person
- **Readability**: Easy to understand and navigate
- **Maintainability**: Easy to modify and extend
- **Collaboration**: Team members can work seamlessly together
- **Automation**: Conventions enable automated tooling

### Convention Philosophy

1. **Consistency over Perfection**: Follow conventions even if you disagree
2. **Community Standards**: Align with language/framework conventions
3. **Explicit over Implicit**: Make intentions clear
4. **Automation**: Use tools to enforce conventions
5. **Evolution**: Conventions evolve with community standards

---

## Code Style Conventions

### Python Code Style

**PEP 8 Compliance**
```python
# Good: Clear, PEP 8 compliant
def calculate_user_score(user_id: int, include_bonus: bool = False) -> float:
    """Calculate the total score for a user.
    
    Args:
        user_id: The unique identifier for the user
        include_bonus: Whether to include bonus points
        
    Returns:
        The calculated score as a float
    """
    score = get_base_score(user_id)
    if include_bonus:
        score += get_bonus_points(user_id)
    return score

# Bad: PEP 8 violations
def calcScore(userId,includeBonus=False):
    score=getBaseScore(userId)
    if includeBonus:score+=getBonusPoints(userId)
    return score
```

**Black Formatting**
- Line length: 88 characters
- Use double quotes for strings
- Trailing commas in multi-line structures
- Consistent indentation (4 spaces)

**Import Organization**
```python
# Standard library imports
import os
import sys
from datetime import datetime
from typing import Optional

# Third-party imports
import requests
from fastapi import FastAPI

# Local imports
from myapp.models import User
from myapp.services import UserService
```

**Type Hints**
```python
# Always use type hints for function signatures
def process_data(
    data: list[dict[str, Any]],
    config: Optional[Config] = None
) -> ProcessedData:
    """Process raw data into structured format."""
    ...

# Use type aliases for complex types
UserId = int
UserData = dict[str, Any]
UserMap = dict[UserId, UserData]
```

### TypeScript/JavaScript Code Style

**TypeScript Strict Mode**
```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

**Prettier Formatting**
```typescript
// Good: Prettier formatted
export interface UserScore {
  userId: number;
  score: number;
  bonusPoints?: number;
}

export async function calculateUserScore(
  userId: number,
  includeBonus: boolean = false
): Promise<number> {
  const baseScore = await getBaseScore(userId);
  if (includeBonus) {
    const bonus = await getBonusPoints(userId);
    return baseScore + bonus;
  }
  return baseScore;
}

// Bad: Inconsistent formatting
export interface UserScore{userId:number;score:number;bonusPoints?:number}
export async function calculateUserScore(userId:number,includeBonus:boolean=false):Promise<number>{
  const baseScore=await getBaseScore(userId);
  if(includeBonus){const bonus=await getBonusPoints(userId);return baseScore+bonus;}
  return baseScore;
}
```

**ESLint Configuration**
- Use Airbnb style guide as base
- Enable TypeScript-specific rules
- Enforce no `any` types
- Require explicit return types
- No unused variables

### Go Code Style

**gofmt and goimports**
```go
// Good: Properly formatted
package user

import (
    "context"
    "fmt"
    
    "github.com/example/myapp/models"
)

// CalculateUserScore calculates the total score for a user.
func CalculateUserScore(ctx context.Context, userID int, includeBonus bool) (float64, error) {
    score, err := getBaseScore(ctx, userID)
    if err != nil {
        return 0, fmt.Errorf("failed to get base score: %w", err)
    }
    
    if includeBonus {
        bonus, err := getBonusPoints(ctx, userID)
        if err != nil {
            return 0, fmt.Errorf("failed to get bonus: %w", err)
        }
        score += bonus
    }
    
    return score, nil
}
```

**Go Conventions**
- Early returns for error handling
- Receiver names: 1-2 letters (consistent per type)
- Interface names: -er suffix (Reader, Writer)
- Exported names: Start with uppercase
- Package names: Lowercase, single word

---

## Naming Conventions

### General Naming Principles

1. **Descriptive**: Names should clearly indicate purpose
2. **Pronounceable**: Easy to say out loud
3. **Searchable**: Avoid single-letter names (except loop counters)
4. **No Abbreviations**: Except domain-standard terms (HTTP, API, URL)
5. **Context-Appropriate**: Length proportional to scope

### File Naming

**General Rules**
- Lowercase with hyphens (kebab-case) for multi-word files
- Extensions match language (.py, .ts, .go, .md)
- Descriptive names indicating content

```bash
# Good file names
user-service.ts
calculate-score.py
api-router.go
user-authentication.md
integration-test.spec.ts

# Bad file names
UserService.ts  # Mixed case
calc.py         # Unclear abbreviation
test1.spec.ts   # Non-descriptive
README.txt      # Wrong extension for markdown
```

**Component Files**
```bash
# React components (PascalCase for components)
Button.tsx
UserProfile.tsx
NavigationBar.tsx

# Vue components
UserProfile.vue
DataTable.vue

# Test files (mirror source file name)
Button.test.tsx
UserProfile.spec.ts
user-service.test.py
```

### Variable Naming

**Python Variables**
```python
# Good: snake_case, descriptive
user_count = 10
max_retry_attempts = 3
is_authenticated = False
has_permission = True
should_retry = False
can_edit = True

# Bad: inconsistent, unclear
userCount = 10      # camelCase (not Python convention)
maxRetry = 3        # Unclear if max attempts or max time
auth = False        # Abbreviation
perm = True         # Abbreviation
```

**TypeScript Variables**
```typescript
// Good: camelCase, descriptive
const userCount = 10;
const maxRetryAttempts = 3;
const isAuthenticated = false;
const hasPermission = true;

// Constants: UPPER_SNAKE_CASE
const MAX_CONNECTIONS = 100;
const API_BASE_URL = 'https://api.example.com';

// Bad
const UserCount = 10;      // Should be camelCase
const max_retry = 3;       // Should be camelCase
const auth = false;        // Abbreviation
```

**Go Variables**
```go
// Good: camelCase for local, PascalCase for exported
userCount := 10
maxRetryAttempts := 3
isAuthenticated := false

// Exported variables
MaxConnections = 100
APIBaseURL = "https://api.example.com"

// Bad
UserCount := 10    // Should be camelCase (unless exported)
max_retry := 3     // Should be camelCase
auth := false      // Abbreviation
```

### Function Naming

**Python Functions**
```python
# Good: verb_noun, descriptive
def get_user_by_id(user_id: int) -> User:
    ...

def calculate_total_score(scores: list[float]) -> float:
    ...

def validate_email_format(email: str) -> bool:
    ...

def send_notification_email(user: User, message: str) -> None:
    ...

# Bad
def user(user_id: int) -> User:  # Missing verb
    ...

def calc(scores: list[float]) -> float:  # Abbreviation
    ...

def check(email: str) -> bool:  # Vague verb
    ...
```

**TypeScript Functions**
```typescript
// Good: verbNoun, descriptive
function getUserById(userId: number): User {
    ...
}

function calculateTotalScore(scores: number[]): number {
    ...
}

function validateEmailFormat(email: string): boolean {
    ...
}

async function sendNotificationEmail(user: User, message: string): Promise<void> {
    ...
}

// Bad
function user(userId: number): User {  // Missing verb
    ...
}

function calc(scores: number[]): number {  // Abbreviation
    ...
}
```

**Go Functions**
```go
// Good: VerbNoun (exported), verbNoun (private)
func GetUserByID(ctx context.Context, userID int) (*User, error) {
    ...
}

func calculateTotalScore(scores []float64) float64 {
    ...
}

// Bad
func User(ctx context.Context, userID int) (*User, error) {  // Missing verb
    ...
}

func calc(scores []float64) float64 {  // Abbreviation
    ...
}
```

### Class/Type Naming

**Python Classes**
```python
# Good: PascalCase, noun
class UserService:
    ...

class EmailValidator:
    ...

class DatabaseConnection:
    ...

# Bad
class user_service:  # Should be PascalCase
    ...

class validateEmail:  # Should be noun, not verb
    ...
```

**TypeScript Classes/Interfaces**
```typescript
// Good: PascalCase
class UserService {
    ...
}

interface UserData {
    id: number;
    name: string;
}

type UserId = number;

// Bad
class userService {  // Should be PascalCase
    ...
}

interface IUserData {  // No 'I' prefix needed in TypeScript
    ...
}
```

**Go Types**
```go
// Good: PascalCase for exported, camelCase for private
type UserService struct {
    ...
}

type userCache struct {
    ...
}

// Interface with -er suffix
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

### Boolean Variable Naming

**Use Clear Prefixes**
```python
# Good: is_, has_, should_, can_, will_
is_valid = True
has_permission = True
should_retry = True
can_edit = True
will_expire = True

# Bad: unclear or negative
valid = True        # Less clear
no_permission = True  # Double negative
retry = True        # Unclear type
```

### Collection Naming

**Use Plural Forms**
```python
# Good: Plural for collections
users = [user1, user2, user3]
email_addresses = ["a@b.com", "c@d.com"]
scores_by_user = {user1: 100, user2: 95}

# Bad: Singular or unclear
user = [user1, user2, user3]  # Confusing
emails = ["a@b.com", "c@d.com"]  # Ambiguous (email objects or addresses?)
user_scores = {user1: 100, user2: 95}  # Unclear structure
```

---

## Git Conventions

### Branch Naming

**Branch Name Format**
```bash
<type>/<short-description>

# Types:
feature/    # New feature
fix/        # Bug fix
docs/       # Documentation changes
refactor/   # Code refactoring
test/       # Adding or updating tests
chore/      # Maintenance tasks

# Good examples
feature/user-authentication
fix/email-validation-bug
docs/api-documentation-update
refactor/database-connection-pool
test/integration-tests-for-auth
chore/update-dependencies

# Bad examples
feature/Feature1          # Not descriptive
fix-bug                   # No type prefix
john/working-on-feature   # Personal branch name
temp                      # Unclear purpose
```

### Commit Messages

**Conventional Commits Format**
```bash
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance
- `security`: Security improvements
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Examples**
```bash
# Good commit messages
feat(auth): add OAuth2 authentication support

Implements OAuth2 flow with Google and GitHub providers.
Includes token refresh and revocation.

Closes #123

---

fix(api): correct email validation regex

The previous regex didn't handle plus signs in email addresses.
Updated to RFC 5322 compliant pattern.

Fixes #456

---

docs: update API documentation for v2 endpoints

Add examples for all v2 endpoints and deprecation notices for v1.

---

# Bad commit messages
update            # No type, not descriptive
Fixed stuff       # Not conventional format
WIP               # Work in progress (squash before merge)
asdf              # Meaningless
```

**Commit Message Best Practices**
- Use imperative mood ("add" not "added")
- First line <= 72 characters
- Separate subject from body with blank line
- Body wraps at 72 characters
- Reference issues/PRs in footer
- Explain *what* and *why*, not *how*

### Pull Request Conventions

**PR Title Format**
- Follow conventional commit format
- Clear and descriptive
- Start with type prefix

**PR Description Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows style guide
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No security issues
- [ ] Breaking changes documented

## Related Issues
Closes #123
Related to #456
```

**PR Size Guidelines**
- Target: < 400 lines changed
- Maximum: 800 lines (excluding generated code)
- Split large changes into multiple PRs
- One logical change per PR

---

## Documentation Conventions

### README Structure

**Standard README Template**
```markdown
# Project Name

Brief one-line description

## Overview
Detailed project description (2-3 paragraphs)

## Features
- Key feature 1
- Key feature 2
- Key feature 3

## Installation
```bash
# Installation steps
```

## Quick Start
```bash
# Minimal example to get started
```

## Usage
### Basic Usage
[Examples]

### Advanced Usage
[Examples]

## Configuration
[Configuration options]

## API Documentation
[Link to full API docs]

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
[License information]

## Support
[How to get help]
```

### Code Documentation

**Python Docstring Format (Google Style)**
```python
def calculate_score(user_id: int, include_bonus: bool = False) -> float:
    """Calculate the total score for a user.
    
    This function retrieves the base score and optionally adds bonus points.
    
    Args:
        user_id: The unique identifier for the user. Must be positive.
        include_bonus: Whether to include bonus points in calculation.
            Defaults to False.
    
    Returns:
        The calculated score as a float. Returns 0.0 if user not found.
    
    Raises:
        ValueError: If user_id is negative or zero.
        DatabaseError: If database connection fails.
    
    Example:
        >>> calculate_score(123)
        85.5
        >>> calculate_score(123, include_bonus=True)
        100.0
    """
    if user_id <= 0:
        raise ValueError("user_id must be positive")
    ...
```

**TypeScript JSDoc Format**
```typescript
/**
 * Calculate the total score for a user.
 * 
 * Retrieves the base score and optionally adds bonus points.
 * 
 * @param userId - The unique identifier for the user (must be positive)
 * @param includeBonus - Whether to include bonus points (default: false)
 * @returns The calculated score
 * @throws {Error} If userId is invalid
 * 
 * @example
 * ```typescript
 * const score = await calculateScore(123);
 * // score = 85.5
 * 
 * const scoreWithBonus = await calculateScore(123, true);
 * // scoreWithBonus = 100.0
 * ```
 */
export async function calculateScore(
  userId: number,
  includeBonus: boolean = false
): Promise<number> {
  if (userId <= 0) {
    throw new Error('userId must be positive');
  }
  ...
}
```

### Architecture Decision Records (ADRs)

**ADR Template**
```markdown
# ADR-001: [Title of Decision]

**Status:** [Proposed | Accepted | Deprecated | Superseded]  
**Date:** YYYY-MM-DD  
**Deciders:** [List of people involved]  
**Technical Story:** [Link to issue/epic]

## Context

What is the issue we're seeing that is motivating this decision or change?

## Decision

What is the change we're proposing and/or doing?

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Drawback 1
- Drawback 2

### Risks
- Risk 1 (mitigation: ...)
- Risk 2 (mitigation: ...)

## Alternatives Considered

### Alternative 1
- Description
- Pros/Cons
- Why not chosen

### Alternative 2
- Description
- Pros/Cons
- Why not chosen

## References
- [Link 1]
- [Link 2]
```

**ADR File Naming**
```bash
docs/adr/
├── 001-use-react-for-frontend.md
├── 002-adopt-microservices-architecture.md
├── 003-choose-postgresql-for-database.md
└── template.md
```

---

## Testing Conventions

### Test File Organization

**Python Test Structure**
```python
# tests/test_user_service.py
"""Tests for user service module."""

import pytest
from myapp.services import UserService
from myapp.models import User


class TestUserService:
    """Test suite for UserService class."""
    
    @pytest.fixture
    def user_service(self):
        """Create a UserService instance for testing."""
        return UserService()
    
    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        return User(id=1, name="Test User", email="test@example.com")
    
    def test_get_user_by_id_returns_user_when_exists(
        self, user_service, sample_user
    ):
        """Test that get_user_by_id returns user when user exists."""
        # Arrange
        user_id = sample_user.id
        
        # Act
        result = user_service.get_user_by_id(user_id)
        
        # Assert
        assert result is not None
        assert result.id == user_id
    
    def test_get_user_by_id_returns_none_when_not_exists(self, user_service):
        """Test that get_user_by_id returns None when user doesn't exist."""
        # Arrange
        nonexistent_id = 9999
        
        # Act
        result = user_service.get_user_by_id(nonexistent_id)
        
        # Assert
        assert result is None
```

**TypeScript Test Structure**
```typescript
// tests/userService.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { UserService } from '../src/services/userService';
import { User } from '../src/models/user';

describe('UserService', () => {
  let userService: UserService;
  let sampleUser: User;

  beforeEach(() => {
    userService = new UserService();
    sampleUser = {
      id: 1,
      name: 'Test User',
      email: 'test@example.com'
    };
  });

  describe('getUserById', () => {
    it('should return user when user exists', async () => {
      // Arrange
      const userId = sampleUser.id;

      // Act
      const result = await userService.getUserById(userId);

      // Assert
      expect(result).toBeDefined();
      expect(result?.id).toBe(userId);
    });

    it('should return null when user does not exist', async () => {
      // Arrange
      const nonexistentId = 9999;

      // Act
      const result = await userService.getUserById(nonexistentId);

      // Assert
      expect(result).toBeNull();
    });
  });
});
```

### Test Naming Conventions

**Format**: `test_<function>_<scenario>_<expected_result>`

```python
# Good test names
test_get_user_by_id_returns_user_when_exists
test_get_user_by_id_returns_none_when_not_exists
test_create_user_raises_error_when_email_invalid
test_update_user_updates_modified_timestamp
test_delete_user_soft_deletes_when_has_dependencies

# Bad test names
test_user             # Not descriptive
test_get_user_1       # Number doesn't convey meaning
test_user_exists      # Unclear what's being tested
test_edge_case        # Which edge case?
```

### Test Organization Patterns

**AAA Pattern** (Arrange, Act, Assert)
```python
def test_calculate_score_includes_bonus_when_flag_true():
    # Arrange: Set up test data and dependencies
    user_id = 123
    base_score = 80.0
    bonus_points = 20.0
    include_bonus = True
    
    # Act: Execute the function under test
    result = calculate_score(user_id, include_bonus)
    
    # Assert: Verify the expected outcome
    assert result == base_score + bonus_points
```

**Given-When-Then Pattern** (BDD style)
```python
def test_user_authentication():
    # Given a user with valid credentials
    user = User(email="test@example.com", password="secure123")
    
    # When authenticating with correct password
    is_authenticated = authenticate_user(user.email, "secure123")
    
    # Then authentication succeeds
    assert is_authenticated is True
```

---

## Security Conventions

### Secret Management

**Environment Variables**
```bash
# Good: Use environment variables for secrets
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=sk_live_abc123xyz789
JWT_SECRET=randomly_generated_secret_key

# Bad: Never commit secrets to code
# config.py
DATABASE_URL = "postgresql://user:MyPassword123@localhost/db"  # ❌
API_KEY = "sk_live_abc123xyz789"  # ❌
```

**Secret Naming Convention**
```bash
# Format: <SERVICE>_<TYPE>_<ENVIRONMENT>

# Good examples
STRIPE_API_KEY_PRODUCTION
AWS_SECRET_ACCESS_KEY_STAGING
DATABASE_PASSWORD_DEV
GITHUB_TOKEN_CI

# Bad examples
key                    # Too vague
stripe_key            # Missing type and environment
MY_SECRET             # Not descriptive
```

### Authentication Conventions

**Token Storage**
```typescript
// Good: Store tokens securely
// - HttpOnly cookies for web apps
// - Secure storage for mobile apps
// - Never in localStorage for sensitive tokens

// Backend: Set HttpOnly cookie
response.cookie('auth_token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 3600000 // 1 hour
});

// Bad: Storing sensitive tokens in localStorage
localStorage.setItem('auth_token', token); // ❌ XSS vulnerability
```

**Password Policies**
```python
# Good: Strong password requirements
MIN_PASSWORD_LENGTH = 12
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True
REQUIRE_DIGIT = True
REQUIRE_SPECIAL_CHAR = True

# Use bcrypt or Argon2 for hashing
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
```

### Input Validation

**Always Validate External Input**
```python
# Good: Validate and sanitize
def create_user(email: str, name: str, age: int) -> User:
    # Validate email format
    if not is_valid_email(email):
        raise ValueError("Invalid email format")
    
    # Validate name length and characters
    if not (1 <= len(name) <= 100):
        raise ValueError("Name must be 1-100 characters")
    if not name.replace(" ", "").isalnum():
        raise ValueError("Name contains invalid characters")
    
    # Validate age range
    if not (0 <= age <= 150):
        raise ValueError("Age must be between 0 and 150")
    
    # Sanitize inputs
    email = email.strip().lower()
    name = name.strip()
    
    return User(email=email, name=name, age=age)

# Bad: No validation
def create_user(email, name, age):
    return User(email=email, name=name, age=age)  # ❌ Unsafe
```

---

## API Conventions

### REST API Conventions

**URL Structure**
```
# Resource-based URLs (nouns, not verbs)
GET    /api/v1/users              # List users
GET    /api/v1/users/{id}         # Get single user
POST   /api/v1/users              # Create user
PUT    /api/v1/users/{id}         # Update user (full)
PATCH  /api/v1/users/{id}         # Update user (partial)
DELETE /api/v1/users/{id}         # Delete user

# Nested resources
GET    /api/v1/users/{id}/posts   # User's posts
POST   /api/v1/users/{id}/posts   # Create post for user

# Bad examples
GET /api/v1/getUser?id=123        # ❌ Verb in URL
POST /api/v1/user-create          # ❌ Verb in URL
GET /api/v1/user_posts            # ❌ Unclear relationship
```

**HTTP Status Codes**
```
# Success responses
200 OK                  # Successful GET, PUT, PATCH
201 Created             # Successful POST
204 No Content          # Successful DELETE

# Client error responses
400 Bad Request         # Invalid request data
401 Unauthorized        # Missing or invalid authentication
403 Forbidden           # Authenticated but not authorized
404 Not Found           # Resource doesn't exist
409 Conflict            # Conflict with current state
422 Unprocessable Entity # Validation errors

# Server error responses
500 Internal Server Error # Unexpected server error
503 Service Unavailable   # Temporary unavailability
```

**Request/Response Format**
```json
// Good: Consistent JSON structure

// Success response
{
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2025-10-12T10:00:00Z",
    "version": "1.0"
  }
}

// Error response (RFC 7807)
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "Email address is required",
  "instance": "/users/123",
  "errors": [
    {
      "field": "email",
      "message": "Email address is required",
      "code": "required_field"
    }
  ]
}

// Pagination
{
  "data": [...],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 100,
    "totalPages": 5
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2",
    "last": "/users?page=5"
  }
}
```

### GraphQL Conventions

**Naming Conventions**
```graphql
# Good: Descriptive, consistent naming

type User {
  id: ID!
  firstName: String!
  lastName: String!
  email: String!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Query {
  user(id: ID!): User
  users(
    first: Int
    after: String
    filter: UserFilter
  ): UserConnection!
  currentUser: User
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
}

# Bad: Inconsistent, unclear
type User {
  user_id: ID!           # ❌ Use camelCase
  name: String!          # ❌ Unclear (firstName? fullName?)
  email_address: String! # ❌ Use camelCase
}
```

---

## Database Conventions

### Table Naming

**General Rules**
```sql
-- Good: Plural, snake_case
CREATE TABLE users (...);
CREATE TABLE order_items (...);
CREATE TABLE user_preferences (...);

-- Bad
CREATE TABLE User (...);         -- Mixed case
CREATE TABLE OrderItem (...);    -- Mixed case
CREATE TABLE user (...);         -- Singular
CREATE TABLE userpref (...);     -- Abbreviation
```

### Column Naming

**Consistent Patterns**
```sql
-- Good: snake_case, descriptive
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Bad
CREATE TABLE users (
    ID BIGINT PRIMARY KEY,          -- Mixed case
    Email VARCHAR(255),             -- Mixed case
    fname VARCHAR(100),             -- Abbreviation
    lname VARCHAR(100),             -- Abbreviation
    createdAt TIMESTAMP,            -- camelCase
    UpdatedAt TIMESTAMP             -- Mixed case
);
```

### Foreign Key Naming

**Format**: `<referenced_table_singular>_id`
```sql
-- Good
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Bad
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user BIGINT NOT NULL,           -- Missing _id suffix
    prod_id BIGINT NOT NULL,        -- Abbreviation
    product_fk BIGINT NOT NULL      -- Unclear naming
);
```

### Index Naming

**Format**: `idx_<table>_<column(s)>`
```sql
-- Good
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_last_name ON users(last_name);
CREATE INDEX idx_orders_user_id_created_at ON orders(user_id, created_at);

-- Bad
CREATE INDEX user_email ON users(email);  -- Missing idx_ prefix
CREATE INDEX index1 ON users(email);      -- Non-descriptive
```

---

## Configuration Conventions

### Environment Configuration

**Environment Naming**
```bash
# Standard environments
development   # Local development
staging       # Pre-production testing
production    # Live production

# Optional environments
test          # Automated testing
qa            # Quality assurance
demo          # Customer demos
```

**Configuration File Structure**
```
config/
├── default.yml          # Default configuration
├── development.yml      # Development overrides
├── staging.yml          # Staging overrides
├── production.yml       # Production overrides
└── test.yml            # Test overrides
```

### Feature Flags

**Flag Naming Convention**
```python
# Format: <component>_<feature>_<action>

# Good examples
FEATURE_USER_PROFILE_V2_ENABLED = True
FEATURE_PAYMENT_APPLE_PAY_ENABLED = False
FEATURE_SEARCH_ELASTIC_ROLLOUT_PERCENTAGE = 50

# Bad examples
NEW_FEATURE = True      # Not descriptive
FLAG1 = True           # Not descriptive
user_v2 = True         # Missing context
```

---

## Project Structure Conventions

### Python Project Structure
```
my-python-project/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── models/
│       ├── services/
│       ├── api/
│       └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
├── .github/
│   └── workflows/
├── pyproject.toml
├── requirements.txt
├── README.md
└── LICENSE
```

### Node.js Project Structure
```
my-node-project/
├── src/
│   ├── models/
│   ├── services/
│   ├── controllers/
│   ├── routes/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
├── .github/
│   └── workflows/
├── package.json
├── tsconfig.json
├── README.md
└── LICENSE
```

### Go Project Structure
```
my-go-project/
├── cmd/
│   └── app/
│       └── main.go
├── internal/
│   ├── models/
│   ├── services/
│   ├── handlers/
│   └── middleware/
├── pkg/
│   └── utils/
├── tests/
├── docs/
├── .github/
│   └── workflows/
├── go.mod
├── go.sum
├── README.md
└── LICENSE
```

---

## Communication Conventions

### Issue/Ticket Conventions

**Issue Title Format**
```
[<Type>] Brief description of issue

# Types:
[Bug]       # Something is broken
[Feature]   # New functionality
[Docs]      # Documentation issue
[Refactor]  # Code improvement
[Test]      # Testing issue
[Security]  # Security concern

# Good examples
[Bug] User email validation fails with plus signs
[Feature] Add OAuth2 authentication support
[Docs] Update API documentation for v2 endpoints
[Security] CSRF vulnerability in form submission

# Bad examples
Bug in code           # No brackets, not descriptive
Issue with login     # No type
Help needed          # Too vague
```

**Issue Description Template**
```markdown
## Description
Clear description of the issue

## Steps to Reproduce (for bugs)
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Browser: [e.g., Chrome 120]
- Version: [e.g., 1.2.3]

## Additional Context
Any other relevant information
```

### Code Review Conventions

**Review Comments Structure**
```markdown
# Blocking issues (must fix before merge)
❌ **[MUST FIX]** This will cause a security vulnerability
⚠️ **[REQUIRED]** Missing error handling for database operations

# Suggestions (nice to have)
💡 **[SUGGESTION]** Consider using a factory pattern here
📝 **[NITPICK]** Could improve naming clarity

# Questions
❓ **[QUESTION]** What happens if this value is null?

# Praise
✅ **[NICE]** Great test coverage!
👍 **[GOOD]** Clear and readable code
```

**Review Response Conventions**
```markdown
# Acknowledge and explain
✅ Fixed in [commit hash]
🔄 Refactored as suggested
📝 Added clarifying comment
❓ Good question! Here's why...
⚠️ Can't fix yet because [reason]. Created issue #123
```

---

## Appendix: Quick Reference

### Checklist for New Code

**Before Committing**
- [ ] Code follows style guide for the language
- [ ] All functions/classes documented
- [ ] Tests added/updated
- [ ] Tests pass locally
- [ ] Linter passes
- [ ] No secrets in code
- [ ] No commented-out code (remove or explain)
- [ ] Error handling appropriate
- [ ] Logging appropriate

**Before Opening PR**
- [ ] Branch name follows convention
- [ ] Commit messages follow conventional commits
- [ ] PR title and description clear
- [ ] PR size reasonable (< 400 lines)
- [ ] Documentation updated
- [ ] Screenshots added (for UI changes)
- [ ] Breaking changes documented
- [ ] Migration plan (if needed)

**During Code Review**
- [ ] Address all blocking comments
- [ ] Respond to all comments
- [ ] Update PR if needed
- [ ] Squash/rebase commits if needed
- [ ] Re-request review after changes

---

**Version History**

- **1.0.0** (2025-10-12): Initial comprehensive conventions document

---

**Maintained by**: Agentic Canon Contributors  
**Review Cycle**: Quarterly  
**Next Review**: 2026-01-12

---

*This document is part of the Agentic Canon framework for frontier software excellence.*
