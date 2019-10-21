FROM alpine:edge

RUN apk add --no-cache \
    bash \
    python3 \
    ruby \
    py3-pip \ 
    musl-dev \
    gcc

RUN gem install ceedling --no-document 
