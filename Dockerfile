# pull official base image
FROM python:3.11.10-bookworm

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/dicom-viewer

RUN apt-get update && \
 apt-get install -y nodejs npm

RUN apt install nodejs npm && \
  mkdir /app/public && \
  npm install && \
  npm run build --production

EXPOSE 5000

WORKDIR /app

# Run application
CMD [ "flask", "--app", "app/server", "--host", "0.0.0.0", "run" ]