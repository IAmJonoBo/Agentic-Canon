# Feature Flag Starter Kit (OpenFeature + flagd)

This folder contains language-specific helpers you can copy into generated
projects to enable feature flags without altering the upstream n00-frontiers
templates.

## Provided Libraries

| Language   | Location                          | Description                                             |
| ---------- | --------------------------------- | ------------------------------------------------------- |
| Python     | `python/feature_flags.py`         | Minimal OpenFeature bootstrap with flagd provider       |
| TypeScript | `typescript/featureFlags.ts`      | Vite/Node compatible helper that bootstraps OpenFeature |
| Go         | `go/featureflags/featureflags.go` | Go helper returning typed evaluation methods            |

### Usage Pattern

1. Copy the relevant language directory into your project (e.g.
   `cp -r templates/_shared/feature_flags/python src/feature_flags`).
2. Install the OpenFeature SDK + flagd provider for your language (see table below).
3. Import the helper and use the `get_flag`/`Evaluate` functions to wrap feature
   toggles around new functionality.
4. Run flagd locally or point to your existing flagd deployment.

| Language   | Install Command                                                                                |
| ---------- | ---------------------------------------------------------------------------------------------- |
| Python     | `pip install openfeature-sdk flagd-openfeature-provider`                                       |
| TypeScript | `npm install @openfeature/js-sdk @openfeature/flagd-provider`                                  |
| Go         | `go get github.com/open-feature/go-sdk`<br>`go get github.com/open-feature/flagd-go/pkg/flagd` |

Each helper configures sensible defaults:

- Automatic connection to a local `flagd` instance (`localhost:8013`) with room
  to override via environment variables.
- Graceful fallbacks when the provider is unavailable (returns default values).
- Structured logging to surface flag evaluation errors.

## flagd Quickstart

```bash
docker run -it --rm \
  -p 8013:8013 \
  ghcr.io/open-feature/flagd:latest \
  start \
    --uri https://raw.githubusercontent.com/open-feature/flagd/main/examples/simple-flags.json
```

## Suggested Workflow

1. Add the helper files to your project repo.
2. Configure a CI check to ensure feature flag schemas stay valid.
3. Surface the active flag list in documentation or Backstage (see
   `docs/dev-experience-roadmap.md`).
4. Re-run `agentic-canon fix` to confirm your environment can evaluate flags
   locally with the new dependencies.
