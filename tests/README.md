# Tests

This directory contains tests for the Agentic Canon project.

## Overview

Tests ensure the quality and correctness of:
- Cookiecutter template rendering
- Template generation hooks
- Example configurations
- Integration workflows

## Test Structure

### test_cookiecutters.py
Tests for Cookiecutter templates using pytest-cookies.

**Tests**:
- Template rendering for all templates
- Variable validation
- Hook execution
- Generated project structure

**Usage**:
```bash
pytest tests/test_cookiecutters.py -v
```

### test_sanity_check.py
Tests for the sanity check script (`sanity-check.sh`).

**Tests**:
- Script existence and executability
- Successful execution with zero failures
- Core documentation validation
- Template validation
- Python syntax validation
- JSON/YAML validation
- Shell script validation
- GitHub Actions workflow validation
- Check count verification (>=135)

**Usage**:
```bash
pytest tests/test_sanity_check.py -v
```

**Test Count:** 11 tests covering all major sanity check categories

## Running Tests

### All Tests

```bash
# Run all tests
pytest tests/

# With verbose output
pytest tests/ -v

# With coverage
pytest tests/ --cov
```

### Specific Tests

```bash
# Test specific file
pytest tests/test_cookiecutters.py

# Test specific template
pytest tests/test_cookiecutters.py -k python

# Test with markers
pytest tests/ -m unit
```

### Template Rendering Tests

```bash
# Test all template rendering
pytest tests/test_cookiecutters.py

# Test specific template
pytest tests/test_cookiecutters.py::test_python_service_template
```

## Test Categories

### Unit Tests
Test individual components in isolation.

**Examples**:
- Template variable validation
- Hook function testing
- Utility function testing

### Integration Tests
Test template generation end-to-end.

**Examples**:
- Full template rendering
- Generated project validation
- CI workflow execution

### Template Tests
Verify template correctness using pytest-cookies.

**Examples**:
- Template renders successfully
- Required files are generated
- Configuration files are valid
- Hooks execute correctly

## Writing Tests

### Test Template Example

```python
def test_python_service_template(cookies):
    """Test Python service template renders correctly."""
    result = cookies.bake(
        extra_context={
            'project_name': 'Test Project',
            'project_slug': 'test-project'
        },
        template='templates/python-service'
    )
    
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
    assert (result.project_path / 'pyproject.toml').is_file()
```

### Best Practices

1. **Clear Names**: Use descriptive test names
2. **Arrange-Act-Assert**: Follow AAA pattern
3. **Isolation**: Tests should be independent
4. **Coverage**: Aim for high code coverage
5. **Speed**: Keep tests fast
6. **Documentation**: Add docstrings to tests

## Test Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests
    integration: Integration tests
    template: Template tests
```

### Coverage Configuration

```ini
[coverage:run]
source = .
omit =
    tests/*
    .venv/*
    */site-packages/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## Continuous Integration

Tests run automatically on:
- Every pull request
- Every push to main
- Scheduled runs (daily)

See `.github/workflows/cookiecutters-test.yml`

## Dependencies

Test dependencies are in `requirements.txt`:
- pytest - Testing framework
- pytest-cookies - Cookiecutter testing
- pytest-cov - Coverage reporting

Install with:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### Tests Failing Locally

1. Update dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. Clear cache:
   ```bash
   pytest --cache-clear
   ```

3. Run with verbose output:
   ```bash
   pytest -vv
   ```

### Template Rendering Fails

1. Check template syntax
2. Verify cookiecutter.json is valid
3. Test hooks independently
4. Check file permissions

### Import Errors

```bash
# Ensure package is installed
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

## Contributing

When adding new functionality:

1. Write tests first (TDD)
2. Ensure tests pass
3. Aim for >80% coverage
4. Document test cases
5. Include in PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## Test Metrics

Target metrics:
- **Coverage**: ≥80%
- **Mutation Score**: ≥70%
- **Execution Time**: <5 minutes
- **Flakiness**: 0%

## Future Tests

Planned test additions per [TASKS.md](../TASKS.md):

- [ ] Integration tests for workflow orchestration
- [ ] E2E tests for generated projects
- [ ] Contract tests between services
- [ ] Performance testing framework
- [ ] Security testing (SAST, DAST)

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cookies Documentation](https://pytest-cookies.readthedocs.io/)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)

## Related

- [Templates](../templates/) - What we're testing
- [CI Workflows](../.github/workflows/) - Where tests run
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute tests

---

For questions about testing, open an issue or discussion in the repository.
