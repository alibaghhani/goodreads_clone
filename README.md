
# Django REST goodreads project

This project is a clone of goodreads website with basic JWTauthentication

## Author

- [@AliBaghani](https://github.com/alibaghhani)


## Feedback

If you have any feedback, please reach out to us at baghaniali2006@gmail.com


## Tech Stack


**Server:** Django REST Framework

**Database:** sqlite

**Deployment** Docker, Nginx






## License

[MIT](https://choosealicense.com/licenses/mit/)



## Deployment

To deploy this project without docker 

```bash
  python -m venv env #create virtual envoirement

  source env/bin/activate  #active the venv

  pip install -r requirements.txt #install dependencies

  python manage.py runserver #run the django server
  
```

To deploy this project with nginx and docker

```bash
  docker-compose up --build  
```
