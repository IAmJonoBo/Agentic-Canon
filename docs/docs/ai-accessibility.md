---
title: "AI Accessibility"
summary: "Defines metadata, schemas, and API formats that make documentation consumable by AI agents and automation."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - documentation
  - ai
  - accessibility
sources:
  - "https://json-schema.org/draft/2020-12/"
  - "https://spec.openapis.org/oas/v3.1.0.html"
decision_records:
  - id: "DR-2025-11-05-AIAccess"
    title: "Established AI accessibility metadata and schema usage"
    link: "docs/docs/ai-accessibility.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "JSON Schema 2020-12"
      url: "https://json-schema.org/draft/2020-12/"
      type: "primary"
    - name: "OpenAPI 3.1 specification"
      url: "https://spec.openapis.org/oas/v3.1.0.html"
      type: "primary"
    - name: "frontiers/policy/frontiers.schema.json"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/frontiers.schema.json"
      type: "secondary"
  methods:
    - "Aligned metadata schema with JSON Schema 2020-12 and documented usage patterns."
    - "Outlined best practices for agent-friendly API and data formats."
  key_results:
    - "Metadata requirements, schema validation guidance, and API accessibility rules."
  uncertainty: "Automation tooling for schema validation still pending."
  safer_alternative: "Run manual schema validation scripts until tooling is ready."
---

# AI Accessibility

## Summary

1. Ensures documentation metadata is machine-parseable via `frontiers.schema.json` (JSON Schema 2020-12).
2. Requires APIs and config examples to use OpenAPI 3.1 + JSON Schema 2020-12 for interoperability with agents.
3. Mandates structured data outputs (JSON, YAML) and predictable anchor IDs for retrieval.

## Metadata Requirements

- Include all required front matter fields defined in `frontiers.schema.json`.
- Use ISO dates (`YYYY-MM-DD`) and `Africa/Johannesburg` timezone for `last_verified`.
- Provide at least one primary and one secondary source URL.
- Mirror `provenance` details in both front matter and rendered `## Provenance` block.

## Schema Validation

```bash
pip install jsonschema
python - <<'PY'
import json, yaml
from jsonschema import validate

schema = json.load(open("frontiers/policy/frontiers.schema.json"))
doc = yaml.safe_load(open("docs/quality/iso-25010-rubric.md").read().split('---')[1])
validate(doc, schema)
PY
```

(Automation backlog: add `tools/validate_frontmatter.py` with CI integration.)

## API & Config Guidelines

1. Publish API specs in OpenAPI 3.1; embed `$schema` references to JSON Schema 2020-12.
2. For CLI/config snippets, provide both YAML and JSON forms when practical.
3. Include example requests/responses with redaction guidance; note authentication requirements.
4. Use consistent naming for components (e.g., `QualityGateCheck`).

## Machine-readable Policies

- Store policies under `frontiers/policy/` as YAML/JSON aligned to documented schema.
- Link each policy in the corresponding Markdown file.
- Maintain version and `last_updated` fields in policy files.

## Retrieval Optimisations

- Provide stable anchor IDs for sections (e.g., `{#metadata-requirements}`).
- Use descriptive alt text in diagrams and tables.
- Keep tables machine-friendly (no merged cells).

## Decision Records

- **DR-2025-11-05-AIAccess** — Docs guild approved metadata schema usage and API guidance.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://json-schema.org/draft/2020-12/">JSON Schema 2020-12</a>; <a href="https://spec.openapis.org/oas/v3.1.0.html">OpenAPI 3.1</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/frontiers.schema.json">Front matter schema</a><br>
<strong>Methods:</strong> Ensured metadata requirements align with JSON Schema 2020-12; documented API/config guidance for agent consumption.<br>
<strong>Key results:</strong> Metadata rules, validation snippet, API accessibility requirements, policy alignment.<br>
<strong>Uncertainty:</strong> Automation scripts pending.<br>
<strong>Safer alternative:</strong> Perform manual schema validation until automation lands.
</div>
