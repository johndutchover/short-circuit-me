# Makefile

# Define dependencies
FRONTEND_DEP_1 = scm-poetry/frontend
BACKEND_DEP_2 = scm-poetry/backend

# Build the dependencies
$(FRONTEND_DEP_1):
    # Build command for dependency 1
	docker build -t frontend scm-poetry/frontend

$(BACKEND_DEP_2):
    # Build command for dependency 2
	docker build -t backend scm-poetry/backend

# Build the application
build:
	docker build -t frontend scm-poetry/frontend
	docker build -t backend scm-poetry/backend

# Run the application and mount scm-poetry as /frontend on containers
run:
	docker run --name frontend -d -p 8501:8501 -v $(PWD):/frontend frontend:latest
	docker run --name backend -d -p 3000:3000 -v $(PWD):/frontend backend:latest

# Stop the application
stop:
	docker stop frontend
	docker stop backend

# Clean up Docker artifacts
clean:
	docker system prune -f
