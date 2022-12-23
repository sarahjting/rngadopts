# rngadopt

babby's first python project!! learning django

FlightRising-style colorwheel RNG pet generator. 

- Dead simple to install docker compose setup for local dev with Python3 + Postgres

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
3. Go to https://localhost:8000/admin -- This admin panel is for the superadmin only. 

# References
- [Django docker setup](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/)
- [Django tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/)
- [LearnDjango](https://learndjango.com/)