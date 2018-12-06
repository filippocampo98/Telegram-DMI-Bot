FROM  ubuntu:18.04

ENV DMI_BOT_REPO    https://github.com/UNICT-DMI/Telegram-DMI-Bot.git
ENV DMI_BOT_DIR    /usr/local

ENV TOKEN    _TOKEN_

RUN apt-get update && \
  apt-get install -y \
	git \
	git-lfs \
	python3 \
	python3-pip\
	language-pack-it

RUN mkdir -p $DMI_BOT_DIR && \
  cd $DMI_BOT_DIR && \
  git clone -b master $DMI_BOT_REPO dmibot

RUN pip3 install -r $DMI_BOT_DIR/dmibot/requirements.txt

RUN cp $DMI_BOT_DIR/dmibot/data/DMI_DB.db.dist $DMI_BOT_DIR/dmibot/data/DMI_DB.db
RUN cp $DMI_BOT_DIR/dmibot/config/settings.yaml.dist $DMI_BOT_DIR/dmibot/config/settings.yaml
RUN echo $TOKEN > $DMI_BOT_DIR/dmibot/config/token.conf
