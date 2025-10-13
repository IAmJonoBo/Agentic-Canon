#!/bin/bash
# Setup GitHub Labels for Project Management Automation
#
# This script creates all required labels for the project management workflows
# to function properly. It uses the GitHub CLI (gh) which must be installed
# and authenticated.
#
# Usage: ./scripts/setup-labels.sh

set -e # Exit on error

# Check if gh CLI is installed
if ! command -v gh &>/dev/null; then
	echo "❌ GitHub CLI (gh) is not installed."
	echo "Install from: https://cli.github.com/"
	exit 1
fi

# Check if authenticated
if ! gh auth status &>/dev/null; then
	echo "❌ Not authenticated with GitHub CLI."
	echo "Run: gh auth login"
	exit 1
fi

echo "🏷️  Setting up GitHub labels for project management automation..."
echo ""

# Function to create label (silently skip if exists)
create_label() {
	local name="$1"
	local color="$2"
	local description="$3"

	if gh label create "$name" --color "$color" --description "$description" 2>/dev/null; then
		echo "✅ Created: $name"
	else
		echo "⏭️  Exists: $name"
	fi
}

echo "📌 Creating Issue Type Labels..."
create_label "bug" "d73a4a" "Something isn't working"
create_label "enhancement" "a2eeef" "New feature or request"
create_label "task" "0e8a16" "Work item or task"
create_label "documentation" "0075ca" "Documentation improvements or additions"
create_label "question" "d876e3" "Further information is requested"

echo ""
echo "🤖 Creating Workflow Labels..."
create_label "from:todo" "d4c5f9" "Created from TODO/FIXME comment"
create_label "from:tasklist" "bfdadc" "Created from markdown checklist"
create_label "from:pr-review" "fbca04" "Created from PR review follow-up"
create_label "needs-triage" "ededed" "Needs initial review and categorization"

echo ""
echo "⭐ Creating Priority Labels..."
create_label "priority:high" "d93f0b" "High priority item"
create_label "priority:medium" "fbca04" "Medium priority item"
create_label "priority:low" "0e8a16" "Low priority item"

echo ""
echo "🔒 Creating Status & Special Labels..."
create_label "stale" "cccccc" "Marked as stale due to inactivity"
create_label "security" "ee0701" "Security-related issue"
create_label "performance" "1d76db" "Performance-related issue"
create_label "critical" "b60205" "Critical issue needing immediate attention"
create_label "pinned" "0e8a16" "Pinned, won't be marked stale"

echo ""
echo "✅ Label setup complete!"
echo ""
echo "📋 To verify, run: gh label list"
echo "📖 For more information, see: .github/LABELS.md"
