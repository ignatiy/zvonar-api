<h4 align="center">Zvonar API </h4>

<p align="center">Проект автообзвона номеров через asterisk. Позволяет обзвонить Ваших клиентов за короткие сроки, не напрягая при этом call-центр.</p>
<p align="center">На данный момент проект сырой. НО(!!!), можно пользоваться в таком виде каком есть.</p>

<hr align="center"/>

<p align="center">
	<img src="https://img.shields.io/pypi/pyversions/apache-airflow.svg">
</p>


**Что умеет:**
- [x] Обзвон списка номеров в несколько каналов (сколько позволяет SIP).
- [x] Формирование и выгрузка отчета в csv файл. 
- [x] Отправка отчета на почту.
- [x] Отправка SMS сообщения (опционально).

**Как запустить API:**
Первым делом клонируем проект и переходим в директорию проекта
```
git clone git@github.com:ignatiy/zvonar-api.git
cd zvonar-api/
```

Создаем виртуальное окружение
```
python3 -m venv env
```

Активируем его
```
source env/bin/activate
```

Устанавливаем зависимости проекта
```
pip3 install -r requirements.txt
```

Деактивируем виртуальное окружение. Больше оно нам не понадобится
```
deactivate
```

Переходим к настройкам
```
cd zvonar-api/app
```

Тут необходимо в файле `config.py` указать свой логин и пароль.
Также указываем директорию куда будем складывать файлы созданные api

Редактируем `zvonar.service`. Меняем пути в `WorkingDirectory`, `Environment` и `ExecStart` на свои.

Добавляем в автозагрузку
```
ln -s zvonar-api/app/zvonar.service /etc/systemd/system/
```
Включаем
```
sudo systemctl enable zvonar
```