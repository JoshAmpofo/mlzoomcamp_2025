ECR_URL="421730342137.dkr.ecr.eu-west-1.amazonaws.com"

REPO_URL=${ECR_URL}/clothing-prediction-lambda

LOCAL_IMAGE_NAME="clothing-prediction-lambda:latest"

REMOTE_IMAGE_TAG="${REPO_URL}:v1"

# authenticate Docker to ECR
aws ecr get-login-password \
    --region "eu-west-1" \
    | sudo docker login \
    --username AWS \
    --password-stdin ${ECR_URL}
