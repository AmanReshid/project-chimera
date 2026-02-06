# AI Review Policy — Project Chimera

Purpose: define what an automated AI reviewer (CodeRabbit/other) should check on pull requests.

Primary checks

- Spec Alignment (required)
  - Ensure implementation code has corresponding spec coverage in `specs/`.
  - Validate `skills/` modules follow the required structure (`interface.py`, `impl.py`, `README.md`) and have tests.
  - Flag missing traceability between code and spec documents.

- Security Vulnerabilities (required)
  - Run static analyzers (Bandit) and dependency audits (`pip-audit`) and report findings.
  - Highlight critical vulnerabilities and provide remediation suggestions.

Behavior

- Fail the automated review if the `spec_alignment` check reports fatal failures.
- Fail the automated review if `pip-audit` or Bandit reports high/critical issues.
- For warnings (non-fatal), post a comment with context and suggested fixes.

How to run locally

```bash
python scripts/spec_check.py
python -m pip install bandit pip-audit
bandit -r . -f txt
pip-audit --output pip-audit.json
```
