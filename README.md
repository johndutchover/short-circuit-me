## short-circuit-me

[![Pylint](https://github.com/johndutchover/short-circuit-me/actions/workflows/pylint.yml/badge.svg)](https://github.com/johndutchover/short-circuit-me/actions/workflows/pylint.yml)

### Notification insights for Slack

#### Bolt for Python
- [Package slack_bolt](https://slack.dev/bolt-python/api-docs/slack_bolt/)

#### Makefile

##### build
- `make build`
  - copy message_counts.csv from backend
    - use `slackbolt_csv.app` which bypasses MongoDB Atlas
  - build docker images

##### run
- `make run` 
  - start application containers

##### stop
- `make stop`

##### clean
- `make clean`
  - cleanup docker containers
