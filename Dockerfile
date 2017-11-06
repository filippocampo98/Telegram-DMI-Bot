FROM  ubuntu:16.04

ENV DMI_BOT_REPO    https://github.com/UNICT-DMI/Telegram-DMI-Bot.git
ENV DMI_BOT_DIR    /usr/local

ENV TOKEN    _TOKEN_

RUN apt-get update && \
  apt-get install -y \
	git \
	python2.7\
	python-pip \
	python-bs4 \
	python-beautifulsoup \
	python-sqlite \
	language-pack-it \
	nano \
	wget

RUN wget https://raw.githubusercontent.com/UNICT-DMI/Telegram-DMI-Bot/master/requirements.txt -O /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p $DMI_BOT_DIR && \
  cd $DMI_BOT_DIR && \
  git clone -b master $DMI_BOT_REPO dmibot

RUN cp $DMI_BOT_DIR/dmibot/data/DMI_DB.db.dist $DMI_BOT_DIR/dmibot/data/DMI_DB.db
RUN cp $DMI_BOT_DIR/dmibot/config/settings.yaml.dist $DMI_BOT_DIR/dmibot/config/settings.yaml
RUN echo $TOKEN > $DMI_BOT_DIR/dmibot/config/token.conf
