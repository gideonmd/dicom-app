# pull official base image
FROM python:3.11.10-alpine3.20

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/dicom-viewer

# Installs node, npm, serve, and node packages
# then builds the app
RUN apk add --update nodejs npm && \
  npm install && \
  npm run build --production



EXPOSE 5000

# Run application
CMD [ "flask", "--app", "app/server", "-p", "3000", "run" ]