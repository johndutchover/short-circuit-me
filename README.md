## short-circuit-me

### Notification insights for Slack

### Development Usage

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

### Fullstack Deployment
- single container for Fly.io
  - https://scm-frontend-1831.fly.dev/

#### scm-poetry/fullstack
- fly.toml
  - `flyctl deploy`
