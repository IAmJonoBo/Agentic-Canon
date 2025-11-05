# Getting Started with Agentic Canon

**Duration:** 5-7 minutes  
**Target Audience:** Developers new to Agentic Canon  
**Prerequisites:** Basic Git and Python knowledge

---

## Script Outline

### Introduction (30 seconds)

**[Screen: Agentic Canon README on GitHub]**

"Welcome to Agentic Canon - the machine-readable, agent-friendly project scaffolding framework. In this tutorial, we'll walk through getting started with Agentic Canon and create your first production-ready project in just a few minutes."

**Key Points to Cover:**

- What is Agentic Canon?
- Why use it?
- What you'll learn today

---

### What is Agentic Canon? (1 minute)

**[Screen: Diagram or slides showing architecture]**

"Agentic Canon is a comprehensive scaffolding framework that helps you create production-ready projects with:

- Built-in security best practices
- Automated testing and CI/CD
- Observability and monitoring
- Quality gates
- Standards compliance"

**Show:**

- DORA metrics dashboard
- Security scanning workflow
- Quality metrics

**Benefits:**

- Save time on project setup
- Enforce best practices automatically
- Meet compliance requirements out-of-the-box
- Agent-friendly for AI-assisted development

---

### Installation (1 minute)

**[Screen: Terminal]**

"Let's get started by installing Agentic Canon. First, make sure you have Python 3.11 or higher installed."

```bash
# Check Python version
python --version

# Clone the repository
git clone https://github.com/IAmJonoBo/Agentic-Canon.git
cd Agentic-Canon

# Install the CLI tool
pip install -e .

# Verify installation
agentic-canon --version
```

**Narrate each command and explain what it does.**

---

### Creating Your First Project (2-3 minutes)

**[Screen: Terminal with split view - commands on left, file explorer on right]**

"Now let's create our first project. We'll use the interactive CLI wizard which makes it super easy."

```bash
# Start the wizard
agentic-canon init
```

**Walk through each prompt:**

1. **Template Selection**
   - "Let's choose 'Python Service' for this demo"
   - Briefly mention other options (Node, React, Go, Docs)

2. **Project Details**
   - Project name: "my-awesome-api"
   - Description: "A production-ready API service"
   - Author name and email

3. **Features Selection**
   - Enable Jupyter Book docs: Yes
   - Security scanning: Yes
   - SBOM generation: Yes
   - Contract testing: Yes
4. **CI/CD Provider**
   - GitHub Actions (default)
5. **License**
   - MIT License

6. **Confirmation**
   - Review summary
   - Confirm and generate

**[Screen: Show project being generated]**

"The wizard is now generating your project with all the selected features..."

---

### Exploring the Generated Project (2 minutes)

**[Screen: File explorer and code editor]**

"Let's explore what was generated:"

```bash
cd my-awesome-api
tree -L 2
```

**Show and explain:**

1. **Project Structure**

   ```
   my-awesome-api/
   ├── src/                  # Source code
   ├── tests/                # Test suite
   ├── docs/                 # Jupyter Book documentation
   ├── .github/workflows/    # CI/CD pipelines
   ├── pyproject.toml        # Project configuration
   └── README.md             # Getting started guide
   ```

2. **Key Files**
   - `pyproject.toml` - "Modern Python packaging with all dependencies"
   - `.github/workflows/ci.yml` - "Automated testing on every push"
   - `.github/workflows/security.yml` - "Security scanning"
   - `tests/test_smoke.py` - "Example test"

3. **Pre-commit Hooks**

   ```bash
   cat .pre-commit-config.yaml
   ```

   - "Automatic code formatting with Black"
   - "Linting with Ruff"
   - "Type checking with mypy"

---

### Running Tests and CI/CD Locally (1 minute)

**[Screen: Terminal]**

"Let's verify everything works by running the tests locally:"

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Check coverage
pytest --cov

# Run pre-commit hooks
pre-commit run --all-files
```

**Show:**

- Tests passing
- 100% coverage
- Code quality checks passing

---

### Next Steps (30 seconds)

**[Screen: Back to README or documentation]**

"Congratulations! You've created your first Agentic Canon project. Here's what you should do next:

1. **Push to GitHub**
   - CI/CD will run automatically
   - Security scans will start

2. **Add Your Code**
   - Use the examples in the docs/ folder
   - Follow the patterns in src/

3. **Explore the Documentation**
   - Check out the Jupyter notebooks
   - Learn about security gates
   - Understand the CI/CD pipelines

4. **Customize**
   - Add your own features
   - Adjust CI/CD workflows
   - Configure security rules"

---

### Conclusion (30 seconds)

**[Screen: Agentic Canon logo or dashboard]**

"That's it! You now have a production-ready project with:

- ✅ Automated testing
- ✅ Security scanning
- ✅ Quality gates
- ✅ CI/CD pipelines
- ✅ Documentation

Visit our GitHub repository for more templates and examples. Happy coding!"

**[Show call-to-action:**

- GitHub: github.com/IAmJonoBo/Agentic-Canon
- Documentation: Link to Jupyter Book
- Discord/Community: If available]

---

## Recording Notes

### B-Roll Suggestions

- Dashboard screenshots
- Code being written
- Tests running
- CI/CD pipeline in action
- GitHub Actions workflow visualization

### Screen Recording Tips

- Use clean terminal with good font size (14-16pt)
- Clear browser history/bookmarks
- Disable notifications
- Use zoom/highlighting tools for important parts
- Record at 1080p minimum

### Audio Notes

- Use quality microphone
- Record in quiet environment
- Speak clearly and at moderate pace
- Add subtle background music
- Include captions/subtitles

### Editing Checklist

- [ ] Add intro animation
- [ ] Add section transitions
- [ ] Highlight important commands/code
- [ ] Add on-screen annotations
- [ ] Include timestamps in description
- [ ] Add chapters/sections
- [ ] Include links in description
- [ ] Create thumbnail
- [ ] Add end screen with next videos

---

## YouTube Description Template

```
🚀 Getting Started with Agentic Canon - Create Production-Ready Projects in Minutes

In this tutorial, you'll learn how to use Agentic Canon to scaffold production-ready projects with built-in security, testing, and CI/CD.

⏱️ TIMESTAMPS
0:00 - Introduction
0:30 - What is Agentic Canon?
1:30 - Installation
2:30 - Creating Your First Project
5:00 - Exploring the Generated Project
7:00 - Running Tests Locally
8:00 - Next Steps
8:30 - Conclusion

🔗 LINKS
GitHub Repository: https://github.com/IAmJonoBo/Agentic-Canon
Documentation: [Link to Jupyter Book]
Example Projects: [Link to examples]

📚 MORE TUTORIALS
- Creating a Service with Cookiecutter
- Setting Up CI/CD Pipelines
- Implementing Security Gates
- Adding Observability

#AgenticCanon #DevOps #CICD #Python #SoftwareEngineering
```

---

## Social Media Snippets

### Twitter/X (Thread)

```
🧵 Just created a production-ready API in under 5 minutes using @AgenticCanon

✅ Security scanning
✅ Automated testing
✅ CI/CD pipelines
✅ Quality gates
✅ Documentation

Watch the full tutorial: [link]

1/5
```

### LinkedIn Post

```
Spent hours setting up project boilerplate?

Try Agentic Canon - a framework that scaffolds production-ready projects with security, testing, and CI/CD built-in.

Just released a new tutorial showing how to get started in 5 minutes.

#DevOps #SoftwareEngineering #DeveloperTools
```
