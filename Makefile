# Makefile

# Define dependencies
POETRY_HOME = scm-poetry
FRONTEND_DEP_1 = scm-poetry/frontend
BACKEND_DEP_2 = scm-poetry/backend

# List of destination directories for csv copy
DESTINATIONS := $(FRONTEND_DEP_1) $(POETRY_HOME)

# Build the dependencies
$(FRONTEND_DEP_1):
    # Build command for dependency 1
	docker build -t frontend scm-poetry/frontend

$(BACKEND_DEP_2):
    # Build command for dependency 2
	docker build -t backend scm-poetry/backend

# Copy the CSV file created by backend to scm-poetry and frontend
copy_csv:
	for dir in $(DESTINATIONS); do \
		cp scm-poetry/data/message_counts.csv $$dir/message_counts.csv; \
	done

# Build the application
build:
	make copy_csv
	docker build -t frontend scm-poetry/frontend
	docker build -t backend scm-poetry/backend

# Run the application and mount scm-poetry as /frontend on containers
run:
	docker run --name frontend -d -p 8501:8501 -v $(PWD):/frontend frontend:latest
	docker run --name backend -d -p 3000:3000 -v $(PWD):/frontend backend:latest
	sleep 5
	open http://localhost:8501

# Stop the application
stop:
	docker stop frontend
	docker stop backend

# Clean up Docker artifacts
clean:
	docker system prune -f
