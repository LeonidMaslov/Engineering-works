#FROM python:3.11-slim-bullseye
#
#WORKDIR /app
#
#COPY ./requirements ./requirements
#
#RUN apt-get update \
# && apt-get install -y -qq --no-install-recommends curl nano iputils-ping ethtool tcpdump jq \
# git \
# && apt-get clean && rm -rf /var/lib/apt/lists/*
#
#
#RUN python -m pip install pip --upgrade \
# && python -m pip install -r requirements/base.txt
#
#COPY . /app
#
#RUN cp commands/entrypoint.sh ./ && chmod +x ./entrypoint.sh
#
#RUN groupadd --gid 1001 app \
#  && useradd --uid 1001 --gid app --shell /bin/bash app
#USER app
#
#CMD ["/app/entrypoint.sh"]
