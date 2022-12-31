# rngadopt

First Python project!! Learning Python/Django and also relearning React apparently lol

- Dead simple to install docker compose setup for local dev with Django + Postgres + Vite + React

# Setup
1. Set up your `.env` --
    ```
    cp .env.example .env
    ```
2. Run the Docker container --
    ```
    docker compose up -d
    ```
3. Set up the administrator account -- Run the following command and follow the instructions.
    ```
    ./manage createsuperuser
    ```
3. Your admin account can use the following admin panel -- https://localhost:8000/admin 

# Expose
This project is compatible with Expose, if you have an Expose server.

1. Update your `.env` values --
  ```
  EXPOSE_SERVER_HOST=sharedwithexpose.com
  EXPOSE_SERVER_PORT=443
  EXPOSE_SUBDOMAIN=rngadopts
  EXPOSE_TOKEN=<FILL IN YOUR AUTH TOKEN>
  ```
2. While the project is running, expose the server --  
  ```
  ./d expose
  ```

# Troubleshooting
## ModuleNotFoundError when running `docker compose up`
```
docker compose up --build
```

# Blog
- [Setting up Docker for Django project development](https://sarahjting.com/Django-dev-docker-compose-d3e0b7d9582347fc8bf0ac3797badfdb)
- [Setting up a self-hosted Laravel Expose server](https://sarahjting.com/Setting-up-self-hosted-Expose-ngrok-1225864eb0cb4902a88b2ea2c681f134)

# References
- Django
  - [Django Docker setup](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/)
  - [Django tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/)
  - [LearnDjango](https://learndjango.com/)
  - [Django REST Framework](https://www.django-rest-framework.org/)
- React & Frontend
  - [Django/React Boilerplate](https://gist.github.com/lucianoratamero/7fc9737d24229ea9219f0987272896a2)
  - [Tailwind](https://tailwindcss.com/)
  - [Flowbite](https://flowbite.com/)