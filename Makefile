# Define dependencies
DEPENDENCY_1 = scm-poetry/frontend
DEPENDENCY_2 = scm-poetry/backend

# Build the dependencies
$(DEPENDENCY_1):
    # Build command for dependency 1
    docker build -t frontend:frontend ./frontend

$(DEPENDENCY_2):
    # Build command for dependency 2
    docker build -t backend:backend ./backend

# Build the application
build: $(DEPENDENCY_1) $(DEPENDENCY_2)
    # Build command for the main application

# Run the application
run:
    docker run -d -p 8501:8501 frontend:frontend
    docker run -d -p 3000:3000 backend:backend
    # Add more lines for additional subdirectories if needed

# Stop the application
stop:
    docker stop frontend
    docker stop backend
    # Add more lines for additional subdirectories if needed

# Clean up Docker artifacts
clean:
    docker system prune -f
