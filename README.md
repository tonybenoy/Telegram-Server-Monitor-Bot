# Telegram-Server-Monitor-Bot
Bot to monitor a server.
To the run the bot you first need to create a config.ini file
```
[telegram]
api_key = <api key> #use @BotFather
admin_user_id=<user_id> #use @Userrinfobot bot
first_name=Tony
```
## Run using docker
Build the image with
```
docker build -t telebot .
```
Run with
```
docker run  -d telebot
```

## Use Python
The project supports poetry
Run
```
poetry install
```
Then
```
python app.py
```
