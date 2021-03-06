FROM aexea/django-base:py3.5-slim
MAINTAINER Aexea Carpentry

WORKDIR marquote
ENV TEST_ON_PLATFORM DOCKER
USER root
# start.sh will be generated by salt on deployment
ENTRYPOINT ["./start.sh"]
CMD ["web"]
