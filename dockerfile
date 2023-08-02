# specify start image
FROM python:latest


# all commands start from this directory
WORKDIR /vpn_bot

# copy all files from this folder to working directory (ignores files in .dockerignore)
COPY . .

RUN pip install -r requirements.txt

# set the start command
CMD [ "python", "count-bot.py" ]