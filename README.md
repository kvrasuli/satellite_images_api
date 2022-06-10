## API
Веб-сервис, позволяющий хранить географические объекты в формате geojson,
и скачивать соответствующие изображения со спутника Sentinel-2 с доступом по REST API
Задеплоено [тут](http://ec2-3-122-231-1.eu-central-1.compute.amazonaws.com:8449/)

## Как запустить
Добавить в корень файл .env со следующими переменными
```
COPERNICUS_USERNAME={copernicus username}
COPERNICUS_PASSWORD={copernicus password}
MONGO_URL=mongodb://db:27017
```
Выполнить
```
docker-compose up
```
Открыть в браузере http://127.0.0.1:8449/docs
## Эндпойнты
##### Записать поле
`POST` на ```/fields/```
##### Получить поле
`GET` на ```/fields/{field_id}```
##### Удалить поле
`DELETE` на ```/fields/{field_id}```
##### Получить изображение поля
`POST` на ```/fields/{id}/image/{band}```
Параметр band принимает 2 значения - 4 и 8, т.к. именно они нужны для расчета NDVI
##### Получить значение NDVI для поля
`POST` на ```/fields/{id}/ndvi``` (расчет не реализован)
Подробнее [здесь](http://ec2-3-122-231-1.eu-central-1.compute.amazonaws.com:8449/docs)

## TODO
- тесты
- скорее всего изображением, получаемые от API Copernicus надо обрезать под размер заданного поля
- картинки лучше хранить в базе, а не в виде файлов
- расчет reflectance по изображениям, для определения NDVI
