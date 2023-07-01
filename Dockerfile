FROM ubuntu:20.04
WORKDIR /app
COPY . /app
RUN sudo apt-get update -y 
EXPOSE 8000
CMD curl 127.0.0.1:8000/docs
