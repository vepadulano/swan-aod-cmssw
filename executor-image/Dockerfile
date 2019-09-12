##
# BUILDING STEPS - tini-builder
##
FROM gitlab-registry.cern.ch/linuxsupport/cc7-base:latest as tini-builder

RUN mkdir -p /tmp/

RUN yum install -y \
    curl \
    wget && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    wget --quiet https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini && \
    mv tini /tmp/tini && \
    chmod +x /tmp/tini

FROM gitlab-registry.cern.ch/linuxsupport/cc7-base:latest
MAINTAINER Piotr Mrowczynski <piotr.mrowczynski@cern.ch>

RUN yum install -y \
        which curl atlas HEP_OSlibs && \
    yum clean all && rm -r /var/cache/yum/* && \
    rm /bin/sh && \
    ln -sv /bin/bash /bin/sh && \
    chgrp root /etc/passwd && \
    chmod ug+rw /etc/passwd

WORKDIR ${SPARK_HOME}/work-dir

COPY --from=tini-builder /tmp/tini /sbin/tini
COPY ./entrypoint.sh /
COPY ./cmssw_setup.sh /

ENTRYPOINT ["/entrypoint.sh"]

LABEL \
  org.label-schema.version="0.1" \
  org.label-schema.build-date=$BUILD_DATE \
  org.label-schema.vcs-url="https://gitlab.cern.ch/db/spark-service/docker-registry.git" \
  org.label-schema.name="SWAN Spark Docker - CERN Spark on Kubernetes" \
  org.label-schema.vendor="CERN" \
  org.label-schema.schema-version="1.0"
