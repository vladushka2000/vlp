# Сервис построения VLP
Учебный сервис в рамках разработки тестового приложения школы "Айти в нефти"

**С заданием можно ознакомиться в файле [TASK.md](TASK.md)**

Инструкция по настройке среды для разработки:
Работаем из корневого каталога

1) Создайте виртуальное окружение
```bash
python -m venv venv
```
2) Активируйте его, также выберите его в настройках
`Pycharm Settings/Project/Python Intepreter`,
чтобы оно автоматически подхватывалось
```bash
venv\Scripts\activate
```
3) Установите необходимые библиотеки
```bash
pip install -r requirements.txt
```
4) Запустите файлик `src/main.py` через pycharm или командой
```bash
python src/main/py
```
5) Теперь приложение запущено и доступно по адресу `localhost:8001/docs`

Для создания и запуска контейнера с БД необходимо запустить сервис postgres в папке:
`docker/docker-compose.yml`

**Команды для работы с миграциями (из корневого каталога):**
1) Создать миграцию:
```bash
alembic revision --autogenerate -m "initial_migration" 
```
2) Накатить миграцию на БД:
```bash
alembic upgrade head
```

Сделать дамп/накатить дамп:
1) Накатить дамп:
Лучше запускать с пустой схемой с помощью command prompt, иначе криво накатывается 
```bash
docker exec -i vlp-postgres psql -U vlp -v -d vlp < dump.sql
```
2) Создать дамп:
```bash
docker exec -i vlp-postgres pg_restore -U vlp -v -d vlp < dump.sql
``` 