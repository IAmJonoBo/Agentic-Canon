# Development Scripts

This directory contains utility scripts for development, automation, and maintenance tasks.

## Available Scripts

### ADR Management

#### `create-adr.sh`

Interactive script for creating Architecture Decision Records.

**Usage:**

```bash
.dev/scripts/create-adr.sh
```

**Features:**

- Automatically numbers ADRs sequentially
- Creates file from template
- Prompts for metadata (title, status, decision makers)
- Opens in editor when complete

**Example:**

```bash
$ .dev/scripts/create-adr.sh

=== ADR Creation Wizard ===

Next ADR Number: 009

Enter ADR title: Use PostgreSQL for primary database
Select status: 1) proposed
Enter decision makers: John Doe - Tech Lead, Jane Smith - Architect
Enter brief problem statement: Need reliable ACID-compliant database

✓ ADR created: docs/adr/ADR-009-use-postgresql-for-primary-database.md
```

See [ADR Lifecycle Guide](../../docs/adr/ADR-LIFECYCLE.md) for more details.

## Adding New Scripts

When adding scripts to this directory:

1. **Make executable:**

   ```bash
   chmod +x .dev/scripts/your-script.sh
   ```

2. **Add shebang:**

   ```bash
   #!/bin/bash
   ```

3. **Include help:**

   ```bash
   # Script Name
   # Description of what it does
   # Usage: ./your-script.sh [options]
   ```

4. **Document here:**
   Add entry to this README with:
   - Purpose
   - Usage example
   - Options/arguments
   - Related documentation

5. **Follow conventions:**
   - Use descriptive names
   - Add error handling
   - Include status messages
   - Exit with appropriate codes

## Script Conventions

### Exit Codes

- `0` - Success
- `1` - General error
- `2` - Invalid arguments
- `3` - Missing dependencies

### Output Formatting

Use colored output for clarity:

```bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}✓ Success${NC}"
echo -e "${RED}✗ Error${NC}"
echo -e "${YELLOW}⚠ Warning${NC}"
```

### Error Handling

```bash
set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure
```

## Related Documentation

- [ADR Lifecycle](../../docs/adr/ADR-LIFECYCLE.md)
- [Issue Management](../../docs/ISSUE_MANAGEMENT.md)
- [Contributing Guide](../../CONTRIBUTING.md)
- [Development Workflows](.github/workflows/)
