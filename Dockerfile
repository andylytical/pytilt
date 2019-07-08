FROM python:3


# Add an init
RUN pip install dumb-init

# Setup entrypoint
ENV TIMEZONE UTC
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
COPY docker-entrypoint.d /docker-entrypoint.d
ENTRYPOINT ["/usr/local/bin/dumb-init", "--", "/docker-entrypoint.sh"]

# Setup pytilt
RUN apt update && \
    apt install -y bluetooth libbluetooth-dev && \
    pip install pybluez && \
    apt clean
ARG BLESCAN_URL=https://raw.githubusercontent.com/iolate/rasp-ble-scanner/master/blescan.py
RUN curl -o /blescan.py ${BLESCAN_URL}
COPY *.py /
RUN chmod +x /pytilt.py

#CMD ["bash"]
