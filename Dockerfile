FROM docker.io/ubuntu:26.04

# fixed timezone, so the emergency cron job fires at 23:00 local time
ENV TZ=Europe/Berlin

RUN apt update
RUN apt -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt -y install cron python3 python3-dev python3-pip tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install pymodbus==3.7.4 pyserial_asyncio pyserial goodwe==0.4.10 --break-system-packages

RUN which python3

# copy files
COPY python /app/python
COPY shell/goodwe-idm.sh /app/goodwe-idm.sh
COPY shell/goodwe-idm-zero.sh /app/goodwe-idm-zero.sh
COPY shell/entrypoint.sh /app/entrypoint.sh
COPY shell/container_cron /etc/cron.d/container_cron

# set workdir
WORKDIR /app

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/container_cron

# apply cron job
RUN crontab /etc/cron.d/container_cron

# run the command on container startup
CMD ["bash", "entrypoint.sh"]
