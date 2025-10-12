#!/bin/bash
# ADR Creation Script
# Automates creation of Architecture Decision Records following the template

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ADR_DIR="${REPO_ROOT}/docs/adr"
TEMPLATE="${REPO_ROOT}/templates/architecture/adr/template.md"

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
    echo -e "${RED}Error: ADR template not found at $TEMPLATE${NC}"
    exit 1
fi

# Function to get next ADR number
get_next_adr_number() {
    local max_num=0
    for file in "$ADR_DIR"/ADR-[0-9]*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            # Only process files matching ADR-NNN-*.md pattern
            if [[ "$filename" =~ ^ADR-([0-9]{3})-.*\.md$ ]]; then
                num="${BASH_REMATCH[1]}"
                # Remove leading zeros for comparison
                num=$((10#$num))
                if [ "$num" -gt "$max_num" ]; then
                    max_num=$num
                fi
            fi
        fi
    done
    printf "%03d" $((max_num + 1))
}

# Function to slugify title
slugify() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//'
}

# Main script
echo -e "${GREEN}=== ADR Creation Wizard ===${NC}\n"

# Get ADR number
ADR_NUMBER=$(get_next_adr_number)
echo -e "Next ADR Number: ${YELLOW}${ADR_NUMBER}${NC}"

# Get title
echo -e "\nEnter ADR title (e.g., 'Use PostgreSQL for primary database'):"
read -r TITLE

if [ -z "$TITLE" ]; then
    echo -e "${RED}Error: Title cannot be empty${NC}"
    exit 1
fi

# Create slug
SLUG=$(slugify "$TITLE")
FILENAME="ADR-${ADR_NUMBER}-${SLUG}.md"
FILEPATH="${ADR_DIR}/${FILENAME}"

# Get status
echo -e "\nSelect status:"
echo "1) proposed (default)"
echo "2) accepted"
echo "3) deprecated"
echo "4) superseded"
read -r STATUS_CHOICE

case $STATUS_CHOICE in
    2) STATUS="accepted" ;;
    3) STATUS="deprecated" ;;
    4) STATUS="superseded" ;;
    *) STATUS="proposed" ;;
esac

# Get current date
DATE=$(date +%Y-%m-%d)

# Get decision makers
echo -e "\nEnter decision makers (comma-separated, e.g., 'John Doe - Tech Lead, Jane Smith - Architect'):"
read -r DECISION_MAKERS

# Get problem statement
echo -e "\nEnter brief problem statement:"
read -r PROBLEM

# Create ADR from template
echo -e "\n${GREEN}Creating ADR...${NC}"

cp "$TEMPLATE" "$FILEPATH"

# Replace placeholders
sed -i "s/{{ ADR_NUMBER }}/${ADR_NUMBER}/g" "$FILEPATH"
sed -i "s/{{ DECISION_TITLE }}/${TITLE}/g" "$FILEPATH"
sed -i "s/{{ DATE }}/${DATE}/g" "$FILEPATH"
sed -i "s/{{ STATUS }}/${STATUS}/g" "$FILEPATH"

# Add decision makers if provided
if [ -n "$DECISION_MAKERS" ]; then
    # This is a simple replacement - manual editing may be needed
    sed -i "s/- {{ NAME }} - {{ ROLE }}/${DECISION_MAKERS}/g" "$FILEPATH"
fi

echo -e "${GREEN}✓ ADR created successfully!${NC}"
echo -e "\nFile: ${YELLOW}${FILEPATH}${NC}"
echo -e "\nNext steps:"
echo "1. Edit the ADR file to fill in all sections"
echo "2. Review with stakeholders"
echo "3. Update docs/adr/README.md to link the new ADR"
echo "4. Create a pull request with the ADR"
echo ""
echo -e "Open the ADR now? (y/n)"
read -r OPEN

if [ "$OPEN" = "y" ] || [ "$OPEN" = "Y" ]; then
    if command -v code &> /dev/null; then
        code "$FILEPATH"
    elif command -v vim &> /dev/null; then
        vim "$FILEPATH"
    else
        echo "No editor found. Opening with default..."
        ${EDITOR:-nano} "$FILEPATH"
    fi
fi

echo -e "\n${GREEN}Don't forget to update docs/adr/README.md!${NC}"
