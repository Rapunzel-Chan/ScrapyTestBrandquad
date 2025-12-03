# ScrapyTestBrandquad — Парсер

Парсер товаров интернет-магазина [Alkoteka](https://alkoteka.com) с использованием Scrapy.  
Собирает информацию о товарах из заданных категорий с учетом выбранного региона (Краснодар) и поддержкой прокси.



## Возможности

- Сбор данных по категориям (`START_URLS`) из `.env`.
- Учет региона через куки и `city_uuid`.
- Пагинация и сбор всех товаров категории.
- Возможность использовать прокси из .env.
- Автоматическая подстановка случайного прокси для каждого запроса.
- Работа даже при падении прокси — паук продолжает сбор.
- Сбор всех обязательных полей по шаблону тестового задания:

```json
{
  "timestamp": int,
  "RPC": "str",
  "url": "str",
  "title": "str",
  "marketing_tags": ["str"],
  "brand": "str",
  "section": ["str"],
  "price_data": {
    "current": float,
    "original": float,
    "sale_tag": "str"
  },
  "stock": {
    "in_stock": bool,
    "count": int
  },
  "assets": {
    "main_image": "str",
    "set_images": ["str"],
    "view360": ["str"],
    "video": ["str"]
  },
  "metadata": { ... },
  "variants": int
}
```


## Установка:

1. Клонируйте репозиторий:

```
clone -b develop https://github.com/Rapunzel-Chan/ScrapyTestBrandquad.git
```

2. Установите зависимости:

```
pip install -r requirements.txt
```

## Использование:

1. Переключитесь на проект:

```
cd alkoteka_parser
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

4. Создайте .env файл в корне проекта и заполните данные на примере .env.example.

5. Запустите парсер командой в терминале с сохранением результатов работы парсера:

```
scrapy crawl alkoteka -O result.json
```

## Сокрытие чувствительных данных

Список переменных окружений находится в .env.example. Заполните данные для правильной работы приложения.


## Вспомогательная информация

Для работы Парсера через прокси использовался прокси сайта https://dashboard.webshare.io/. 

## Создатель

В случае возникновения вопросов, нахождения багов или предложений по улучшению кода, можно обратиться к разработчику
по e-mail: rapuncel.chan24@gmail.com.
