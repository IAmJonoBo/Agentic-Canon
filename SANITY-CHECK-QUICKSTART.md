# Quick Start Guide - Enhanced Sanity Check

## Overview

The enhanced sanity check script provides comprehensive validation of the Agentic Canon project with 140 automated checks covering 24 categories.

## Quick Usage

### Run Sanity Check

```bash
./sanity-check.sh
```

**Expected Output:**
```
🔍 Agentic Canon - Comprehensive Sanity Check
==============================================

📚 Checking Core Documentation...
  ✅ README.md exists
  ✅ TASKS.md exists
  ...

==============================================
📊 Sanity Check Summary
==============================================
  ✅ Passed: 140
  ⚠️  Warnings: 3
  ❌ Failed: 0

🎉 All critical checks passed!
```

### Run Tests

```bash
# All tests
pytest tests/ -v

# Sanity check tests only
pytest tests/test_sanity_check.py -v

# Quick test run
pytest tests/ -q
```

## What Gets Checked?

### 1. Documentation (14 checks)
- ✅ Core docs (README, LICENSE, CHANGELOG)
- ✅ Framework docs (FRAMEWORK.md, QUALITY_STANDARDS.md, CONVENTIONS.md)
- ✅ Completeness validation (8 critical files)

### 2. Code Quality (26 checks)
- ✅ Python syntax validation (11 hook files)
- ✅ Shell script syntax validation (2+ scripts)
- ✅ Python hook import validation
- ✅ Executable permissions

### 3. Configuration Files (26 checks)
- ✅ JSON validation (10+ files)
- ✅ YAML validation (10 files)
- ✅ Pre-commit config validation
- ✅ Requirements files validation

### 4. Templates (59 checks)
- ✅ 5 primary templates
- ✅ 8 additional template categories
- ✅ Template structure compliance
- ✅ README.md documentation
- ✅ Hooks directory presence
- ✅ Project structure validation

### 5. Examples & Projects (15 checks)
- ✅ 4 example project docs
- ✅ Naming conventions
- ✅ 4 Grafana dashboards
- ✅ 6 video tutorial scripts

### 6. Infrastructure (15 checks)
- ✅ Azure Pipelines support
- ✅ CLI wizard structure
- ✅ Test infrastructure
- ✅ Multi-cloud support
- ✅ Advanced features

### 7. CI/CD (11 checks)
- ✅ GitHub Actions workflows
- ✅ Workflow structure validation
- ✅ Required keys verification

### 8. Repository Health (8 checks)
- ✅ Broken symlinks detection
- ✅ File size sanity checks
- ✅ Shared validation module

## Understanding Results

### Exit Codes
- `0` = Success (all critical checks passed)
- `1` = Failure (one or more critical checks failed)

### Status Icons
- ✅ **Green checkmark** = Test passed
- ⚠️ **Yellow warning** = Non-critical issue
- ❌ **Red X** = Critical failure

### Warning Examples
```
⚠️  azure examples missing          # Expected - work in progress
⚠️  pre-commit not installed        # Informational only
⚠️  Large file detected: data.json  # Potential issue
```

### Failure Examples
```
❌ README.md missing                 # Critical - must fix
❌ Template tests missing            # Critical - must fix
❌ syntax_error.py has syntax errors # Critical - must fix
```

## Common Scenarios

### Scenario 1: Clean Repository
```bash
./sanity-check.sh
# Expected: ✅ 140 passed, ⚠️ 3 warnings, ❌ 0 failed
```

### Scenario 2: After Adding New Template
```bash
./sanity-check.sh
# Check for:
# - Template structure compliance
# - README.md presence
# - Hook syntax validation
# - cookiecutter.json validity
```

### Scenario 3: Before Committing Changes
```bash
# 1. Run sanity check
./sanity-check.sh

# 2. Run tests
pytest tests/ -v

# 3. Both should pass before committing
```

### Scenario 4: CI/CD Pipeline
```yaml
# In .github/workflows/ci.yml
- name: Run sanity check
  run: ./sanity-check.sh
  
- name: Run tests
  run: pytest tests/ -v
```

## Troubleshooting

### Issue: Shell script syntax errors
```bash
# Fix:
bash -n script.sh  # Check syntax
# Then fix errors and run sanity check again
```

### Issue: Python hook import errors
```bash
# Fix:
python -m py_compile templates/*/hooks/*.py
# Fix import errors, then run sanity check
```

### Issue: Invalid JSON/YAML
```bash
# Fix JSON:
python -m json.tool file.json

# Fix YAML:
python -c "import yaml; yaml.safe_load(open('file.yml'))"
```

### Issue: Broken symlinks
```bash
# Find broken symlinks:
find . -type l ! -exec test -e {} \; -print

# Fix or remove them, then run sanity check
```

## Best Practices

### For Developers
1. ✅ Run sanity check before committing
2. ✅ Fix all failures immediately
3. ✅ Investigate warnings (may become failures)
4. ✅ Keep checks passing at all times

### For CI/CD
1. ✅ Run sanity check as first job
2. ✅ Fail fast on errors
3. ✅ Cache dependencies for speed
4. ✅ Report results clearly

### For Maintainers
1. ✅ Review sanity check output regularly
2. ✅ Add new checks as needed
3. ✅ Update documentation when adding checks
4. ✅ Keep tests in sync with checks

## Performance Tips

### Fast Mode (Skip Tests)
```bash
# Only run checks, skip test execution
grep -v "pytest" sanity-check.sh | bash
```

### Parallel Execution (Future)
```bash
# Not yet implemented, but possible:
./sanity-check.sh --parallel
```

### Specific Category
```bash
# Run only specific checks (manual filtering)
./sanity-check.sh 2>&1 | grep -A 10 "Checking Templates"
```

## Integration Examples

### Pre-commit Hook
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: sanity-check
        name: Run sanity check
        entry: ./sanity-check.sh
        language: system
        pass_filenames: false
```

### GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  sanity-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run sanity check
        run: ./sanity-check.sh
```

### Make Target
```makefile
# Makefile
.PHONY: sanity-check
sanity-check:
	@./sanity-check.sh

.PHONY: test
test:
	@pytest tests/ -v

.PHONY: check
check: sanity-check test
```

## Advanced Usage

### Verbose Mode
```bash
# Already verbose by default
./sanity-check.sh
```

### Capture Output
```bash
# Save to file
./sanity-check.sh 2>&1 | tee sanity-check-results.txt

# Save only summary
./sanity-check.sh 2>&1 | tail -30 > summary.txt
```

### Check Specific Components
```bash
# Templates only
./sanity-check.sh 2>&1 | grep -A 50 "Checking Cookiecutter Templates"

# Documentation only
./sanity-check.sh 2>&1 | grep -A 20 "Checking Core Documentation"

# Tests only
./sanity-check.sh 2>&1 | grep -A 10 "Checking Test Infrastructure"
```

## Maintenance

### Adding New Checks
1. Edit `sanity-check.sh`
2. Add check in appropriate section
3. Use `check_pass`, `check_warn`, or `check_fail`
4. Test thoroughly
5. Add tests in `tests/test_sanity_check.py`
6. Update documentation

### Updating Documentation
1. `TASKS.md` - Update check count and categories
2. `SANITY-CHECK-ENHANCEMENTS.md` - Add new features
3. `tests/README.md` - Document new tests
4. This file - Update usage examples

## Resources

### Documentation
- `SANITY-CHECK-ENHANCEMENTS.md` - Detailed technical summary
- `SANITY-CHECK-COMPARISON.md` - Before/after comparison
- `TASKS.md` - Implementation status
- `tests/README.md` - Test documentation

### Related Scripts
- `sanity-check.sh` - Main validation script
- `validate-templates.sh` - Template-specific validation
- `tests/test_sanity_check.py` - Test suite

### Standards References
- `FRAMEWORK.md` - Framework standards
- `QUALITY_STANDARDS.md` - Quality requirements
- `CONVENTIONS.md` - Development conventions

## Support

### Getting Help
1. Check error messages (they include solutions)
2. Review relevant documentation
3. Check tests for examples
4. Create GitHub issue if needed

### Reporting Issues
Include:
- Sanity check output
- Error messages
- Steps to reproduce
- Expected vs actual behavior

---

**Quick Reference:**
```bash
# Run checks
./sanity-check.sh

# Run tests
pytest tests/ -v

# Both
./sanity-check.sh && pytest tests/ -v
```

**Status:** ✅ 140 checks passing, 28 tests passing, ready for production use
