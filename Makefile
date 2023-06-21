# Makefile

# Build the application
build:
	docker build -t fullstack scm-poetry/fullstack
	# docker build -t frontend scm-poetry/frontend
	# docker build -t backend scm-poetry/backend

# Run the application and mount scm-poetry as /frontend on containers
run:
	docker run --name fullstack -d -p 8501:8501 fullstack:latest
	# docker run --name frontend -d -p 8501:8501 -v ./scm-poetry/frontend/message_counts.csv:/app/message_counts.csv frontend:latest
	# docker run --name backend -d -p 3000:3000 -v ./scm-poetry/frontend/message_counts.csv:/bolt/message_counts.csv backend:latest
	sleep 7
	open http://localhost:8501

# Stop the application
stop:
	docker stop fullstack

# Start the application
start:
	docker start fullstack
	open http://localhost:8501

# Clean up Docker artifacts
clean:
	docker system prune -f
