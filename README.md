# TgQuizBot
Telegram-бот для участия в Quiz-викторине. 

Для запуска бота необходимо выполнить:

```
git clone https://github.com/Semund/TgQuizBot.git && cd ./TgQuizBot
``` 
В переменных окружения необходимо добавить `TG_API_TOKEN` - API токен бота.
___

Для работы через docker необходимо предварительно заполнить ENV переменную `TG_API_TOKEN` в `Dockerfile`
После чего запустить контейнер:
```
docker build -t tgquiz ./
docker run -d --name tg tgquiz
``` 


[База вопросов](https://baza-otvetov.ru/categories/view/1/), которая использовалась в разработке.
