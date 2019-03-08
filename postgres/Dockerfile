FROM postgres:9.5

ENV WAL2JSON_COMMIT_ID=92b33c7d7c2fccbeb9f79455dafbc92e87e00ddd

# Install the packages which will be required to get everything to compile
RUN apt-get update \
    && apt-get install -f -y --no-install-recommends \
        software-properties-common \
        build-essential \
        pkg-config \
        git \
        postgresql-server-dev-9.5 \
        libproj-dev \
    && rm -rf /var/lib/apt/lists/*


RUN git clone https://github.com/eulerto/wal2json -b master --single-branch \
    && cd /wal2json \
    && git checkout $WAL2JSON_COMMIT_ID \
    && make && make install \
    && cd / \
    && rm -rf wal2json
