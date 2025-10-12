# Development Tools

**Purpose:** Internal tools for maintaining and upgrading the Agentic Canon repository itself.

**⚠️ Important:** These tools are for **repository maintenance only**, not for end users.

## Directory Structure

```
.dev/
├── README.md                   # This file
├── scripts/                    # Development scripts
│   └── setup-labels.sh        # GitHub labels setup
├── validate-templates.sh       # Template validation
└── sanity-check.sh            # Repository sanity checks
```

## Tools

### validate-templates.sh
Validates all Cookiecutter templates for correctness:
- Checks cookiecutter.json syntax
- Validates hooks (pre_gen_project.py, post_gen_project.py)
- Verifies template structure

**Usage:**
```bash
.dev/validate-templates.sh
```

### sanity-check.sh
Runs comprehensive repository health checks:
- Verifies directory structure
- Checks documentation completeness
- Validates configuration files
- Tests CI/CD workflows

**Usage:**
```bash
.dev/sanity-check.sh
```

### scripts/setup-labels.sh
Sets up GitHub issue labels for the repository:
- Creates standard label set
- Configures colors and descriptions
- Requires GitHub CLI (gh) authentication

**Usage:**
```bash
.dev/scripts/setup-labels.sh
```

## Separation of Concerns

### Development Tools (.dev/)
**Internal use - for maintaining this repository:**
- Repository validation scripts
- CI/CD maintenance tools
- Label and issue management
- Health checks and diagnostics

### Distribution Assets (root level)
**External use - for end users:**
- `agentic_canon_cli/` - CLI wizard for project generation
- `templates/` - Cookiecutter templates and supporting files
- `notebooks/` - Executable guides
- `docs/` - Documentation
- `examples/` - Reference implementations

## Contributing

When adding new development tools:
1. Place them in `.dev/` or `.dev/scripts/`
2. Make scripts executable: `chmod +x script-name.sh`
3. Add documentation to this README
4. Update DIRECTORY_STRUCTURE.md if structure changes

## Related Documentation

- [DIRECTORY_STRUCTURE.md](../DIRECTORY_STRUCTURE.md) - Complete repository structure
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [FRAMEWORK.md](../FRAMEWORK.md) - Framework and philosophy
