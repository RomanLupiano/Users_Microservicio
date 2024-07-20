# Servicio de usuarios
Este repositorio contiene el servicio de usuarios de una red social simple. El servicio maneja el registro, autenticación y perfil de los usuarios.


#### Pasos a seguir
1. python -m venv env
2. source ./env/bin/activate
3. pip install -r requirements.txt
4. cd UsersAuth/
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py runserver



### Framework y herramientas utilizados 🛠️
- [django](https://www.djangoproject.com/)
- [djangorestframework](https://www.django-rest-framework.org/)  
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

Para subir las imagenes a Google Cloud Storage:
- [google-api-python-client](https://github.com/googleapis/google-api-python-client)
- [django-storages[google]](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html)
- [Pillow](https://pypi.org/project/pillow/)  

Facilidades con el .env:
- [python-dotenv](https://pypi.org/project/python-dotenv/)