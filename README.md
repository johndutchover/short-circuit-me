## short-circuit-me

[![Pylint](https://github.com/johndutchover/short-circuit-me/actions/workflows/pylint.yml/badge.svg)](https://github.com/johndutchover/short-circuit-me/actions/workflows/pylint.yml)

### Notification insights for Slack

### Usage

#### Makefile

##### build
- `make build`
  - copy message_counts.csv from backend
    - use `slackbolt_csv.app` which bypasses MongoDB Atlas
  - build docker images

##### run
- `make run` 
  - Launch application containers
    -  Opens Streamlit (sleep 7)

##### stop
- `make stop`

##### start
- `make start`
  - start application containers

##### clean
- `make clean`
  - cleanup unused containers
