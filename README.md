# Title
Данная работа была написанна для визуализации иерархии цепочки производителя и поставщиков.

# Run
Для запуска проекта заполните .env.sample и затем введите:
- docker compose build && docker compose up

# Descriptions
Этот проект по большей части является тестовым и показывает на то, как эффективна иерархичная структура.

# Rules
## Contact
- Поля "name", "role", "country" должны быть уникальным массивом данных, похожих объектов с такими данными не может быть

## ProdMap
- Поле "duty" при создании не может быть отрицательным значением.
- Поле "duty" при изменении значение не доступно через API.
- Поле "role" тут действуют некоторые правила неоходимы для структуры проекта:
1. "factory" может быть в только начале цепочки, кроме случая когда "factory" идут подряд.
2. "retail" и "entrepreneur" могут быть только после "factory", первыми по иерархии они не могут быть.
3. "retail" и "entrepreneur" могут чередоваться сколь угодно кроме "factory".
- Поле "products", у сети не может быть большего разнообразия чем у поставщика.
("supplier" -> "products" = {1,2,3,4} and "curr_object" -> "products" = {1,5,6,8,7} | {1,2,3,4} - {1,5,6,8,7} = {5,6,8,7} -> validation_error)


# URLS
## Products
- GET http://localhost/api/products/ - Получение списка товаров
- GET http://localhost/api/products/"lookup_value"/ - Получение товара по номеру
- POST http://localhost/api/products/ - Создание товара
- PATCH http://localhost/api/products/"lookup_value"/ - Изменение товара
- DELETE http://localhost/api/products/"lookup_value"/ - "Не доступно до внедрения некоторых решений"

## Contact
- GET http://localhost/api/contacts/ - Получение списка контактов
- GET http://localhost/api/contacts/"lookup_value"/ - Получение контакта по номеру
- POST http://localhost/api/contacts/ - Создание контакта
- PATCH http://localhost/api/contacts/"lookup_value"/ - Изменение контакта
- DELETE http://localhost/api/contacts/"lookup_value"/ - "Не доступно до внедрения некоторых решений"

## ProdMap
- GET http://localhost/api/prod-map/ - Получение списка цепочек
- GET http://localhost/api/prod-map/"lookup_value"/ - Получение цепочки по номеру
- POST http://localhost/api/prod-map/ - Создание цепочки
- PATCH http://localhost/api/prod-map/"lookup_value"/ - Изменение цепочки
- DELETE http://localhost/api/prod-map/"lookup_value"/ - "Не доступно до внедрения некоторых решений"

# Summary

Были проведенны тесты
- 90% покрытия.
- 19 Тестов.
