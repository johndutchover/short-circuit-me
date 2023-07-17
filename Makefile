deploy-backend:
	cd backend && flyctl deploy

deploy-frontend:
	cd frontend && flyctl deploy

start-frontend:
	shell cd frontend && flyctl scale count 1 -y

start-backend:
	shell cd backend && flyctl scale count 1 -y

stop-frontend:
	shell cd frontend && flyctl scale count 0 -y

stop-backend:
	shell cd backend && flyctl scale count 0 -y
