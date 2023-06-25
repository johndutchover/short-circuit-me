# Makefile

# Build the application
build:
	docker build -t frontend scm-poetry/frontend
	docker build -t backend scm-poetry/backend

build_front:
	docker build -t frontend scm-poetry/frontend

build_back:
	docker build -t backend scm-poetry/backend

run:
	docker run --name backend -d -p 3000:3000 backend:latest
	docker run --name frontend -d -p 8501:8501 frontend:latest
	sleep 7
	open http://localhost:8501

run_front:
	docker run --name frontend -d -p 8501:8501 frontend:latest

run_back:
	docker run --name backend -d -p 3000:3000 backend:latest

stop:
	docker stop backend
	docker stop frontend

start:
	docker start backend
	docker start frontend

clean:
	docker system prune -f
