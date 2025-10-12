package jwt

import (
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var (
	errMissingSecret = errors.New("jwt: signing secret not configured")
)

// SignToken issues a short-lived JWT suitable for auth demos.
func SignToken(userID, email, secret string, ttl time.Duration) (string, error) {
	if secret == "" {
		return "", errMissingSecret
	}

	claims := jwt.RegisteredClaims{
		Subject:   userID,
		IssuedAt:  jwt.NewNumericDate(time.Now()),
		ExpiresAt: jwt.NewNumericDate(time.Now().Add(ttl)),
	}
	if email != "" {
		claims.Audience = jwt.ClaimStrings{email}
	}

	tok := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return tok.SignedString([]byte(secret))
}
