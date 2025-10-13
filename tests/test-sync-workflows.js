#!/usr/bin/env node
/**
 * Test script for TASKS.md and ADR sync workflows
 *
 * This simulates the workflow logic to verify it works correctly
 * without actually creating GitHub issues.
 */

const fs = require("fs");
const path = require("path");

// Test data
const testTasksContent = `# Test TASKS.md

## Version 2.0 - High Priority Features

### Security Enhancements
These tasks implement ADR-005 (SLSA compliance) and ADR-008.
- [ ] Generate SBOM for all builds
- [ ] Sign release artifacts (ADR-005)
- [x] #123 Implement secret scanning
- [ ] Add security headers

### Documentation
- [ ] Update API documentation
- [ ] Create user guide (ADR-001)

## Version 3.0 - Lower Priority

### Performance
- [ ] Optimize database queries
- [ ] Implement caching layer
`;

console.log("🧪 Testing TASKS.md Metadata Extraction\n");

// Simulate the workflow script logic
function extractTaskMetadata(text) {
  const lines = text.split("\n");
  const tasks = [];
  let currentSection = "";
  let currentSubsection = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Track section headers
    if (line.match(/^## /)) {
      currentSection = line.replace(/^## /, "").trim();
      currentSubsection = "";
    } else if (line.match(/^### /)) {
      currentSubsection = line.replace(/^### /, "").trim();
    }

    // Find unchecked items
    const match = line.match(/^-\s\[\s\]\s+(.*)$/);
    if (match) {
      const title = match[1].trim();

      // Skip if already tracked
      if (/#\d+/.test(title)) continue;

      const metadata = {
        title: title,
        section: currentSection,
        subsection: currentSubsection,
        adrRefs: [],
        issueRefs: [],
        labels: ["task", "from:tasklist"],
        lineNumber: i,
        contextLines: [],
      };

      // Extract ADR references
      const adrPattern = /ADR-(\d{3})/g;
      let adrMatch;
      while ((adrMatch = adrPattern.exec(title)) !== null) {
        metadata.adrRefs.push(`ADR-${adrMatch[1]}`);
      }

      // Look for ADRs in context
      for (let j = Math.max(0, i - 5); j < i; j++) {
        const contextLine = lines[j].trim();
        if (contextLine && !contextLine.match(/^-\s\[/)) {
          metadata.contextLines.push(contextLine);

          let contextAdrMatch;
          const contextAdrPattern = /ADR-(\d{3})/g;
          while (
            (contextAdrMatch = contextAdrPattern.exec(contextLine)) !== null
          ) {
            const adrRef = `ADR-${contextAdrMatch[1]}`;
            if (!metadata.adrRefs.includes(adrRef)) {
              metadata.adrRefs.push(adrRef);
            }
          }
        }
      }

      // Add component labels based on section
      if (currentSection.includes("Template")) {
        metadata.labels.push("component:templates");
      } else if (currentSection.includes("Notebook")) {
        metadata.labels.push("component:notebooks");
      } else if (
        currentSubsection.includes("Documentation") ||
        currentSection.includes("Documentation")
      ) {
        metadata.labels.push("component:documentation");
      } else if (
        currentSection.includes("CLI") ||
        currentSection.includes("Wizard")
      ) {
        metadata.labels.push("component:cli");
      } else if (
        currentSubsection.includes("Security") ||
        currentSection.includes("Security")
      ) {
        metadata.labels.push("security");
      } else if (currentSection.includes("Testing")) {
        metadata.labels.push("component:testing");
      } else if (
        currentSubsection.includes("Performance") ||
        currentSection.includes("Performance")
      ) {
        metadata.labels.push("performance");
      }

      // Add priority based on section
      if (currentSection.includes("High Priority")) {
        metadata.labels.push("priority:high");
      } else if (currentSection.includes("Medium Priority")) {
        metadata.labels.push("priority:medium");
      } else if (currentSection.includes("Lower Priority")) {
        metadata.labels.push("priority:low");
      }

      tasks.push(metadata);
    }
  }

  return tasks;
}

// Run the test
const tasks = extractTaskMetadata(testTasksContent);

console.log(`Found ${tasks.length} unchecked tasks\n`);

// Display results
tasks.forEach((task, i) => {
  console.log(`Task ${i + 1}: ${task.title}`);
  console.log(`  Section: ${task.section} > ${task.subsection}`);
  console.log(`  Line: ${task.lineNumber + 1}`);
  console.log(`  Labels: ${task.labels.join(", ")}`);

  if (task.adrRefs.length > 0) {
    console.log(`  ADR Refs: ${task.adrRefs.join(", ")}`);
  }

  if (task.contextLines.length > 0) {
    console.log(`  Context: ${task.contextLines.slice(-2).join(" | ")}`);
  }

  console.log();
});

// Validate results
console.log("✅ Validation:\n");

const tests = [
  {
    name: "Task 1 should have ADR-005 and ADR-008 from context",
    condition:
      tasks[0].adrRefs.includes("ADR-005") &&
      tasks[0].adrRefs.includes("ADR-008"),
  },
  {
    name: "Task 2 should have ADR-005 from title",
    condition: tasks[1].adrRefs.includes("ADR-005"),
  },
  {
    name: "Task 4 should have documentation label",
    condition: tasks[3].labels.includes("component:documentation"),
  },
  {
    name: "Task 5 should have ADR-001 from title",
    condition: tasks[4].adrRefs.includes("ADR-001"),
  },
  {
    name: "Task 5 should have documentation label",
    condition: tasks[4].labels.includes("component:documentation"),
  },
  {
    name: "Tasks in High Priority section should have priority:high",
    condition: tasks
      .slice(0, 4)
      .every((t) => t.labels.includes("priority:high")),
  },
  {
    name: "Tasks in Lower Priority section should have priority:low",
    condition: tasks.slice(6).every((t) => t.labels.includes("priority:low")),
  },
];

let passed = 0;
let failed = 0;

tests.forEach((test) => {
  if (test.condition) {
    console.log(`  ✅ ${test.name}`);
    passed++;
  } else {
    console.log(`  ❌ ${test.name}`);
    failed++;
  }
});

console.log(
  `\n📊 Results: ${passed} passed, ${failed} failed out of ${tests.length} tests\n`,
);

if (failed === 0) {
  console.log("🎉 All tests passed! Workflow logic is working correctly.\n");
  process.exit(0);
} else {
  console.log("⚠️  Some tests failed. Please review the logic.\n");
  process.exit(1);
}
