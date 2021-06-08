Нужен nvidia-docker и docker-compose 1.28.0+ (пример установки - [тут](https://docs.docker.com/compose/install/))

Веса: [model_final.pth](https://drive.google.com/file/d/1m-vEyQl6vDjMW6cCnpFv7JFQY6N8GMOk/view?usp=sharing)

Установка:
```
git clone https://github.com/AlexandrGrents/web-speed-determinating.git
cd ./web-speed-determinating
git submodule init
git submodile update
```

Для запуска c docker требуется выполнить `docker-compose up --build`

### Информация о деталях проекта: 

[Сервер](https://github.com/AlexandrGrents/web-speed-determinating)

[Клиент](https://github.com/AlexandrGrents/interface-speed-determinationg)

[Ссылка для работы](https://alexandrgrents.github.io/interface-speed-determinationg/)

[Приложение для распознавания скорости по видео](https://github.com/AlexandrGrents/determining_vehicle_speed)

[Улучшенная реализация алгоритма SORT](https://github.com/AlexandrGrents/sort)