# Project 7 - Image Generation and Voice Chat

Instructions to run the project:
- Make sure you're connected to the VPN(Ivanti)
- Start Docker Engine
- Build the docker image which might fail if on Windows.
```
docker build -t cs5740-project7 .
```
## For Windows, run the following commands:
1. Build a multi-platform Builder context:
```
docker buildx create --use --platform=linux/arm64,linux/amd64 --name multi-platform-builder
docker buildx inspect --bootstrap
```
2. Now, use this builder to build your image:
```
docker buildx build -t cs5740-project7 --platform multi-platform-builder .
```
3. Run the docker image:
```
docker run -p 8501:8501 -v .:/app --name cs5740-project7 cs5740-project7
```

- Finally, access it on http://localhost:8501/