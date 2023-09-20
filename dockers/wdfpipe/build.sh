IMAGE_NAME=${PWD##*/}
IMAGE_VERSION=$(head -n1 version.txt)

docker build -t wdfteam/${IMAGE_NAME}:${IMAGE_VERSION} .
