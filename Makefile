# Build the application
build:
    docker build -t ./scm-poetry/frontend .

# Run the application
run:
    docker run -d -p 8501:8501 frontend

# Stop the application
stop:
    docker frontend your_container_name

# Clean up Docker artifacts
clean:
    docker system prune -f
