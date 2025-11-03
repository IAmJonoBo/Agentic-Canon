# Feature Flags with OpenFeature + flagd

This guide explains how to adopt feature flags across Agentic Canon projects
without modifying the cookiecutter templates directly.

## Shared Starter Kit

Reusable helpers live in `templates/_shared/feature_flags/`:

| Language   | Path                              | Notes                                   |
| ---------- | --------------------------------- | --------------------------------------- |
| Python     | `python/feature_flags.py`         | Requires `openfeature-sdk` + flagd      |
| TypeScript | `typescript/featureFlags.ts`      | Works with Vite/Node, uses async client |
| Go         | `go/featureflags/featureflags.go` | Simple package returning boolean flags  |

### Quick Steps

1. Copy the relevant language helper into your project:

   ```bash
   cp -r templates/_shared/feature_flags/python src/feature_flags
   ```

2. Install the OpenFeature SDK and flagd provider (see table below).
3. Import the helper and wrap new functionality in flag checks.
4. Run flagd locally (`docker run ghcr.io/open-feature/flagd:latest ...`) or point
   to your managed deployment.

| Language   | Install Command                                                                               |
| ---------- | --------------------------------------------------------------------------------------------- |
| Python     | `pip install openfeature-sdk flagd-openfeature-provider`                                      |
| TypeScript | `npm install @openfeature/js-sdk @openfeature/flagd-provider`                                 |
| Go         | `go get github.com/open-feature/go-sdk` + `go get github.com/open-feature/flagd-go/pkg/flagd` |

Example (Python):

```python
from feature_flags import feature_flags

if feature_flags.get_boolean("new-dashboard", default=False):
    enable_new_dashboard()
```

Example (TypeScript):

```ts
import { getBoolean } from "./featureFlags";

if (await getBoolean("new-dashboard")) {
  enableNewDashboard();
}
```

Example (Go):

```go
if featureflags.Bool(ctx, "new-dashboard", false) {
    enableNewDashboard()
}
```

## Local flagd

To experiment locally:

```bash
docker run -it --rm \
  -p 8013:8013 \
  ghcr.io/open-feature/flagd:latest \
  start \
    --uri https://raw.githubusercontent.com/open-feature/flagd/main/examples/simple-flags.json
```

## Best Practices

- Keep flag names consistent across environments.
- Store default values in code to ensure safe fallbacks when the provider is
  unavailable.
- Surface active flags and their purpose in project documentation or the
  Backstage portal.
- Include flag evaluation in integration tests to guard against configuration
  drift.

For roadmap context see `docs/dev-experience-roadmap.md` (#131).
