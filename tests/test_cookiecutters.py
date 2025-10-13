"""Tests for Cookiecutter templates."""


def test_python_cookiecutter_bakes(bake_template):
    """Test that the Python service template renders successfully."""
    result = bake_template(
        "templates/python-service",
        {
            "project_name": "Demo Service",
            "project_slug": "demo-service",
            "pkg_name": "demo_service",
            "project_description": "A demo Python service",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "license": "Apache-2.0",
            "python_version": "3.11",
            "include_jupyter_book": "yes",
            "enable_security_gates": "yes",
            "enable_sbom_signing": "yes",
            "enable_contract_tests": "yes",
            "ci_provider": "github",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()

    # Check essential files exist
    assert (result.project_path / "pyproject.toml").exists()
    assert (result.project_path / "README.md").exists()
    assert (result.project_path / "src" / "demo_service" / "__init__.py").exists()
    assert (result.project_path / "tests" / "test_smoke.py").exists()
    assert (result.project_path / ".github" / "workflows" / "ci.yml").exists()


def test_python_cookiecutter_minimal(bake_template):
    """Test Python template with minimal options."""
    result = bake_template(
        "templates/python-service",
        {
            "project_name": "Minimal Service",
            "project_slug": "minimal-service",
            "pkg_name": "minimal_service",
            "license": "MIT",
            "include_jupyter_book": "no",
            "enable_security_gates": "no",
            "enable_sbom_signing": "no",
            "enable_contract_tests": "no",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0

    # Security workflow should not exist when disabled
    assert not (result.project_path / ".github" / "workflows" / "security.yml").exists()

    # Docs should not exist when Jupyter Book is disabled
    assert not (result.project_path / "docs" / "_config.yml").exists()


def test_python_cookiecutter_invalid_slug(cookies):
    """Test that invalid project_slug is rejected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "Invalid_Slug",  # Underscores not allowed
            "pkg_name": "invalid_service",
        },
        template="templates/python-service",
    )

    # Should fail validation
    assert result.exit_code != 0


def test_node_cookiecutter_bakes(bake_template):
    """Test that the Node.js service template renders successfully."""
    result = bake_template(
        "templates/node-service",
        {
            "project_name": "Demo Node Service",
            "project_slug": "demo-node-service",
            "description": "A demo Node.js service",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "license": "Apache-2.0",
            "node_version": "20",
            "enable_security_gates": "yes",
            "enable_sbom_signing": "yes",
            "ci_provider": "github",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()

    # Check essential files exist
    assert (result.project_path / "package.json").exists()
    assert (result.project_path / "tsconfig.json").exists()
    assert (result.project_path / "src" / "index.ts").exists()
    assert (result.project_path / "tests" / "smoke.test.ts").exists()
    assert (result.project_path / ".github" / "workflows" / "ci.yml").exists()


def test_react_cookiecutter_bakes(bake_template):
    """Test that the React webapp template renders successfully."""
    result = bake_template(
        "templates/react-webapp",
        {
            "project_name": "Demo React App",
            "project_slug": "demo-react-app",
            "description": "A demo React application",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "license": "MIT",
            "include_storybook": "yes",
            "include_e2e_tests": "yes",
            "enable_accessibility_tests": "yes",
            "ci_provider": "github",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()

    # Check essential files exist
    assert (result.project_path / "package.json").exists()
    assert (result.project_path / "vite.config.ts").exists()
    assert (result.project_path / "src" / "App.tsx").exists()
    assert (result.project_path / "src" / "components" / "Button.tsx").exists()
    assert (result.project_path / ".storybook" / "main.ts").exists()
    assert (result.project_path / "playwright.config.ts").exists()
    assert (result.project_path / ".github" / "workflows" / "ci.yml").exists()


def test_react_cookiecutter_minimal(bake_template):
    """Test React template with minimal options."""
    result = bake_template(
        "templates/react-webapp",
        {
            "project_name": "Minimal React App",
            "project_slug": "minimal-react-app",
            "include_storybook": "no",
            "include_e2e_tests": "no",
            "enable_accessibility_tests": "no",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0

    # Storybook and E2E should not exist when disabled
    assert not (result.project_path / ".storybook").exists()
    assert not (result.project_path / "playwright.config.ts").exists()


def test_go_cookiecutter_bakes(bake_template):
    """Test that the Go service template renders successfully."""
    result = bake_template(
        "templates/go-service",
        {
            "project_name": "Demo Go Service",
            "project_slug": "demo-go-service",
            "module_path": "github.com/test/demo-go-service",
            "description": "A demo Go service",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "license": "Apache-2.0",
            "go_version": "1.22",
            "enable_security_gates": "yes",
            "ci_provider": "github",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()

    # Check essential files exist
    assert (result.project_path / "go.mod").exists()
    assert (result.project_path / "Makefile").exists()
    assert (result.project_path / "cmd" / "app" / "main.go").exists()
    assert (result.project_path / "internal" / "app" / "app.go").exists()
    assert (result.project_path / "internal" / "app" / "app_test.go").exists()
    assert (result.project_path / ".golangci.yml").exists()
    assert (result.project_path / ".github" / "workflows" / "ci.yml").exists()


def test_docs_only_cookiecutter_bakes(bake_template):
    """Test that the docs-only template renders successfully."""
    result = bake_template(
        "templates/docs-only",
        {
            "project_name": "Demo Documentation",
            "project_slug": "demo-docs",
            "description": "Demo documentation project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "license": "CC-BY-4.0",
            "ci_provider": "github",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()

    # Check essential files exist
    assert (result.project_path / "docs" / "_config.yml").exists()
    assert (result.project_path / "docs" / "_toc.yml").exists()
    assert (result.project_path / "docs" / "index.md").exists()
    assert (result.project_path / "requirements.txt").exists()
    assert (result.project_path / ".github" / "workflows" / "book-deploy.yml").exists()


# ============================================================================
# Enhanced Validation Tests
# ============================================================================


def test_python_invalid_email(cookies):
    """Test that invalid email is rejected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-service",
            "pkg_name": "test_service",
            "author_email": "not-an-email",  # Invalid email
            "project_description": "A test service for validation",
        },
        template="templates/python-service",
    )
    assert result.exit_code != 0


def test_python_invalid_author_name(cookies):
    """Test that invalid author name is rejected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-service",
            "pkg_name": "test_service",
            "author_name": "X",  # Too short
            "project_description": "A test service for validation",
        },
        template="templates/python-service",
    )
    assert result.exit_code != 0


def test_python_invalid_license(cookies):
    """Test that invalid license is rejected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-service",
            "pkg_name": "test_service",
            "license": "InvalidLicense",  # Not in approved list
            "project_description": "A test service for validation",
        },
        template="templates/python-service",
    )
    assert result.exit_code != 0


def test_python_short_description(cookies):
    """Test that too short description is rejected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-service",
            "pkg_name": "test_service",
            "project_description": "Short",  # Less than 10 characters
        },
        template="templates/python-service",
    )
    assert result.exit_code != 0


def test_python_reserved_keyword_package_name(cookies):
    """Test that Python reserved keyword is rejected for package name."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-service",
            "pkg_name": "import",  # Reserved keyword
            "project_description": "A test service for validation",
        },
        template="templates/python-service",
    )
    assert result.exit_code != 0


def test_node_invalid_email(cookies):
    """Test that Node template rejects invalid email."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-node",
            "author_email": "invalid.email",
            "description": "A test Node.js service",
        },
        template="templates/node-service",
    )
    assert result.exit_code != 0


def test_react_invalid_slug(cookies):
    """Test that React template rejects invalid slug."""
    result = cookies.bake(
        extra_context={
            "project_slug": "Invalid-App_Name",
            "description": "A test React application",
        },
        template="templates/react-webapp",
    )
    assert result.exit_code != 0


def test_go_invalid_module_path(cookies):
    """Test that Go template rejects invalid module path."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-go",
            "module_path": "invalid-path",  # Must have domain/path
            "description": "A test Go service",
        },
        template="templates/go-service",
    )
    assert result.exit_code != 0


def test_docs_only_invalid_description(cookies):
    """Test that docs template rejects too short description."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-docs",
            "description": "Short",  # Too short
        },
        template="templates/docs-only",
    )
    assert result.exit_code != 0


def test_project_management_bakes(bake_template):
    """Test that the project management template renders successfully."""
    result = bake_template(
        "templates/project-management",
        {
            "project_name": "My Project",
            "project_slug": "my-project",
            "github_org": "my-org",
            "project_description": "A well-managed project",
            "enable_todo_tracking": "yes",
            "enable_tasklist_tracking": "yes",
            "enable_pr_followups": "yes",
            "enable_issue_triage": "yes",
            "enable_projects_board": "yes",
            "enable_branch_protection": "yes",
            "enable_codeowners": "yes",
            "default_branch": "main",
            "require_approvals": "2",
            "auto_close_stale_issues": "yes",
            "stale_days": "60",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()

    # Check essential files exist
    assert (result.project_path / "README.md").exists()
    assert (result.project_path / "PROJECT_MANAGEMENT.md").exists()
    assert (result.project_path / "TASKS.md").exists()
    assert (result.project_path / ".github" / "workflows" / "todos.yml").exists()
    assert (result.project_path / ".github" / "workflows" / "tasklist-scan.yml").exists()
    assert (result.project_path / ".github" / "workflows" / "pr-review-followup.yml").exists()
    assert (result.project_path / ".github" / "workflows" / "issue-triage.yml").exists()
    assert (result.project_path / ".github" / "workflows" / "stale.yml").exists()
    assert (result.project_path / ".github" / "CODEOWNERS").exists()
    assert (result.project_path / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").exists()
    assert (result.project_path / ".github" / "ISSUE_TEMPLATE" / "feature_request.md").exists()
    assert (result.project_path / ".github" / "ISSUE_TEMPLATE" / "task.md").exists()
    assert (result.project_path / ".github" / "PULL_REQUEST_TEMPLATE.md").exists()


def test_project_management_minimal(bake_template):
    """Test project management template with minimal options."""
    result = bake_template(
        "templates/project-management",
        {
            "project_name": "Minimal Project",
            "project_slug": "minimal-project",
            "github_org": "test-org",
            "enable_todo_tracking": "yes",
            "enable_tasklist_tracking": "no",
            "enable_pr_followups": "no",
            "enable_issue_triage": "no",
            "enable_codeowners": "no",
            "auto_close_stale_issues": "no",
        },
    )

    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()

    # Only todos.yml should have content
    todos_content = (result.project_path / ".github" / "workflows" / "todos.yml").read_text()
    assert "TODO" in todos_content

    # Other workflows should be empty or not generated
    tasklist_file = result.project_path / ".github" / "workflows" / "tasklist-scan.yml"
    if tasklist_file.exists():
        content = tasklist_file.read_text().strip()
        assert not content or content == ""


def test_project_management_invalid_slug(cookies):
    """Test that project management template rejects invalid slug."""
    result = cookies.bake(
        extra_context={
            "project_slug": "Invalid_Slug",
            "github_org": "test-org",
        },
        template="templates/project-management",
    )
    assert result.exit_code != 0


def test_project_management_invalid_org(cookies):
    """Test that project management template rejects invalid org name."""
    result = cookies.bake(
        extra_context={
            "project_slug": "test-project",
            "github_org": "invalid org name",
        },
        template="templates/project-management",
    )
    assert result.exit_code != 0
