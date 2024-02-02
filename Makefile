deploy-backend:
	flyctl deploy --config backend/fly.toml -a shortcircuitme-backend

start-backend:
	flyctl scale count 1 -y -a shortcircuitme-backend

stop-backend:
	flyctl scale count 0 -y -a shortcircuitme-backend
