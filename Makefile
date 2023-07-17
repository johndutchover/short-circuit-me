deploy-backend:
	$(shell cd backend && flyctl deploy)

deploy-frontend:
	$(shell cd frontend && flyctl deploy)

stop-frontend:
	$(shell cd frontend && flyctl scale count 0 -y)

stop-backend:
	$(shell cd backend && flyctl scale count 0 -y)

start-frontend:
	$(shell cd frontend && flyctl scale count 1 -y)

start-backend:
	$(shell cd backend && flyctl scale count 1 -y)
