# yamdb_final
yamdb_final - API-Проект YaMDb
=====================
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок высчитывается средняя оценка произведения.

Команды для запуска приложения
-----------------------------------
docker pull rutap/infra_sp2:v1.0.2021
docker run rutap/infra_sp2:v1.0.2021

### Миграции и статика
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input

### Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

### Заполнение базы начальными данными
python3 manage.py shell  
# выполнить в открывшемся терминале:
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()

python manage.py loaddata fixtures.json 


Документация по API проекта
-----------------------------------
После запуска проекта, вам будет доступна документация по API, расположенная - http://example.com/redoc/


![example workflow](https://github.com/Rutap-ru/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
