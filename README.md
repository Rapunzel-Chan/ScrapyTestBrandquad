# ScrapyTestBrandquad — Парсер

## Описание:

**ScrapyTestBrandquad** — это веб-приложение для автоматического поиска и расчета средней стоимости товаров 
в строительной сфере, с возможностью настроить автоматический парсер по расписанию и получению готовых 
отчетов по выбранным товарам за установленный период.

## Установка:

1. Клонируйте репозиторий:

```
clone -b develop https://github.com/Rapunzel-Chan/.git
```

2. Установите зависимости:

```
pip install -r requirements.txt
```

## Использование:

1. Переключитесь на проект:

```
cd 
```

2. Создайте виртуальное окружение:

```
python -m venv venv
```

3. Активируйте виртуальное окружение:

- Windows:

```
.\venv\Scripts\activate
```

- Linux/macOS:

```
source venv/bin/activate
```

4. Примените миграции:

```
python manage.py migrate
```

5. Создайте суперпользователя:

```
python manage.py csu
```

6. Запустите сервер:

```
python manage.py runserver
```

7. Запустите Celery:

```
celery -A config beat --loglevel=info
celery -A config worker --loglevel=info
```

## Тестирование:

Для запуска тестов напишите(***ПОКА НАХОДИТСЯ В РАЗРАБОТКЕ***):

```
python manage.py test
```

## Функциональность:


## Работа с парсером

Шаг 1. 

## Кастомные команды и сервисы ***ТОЛЬКО ДЛЯ РАЗРАБОТЧИКОВ***:


## Сокрытие чувствительных данных

Список переменных окружений находится в .env.example. Заполните данные для правильной работы приложения.

## Запуск и проверка сервисов приложения в Docker-контейнере

```
docker compose up -d --build
```
5. Поднимите базовые сервисы и проверьте статус и их "здоровье", соберите статику:
```
docker compose -f docker-compose.prod.yml up static_collector
docker-compose up -d db redis
docker-compose ps
```

6. Выполните миграции для полноценной работы beat и создайте суперпользователя:
```
docker compose exec backend python manage.py createsuperuser
docker-compose run --rm backend python manage.py migrate
```

7. Поднимите все сервисы:
```
docker-compose up -d backend celery beat
```

8. Проверьте логи по сервисам:
```
docker-compose -f logs backend
docker-compose -f logs celery
docker-compose -f logs beat
```

## Deploy и проверка сервисов приложения на Yandex.Cloud:

1. Подготовьте сервер (Yandex Cloud / Ubuntu 22.04):
```
ssh ubuntu@SERVER_IP
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv docker.io docker-compose-plugin git ufw
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
sudo ufw status
```

2. Настройте SSH-ключи для GitHub Actions:

Локально:
```
ssh-keygen -t ed25519 -C "deploy@priceparser" -f ~/.ssh/priceparser_deploy
```
На сервере:
```
ssh-copy-id -i ~/.ssh/priceparser_deploy.pub ubuntu@SERVER_IP
ssh -i ~/.ssh/priceparser_deploy ubuntu@SERVER_IP
```

3. Склонируйте проект:
```
git clone https://github.com/<your-username>/priceparser.git
cd Average_price_parser
```

4. Подготовьте переменные окружения:
```
cp .env.example .env
base64 --wrap=0 .env > env.b64 **либо** certutil -encode .env env.b64
Get-Content env.b64 | Select-Object -Skip 1 | Select-Object -SkipLast 1 | Out-File -Encoding ascii env_clean.b64
```

5. Соберите статику:
```
docker compose -f docker-compose.prod.yml up static_collector
```

6. Зайдите в Repo → Settings → Secrets → Actions и добавьте:

| Secret           | Значение                             |
|------------------|--------------------------------------|
 ENV_FILE	        | содержимое env.b64 или env_clean.b64 |
| SERVER_IP        | 	IP сервера                          |
| SERVER_USER      | 	ubuntu или другой пользователь      |
| SERVER_SSH_KEY   | 	приватный ключ ilearn_deploy        |
| DOCKERHUB_USERNAME | 	твой Docker Hub username            |
| DOCKERHUB_TOKEN  |Access Token из Docker Hub |

7. Подготовьте Systemd Unit для Docker Compose и вставьте данные из deploy/systemd/average_price_parser.service:


8. Подготовьте Nginx и вставьте данные из deploy/nginx/default.conf:


9. Запустите GitHub Actions Workflow (.github/workflows/deploy.yml):


10. Проверьте работу всего deploy:



## Вспомогательная информация

Для работы Парсера необходим Google Chrome версии 140 и выше, соответственно, нужен совместимый chromedriver 114/115
и выше версий. 

## Создатель

В случае возникновения вопросов, нахождения багов или предложений по улучшению кода, можно обратиться к разработчику
по e-mail: rapuncel.chan24@gmail.com.
