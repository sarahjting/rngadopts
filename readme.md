# rngadopt

First Python project!! Learning Python/Django and also relearning React apparently lol

FlightRising-style color-wheel adoptable pet generator for use by the gacha adopt Discord community. Users can log into the web panel and upload files to build a pet generator, which can then be triggered by a Discord bot authorized to their Discord account.

Web-based admin panel paired with a Discord bot for daily use.

- Docker compose setup (Django, Postgres, Vite/NPM, Laravel Expose containers)
- SPA (Django REST API for the backend, React/Tailwind/Flowbite for the frontend)
- Discord login (allauth)
- Image manipulation with Python Pillow 
- Discord bot integration

# Screenshots
| | | | |
|-|-|-|-|
| ![Admin panel screenshot](https://user-images.githubusercontent.com/58196030/210177857-7e2732cb-bb6e-4e04-83f8-b4fc2f43b149.png)  | ![Admin panel screenshot](https://user-images.githubusercontent.com/58196030/210177927-f1e7ab8b-e6bf-4cd5-abcf-4cb0714218b4.png) | ![Color pool dashboard screenshot](https://user-images.githubusercontent.com/58196030/210177866-fbbfad2d-a74b-4e97-8bed-9805a80cc407.png)  | 
| ![Discord screenshot](https://user-images.githubusercontent.com/58196030/210177879-8ab3cf10-1840-43a5-8697-ec0dca4f36c4.png) | ![Admin panel screenshot](https://user-images.githubusercontent.com/58196030/210177953-23e49140-4f29-4c41-bb15-5d5ef799bef8.png) | ![Gene screenshot](https://user-images.githubusercontent.com/58196030/210177875-752eae3b-9801-4f93-ae2d-08230c38f5cd.png) |


# Client documentation
- [RNGAdopts how-to-use](https://bloom-steel-03a.notion.site/RNGAdopts-Client-Guide-a3703a9899064d8d907c2acf04b06dcd)

# Dev/self hosted setup
1. Set up your `.env` --
    ```
    cp .env.example .env
    ```
1. Run the Docker container --
    ```
    docker compose up -d
    ```
1. Migrations --
    ```
    ./d manage migrate
    ```
1. Build assets --
   ```
   ./d build
   ```
1. Set up the administrator account. Run the following command and follow the instructions. 
    ```
    ./d manage createsuperuser
    ```    
1. Admin panel at https://localhost:8000/admin/ -- log in using the above credentials and create your Site + Discord social application to get Discord login working. 
1. Dashboard should now be available at https://localhost:8000/
1. Run the discord bot to start serving adopts --
   ```
   ./d manage runbot
   ```

##  Expose
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

# Blog posts
- [Setting up Docker for Django project development](https://sarahjting.com/Django-dev-docker-compose-d3e0b7d9582347fc8bf0ac3797badfdb)
- [Setting up a self-hosted Laravel Expose server](https://sarahjting.com/Setting-up-self-hosted-Expose-ngrok-1225864eb0cb4902a88b2ea2c681f134)
- [Django notes & learnings](https://sarahjting.com/Setting-up-self-hosted-Expose-ngrok-1225864eb0cb4902a88b2ea2c681f134)

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