

ECR_URL="421730342137.dkr.ecr.eu-west-1.amazonaws.com"

REPO_URL=${ECR_URL}/churn-prediction-lambda

LOCAL_IMAGE_NAME="churn-prediction-lambda"

REMOTE_IMAGE_TAG="${REPO_URL}:v1"

# authenticate Docker to ECR
aws ecr get-login-password \
    --region "eu-west-1" \
    | sudo docker login \
    --username AWS \
    --password-stdin ${ECR_URL}



sudo docker build -t ${LOCAL_IMAGE_NAME} .

sudo docker tag ${LOCAL_IMAGE_NAME} ${REMOTE_IMAGE_TAG}

sudo docker push ${REMOTE_IMAGE_TAG}

echo "Image pushed to ECR: ${REMOTE_IMAGE_TAG}"