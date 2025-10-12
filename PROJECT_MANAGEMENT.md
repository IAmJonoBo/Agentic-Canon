Here’s how to get from a flaky Tasks.md to a tight, self-maintaining loop where “new tasks that surface during implementation” become real, trackable GitHub Issues—without you babysitting it.


> **✨ Implementation Status:** This repository has implemented an enhanced version of this workflow!
> See [docs/TASKS-ADR-SYNC.md](docs/TASKS-ADR-SYNC.md) for the live implementation with ADR integration,
> metadata extraction, and bidirectional sync. The workflows below serve as examples and reference.

Executive summary
	•	Make GitHub Issues + Projects the single source of truth. Stop hand-editing Tasks.md (keep it as a generated mirror if you must).  ￼
	•	Auto-harvest work from the code and reviews:
	•	Convert TODO/FIXME comments → Issues on push; close them when removed.  ￼
	•	Convert unchecked checklist items in Tasks.md (or any markdown) → Issues with a small workflow/script. (Example below.)
	•	From PR review comments, auto-open follow-ups when phrases like “follow-up”, “out of scope”, “nit” appear (scripted via API). Also support manual “Reference in new issue” for precision.  ￼
	•	Auto-triage into Projects (board), set status/iteration/priority with built-in workflows.  ￼
	•	Auto-close & roll-up: use closing keywords in PRs/commits to close linked tasks; the TODO action also closes when the TODO disappears.  ￼
	•	Add guardrails: branch protection, required checks, CODEOWNERS; optionally make Tasks.md read-only.  ￼

⸻

1) Issues as the source of truth (retire Tasks.md as manual)

Use Projects for planning; add Iteration and Priority fields and default workflow states (Todo → In Progress → Done). Built-in Auto-add keeps new Issues flowing onto the board; built-in status rules keep them in sync.  ￼

2) Create Issues automatically from real developer signals

A) From TODO/FIXME in code (zero-friction)

Add this workflow:

# .github/workflows/todos.yml
name: TODOs → Issues
on: [push]
permissions:
  contents: read
  issues: write
  pull-requests: write
jobs:
  todo_to_issue:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: alstr/todo-to-issue-action@v5
        with:
          CLOSE_ISSUES: "true"            # close when TODO removed
          INSERT_ISSUE_URLS: "true"       # writes issue URL back into TODO
          AUTO_ASSIGN: "@me"
          LABELS: "task, from:todo"
          PROJECT: "organization/your-org/Your Project"

This action is maintained, supports Projects (v2), labels/assignees/milestones, and can write the created issue URL back into the source line to prevent duplicates.  ￼

B) From your markdown checklist(s) (e.g., Tasks.md)

Two options:
	•	Thin-slice: If you generate a single file per task, use Create Issue From File.  ￼
	•	Parse checkboxes: One job scans for - [ ] items and opens Issues for any that aren’t already tracked, then replaces the plain text with a #123 tracked-issue link so the list becomes self-healing.

# .github/workflows/tasklist-scan.yml
name: Tasklists → Issues
on:
  push:
    paths: ["Tasks.md", "docs/**.md"]
permissions:
  contents: write
  issues: write
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const path = 'Tasks.md';
            if (!fs.existsSync(path)) { return; }
            let text = fs.readFileSync(path, 'utf8');
            const unchecked = [...text.matchAll(/^-\s\[\s\]\s+(.*)$/gm)].map(m => m[1].trim());
            for (const title of unchecked) {
              // Skip if already a tracked issue link
              if (/#\d+/.test(title)) continue;
              // De-dupe by existing issue title
              const { data: existing } = await github.rest.search.issuesAndPullRequests({
                q: `repo:${context.repo.owner}/${context.repo.repo} is:issue in:title "${title.replace(/"/g,'\\"')}"`
              });
              let number = existing.items.find(i => i.title === title)?.number;
              if (!number) {
                const created = await github.rest.issues.create({
                  owner: context.repo.owner, repo: context.repo.repo,
                  title, labels: ['task','from:tasklist']
                });
                number = created.data.number;
                // Add to a project (optional): gh CLI or Projects API could be used here
              }
              // Replace the line with a tracked-issue checkbox
              const safeTitle = title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
              const re = new RegExp(`^-\\s\$begin:math:display$\\\\s\\$end:math:display$\\s+${safeTitle}$`, 'm');
              text = text.replace(re, `- [ ] #${number} ${title}`);
            }
            fs.writeFileSync(path, text);
      - name: Commit back
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A && git diff --cached --quiet || git commit -m "chore: track checklist items as issues" && git push

Tasklists are first-class in GitHub; converting tasks to issues is also supported in the UI if you want a manual fallback.  ￼

C) From PR review comments (“follow-ups”)

As a baseline, reviewers can “Reference in new issue” on any PR comment (native). If you want automation, trigger on pull_request_review and create an Issue when a review contains follow-up phrases, linking back to the PR/line. Use the REST API or gh issue create.  ￼

3) Auto-triage into Projects (status/iteration/priority)

Enable Auto-add so any new Issues from the above flows land on your Project. Use built-in automations to set Status = Todo on add; use an Iteration field to sequence work in time, and a Priority single-select to sort views.  ￼

4) Auto-close and progress
	•	Use closing keywords (Closes #123) in PRs/commits; GitHub will close the Issue on merge.  ￼
	•	The TODO→Issue action closes those Issues when the TODO disappears.  ￼

5) Guardrails (keep the system clean)
	•	Protected branches + required checks so nothing merges without status checks (tests/linters) and reviews.  ￼
	•	CODEOWNERS to ensure the right reviewers gate changes (including any file like Tasks.md).  ￼
	•	Consider making Tasks.md generated-only (blocked by CODEOWNERS) so humans don’t drift it.

⸻

Minimal CLI helper (optional)

If you prefer shellable, human-triggered creation in Codespaces/remote dev, the GitHub CLI supports gh issue create (and project attachment with the project scope). Handy when Copilot Chat surfaces a task and you want a one-liner.  ￼

⸻

Risks & mitigations
	•	Issue spam from noisy TODOs → allowlist directories, require a label (e.g., TODO(!task)), and cap per-push creations. (The TODO action supports custom identifiers & labels.)  ￼
	•	Duplicates → enable URL insertion so the created Issue URL is written back to the TODO; the tasklist job replaces lines with #123 links.  ￼
	•	Unprioritised backlog → enforce Priority required in the Project and auto-set Todo status on add.  ￼

⸻

Copy-ready setup order (15–30 mins, once)
	1.	Add todos.yml (above) using alstr/todo-to-issue-action@v5.  ￼
	2.	Add tasklist-scan.yml (above) if you still keep a checklist file.
	3.	In Projects: add Auto-add workflow; create Status, Priority, Iteration; set status rules.  ￼
	4.	Turn on branch protection & required checks; add CODEOWNERS.  ￼
	5.	Update PR template to nudge Closes #… usage.  ￼
