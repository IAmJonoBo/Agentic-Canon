package featureflags

import (
	context "context"
	"os"

	flagd "github.com/open-feature/flagd-go/pkg/flagd"
	"github.com/open-feature/go-sdk/pkg/openfeature"
)

var (
	host   = getenv("FLAGD_HOST", "localhost")
	port   = getenv("FLAGD_PORT", "8013")
	client *openfeature.Client
)

func getenv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func getClient() *openfeature.Client {
	if client != nil {
		return client
	}

	provider := flagd.NewProvider(flagd.WithHost(host), flagd.WithPort(port))
	openfeature.SetProvider(provider)
	client = openfeature.NewClient("agentic-canon")
	return client
}

// Bool retrieves a boolean feature flag, returning the default if evaluation fails.
func Bool(ctx context.Context, flagKey string, defaultValue bool) bool {
	value, err := getClient().BooleanValue(ctx, flagKey, defaultValue, openfeature.EvaluationContext{})
	if err != nil {
		return defaultValue
	}
	return value
}
