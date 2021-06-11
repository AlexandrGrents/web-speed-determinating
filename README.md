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

![detect example](https://github.com/AlexandrGrents/web-speed-determination/tree/main/files/example.gif)

### Информация о деталях проекта:

[Приложение для распознавания скорости по видео](https://github.com/AlexandrGrents/determining_vehicle_speed)

[Улучшенная реализация алгоритма SORT](https://github.com/AlexandrGrents/sort)
