---
title: Waiver Repository
summary: Canonical store for approved temporary deviations from frontiers policies.
version: 1.0.0
last_verified: 2025-11-05
last_verified_tz: Africa/Johannesburg
diataxis: reference
tags: [governance, waivers]
sources:
  - "docs/workflows/triage-and-exceptions.md"
decision_records:
  - id: "DR-2025-11-05-Waivers"
    title: "Established YAML-based waiver tracking"
    link: "docs/workflows/triage-and-exceptions.md#quality-waivers"
    status: accepted
provenance:
  data:
    - name: "Triaging & Exceptions workflow"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/docs/workflows/triage-and-exceptions.md"
      type: secondary
  methods:
    - "Defined machine-readable format for automated reminders and compliance manifests."
  key_results:
    - "Centralised waiver storage with automation hooks."
  uncertainty: "Waiver schema may expand as new policy classes are added."
  safer_alternative: "Avoid waivers by addressing root cause before merge."
---

# Waiver Repository

Store each approved waiver as a standalone YAML file named `{category}-{control}-{expiry}.yml`. Required fields:

```yaml
id: WVR-2025-001
control: SSDF-PO.3.2
category: supply-chain
owner: platform-security@example.com
approver: ciso@example.com
created: 2025-11-05
expires: 2025-11-12
description: "Awaiting upstream fix for cosign Fulcio outage."
compensating_controls:
  - "Manual signature verification by release manager"
monitoring:
  - "Alert: grafana alert:llm-budget"
status: active
```

Automation:

- `tools/check_waivers.py` scans this directory and surfaces expirations or overdue waivers.
- `.github/workflows/waiver-reminder.yml` runs daily to notify maintainers of upcoming expirations.

Remove files once remediation is complete and update `docs/workflows/triage-and-exceptions.md` with closure details.
