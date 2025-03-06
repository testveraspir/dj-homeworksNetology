# Анализ количество SQL-запросов
Без использования prefetch_related - 4 запроса

![без prefetch_related](static/images/sql_1.png)

С использование prefetch_related - 2 запроса

![с prefetch_related](static/images/sql_2.png)

prefetch_related позволяет получить связанные объекты с помощью одного SQL-запроса с использованием оператора JOIN, вместо трёх запросов.
