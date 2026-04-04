#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata inicial.json
python manage.py loaddata materias_iniciais.json
python manage.py importar_provas
python manage.py collectstatic --noinput
python manage.py popular_flashcards