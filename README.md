# short-circuit-me

[![Pylint](https://github.com/johndutchover/short-circuit-me/actions/workflows/test.yml/badge.svg)](https://github.com/johndutchover/short-circuit-me/actions/workflows/test.yml)

## Notification insights for Slack

### IDE notes:

- from JetBrains...set Python "Virtual Environment" interpreter to existing:
  - `.pixi/envs/default/bin/python`

## CI/CD

### GitLab
- [Qodana Cloud](https://www.jetbrains.com/help/qodana/cloud-about.html)

### GitHub
- Pytest (as defined in pixi.toml)
  - Pytest :`pytest --md=report.md`
  - [GitLab Semgrep analyzer](https://gitlab.com/gitlab-org/security-products/analyzers/semgrep)

### TeamCity Pipelines
- Building container in early access version of TeamCity Pipelines.
