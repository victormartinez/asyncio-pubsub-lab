FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:latest

RUN gcloud config set project lab-workspace-318620

CMD ["gcloud", "beta", "emulators", "pubsub", "start", "--host-port=0.0.0.0:8085"]

EXPOSE 8085
