# luchanos_oxford_university

Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:

```
alembic init migrations
```

После этого будет создана папка с миграциями и конфигурационный файл для алембика.

- В alembic.ini нужно задать адрес базы данных, в которую будем катать миграции.
- Дальше идём в папку с миграциями и открываем env.py, там вносим изменения в блок, где написано 

```
from myapp import mymodel
```

- Дальше вводим: ```alembic revision --autogenerate -m "comment"``` - делается при любых изменениях моделей
- Будет создана миграция
- Дальше вводим: ```alembic upgrade heads```

Для того, чтобы во время тестов нормально генерировались миграции нужно:
 - сначала попробовать запустить тесты обычным образом. с первого раза все должно упасть
 - если после падения в папке tests создались алембиковские файлы, то нужно прописать туда данные по миграхам
 - если они не создались, то зайти из консоли в папку test и вызвать вручную команды на миграции, чтобы файлы появились
