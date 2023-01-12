FROM ubuntu:20.04
WORKDIR /base

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3 python3-pip 

RUN pip3 install uvicorn fastapi pyyaml
# ENV XDG_RUNTIME_DIR=/base
# RUN chmod -R 777 /base
# ENV RUNLEVEL=3
CMD sh start_service.sh