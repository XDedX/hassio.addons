ARG BUILD_FROM=hassioaddons/ubuntu-base:4.0.3
FROM $BUILD_FROM

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_ARCH=amd64

RUN apt-get update && \
    apt-get install apt-utils --yes && \
    apt-get upgrade --yes && \
    DEBIAN_FRONTEND="noninteractive" apt-get --yes --option Dpkg::Options::="--force-confnew" --no-install-recommends install && \
    apt-get install libopencv-dev libtesseract-dev python3-pip git cmake build-essential libleptonica-dev --yes && \
    apt-get install liblog4cplus-dev libcurl3-dev python3-numpy libopenalpr-dev openalpr --yes && \
    pip3 install Flask requests pyopenalpr

RUN mkdir -p /root/oalpr/data && mkdir -p /root/oalpr/scripts && mkdir -p /root/oalpr/log

# Добавляем поддержку ua на основе eu
RUN mkdir -p /usr/share/openalpr/runtime_data/config && \
    mkdir -p /usr/share/openalpr/runtime_data/postprocess && \
    mkdir -p /usr/share/openalpr/runtime_data/ocr && \
    cp /usr/share/openalpr/runtime_data/config/eu.conf /usr/share/openalpr/runtime_data/config/ua.conf && \
    echo "[A-Z]{2}[0-9]{4}[A-Z]{2}" > /usr/share/openalpr/runtime_data/postprocess/ua.patterns && \
    cp /usr/share/openalpr/runtime_data/ocr/eu.traineddata /usr/share/openalpr/runtime_data/ocr/ua.traineddata

COPY ./oalpr.py /root/oalpr/scripts
COPY rootfs /

CMD bash -c "export COUNTRY=$(jq -r '.country' /data/options.json) && python3 -u /config/oalpr/scripts/oalpr.py"

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
