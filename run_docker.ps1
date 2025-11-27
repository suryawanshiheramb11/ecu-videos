# Build the Docker image
docker build -t ecu-videos .

# Run the container
# -p 8501:8501 maps port 8501 on your machine to port 8501 in the container
# --env-file .env passes your environment variables (API keys) to the container
docker run -p 8501:8501 --env-file .env ecu-videos
