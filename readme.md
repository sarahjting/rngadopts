# rngadopt

babby's first python project!! learning django and also relearning react apparently lol

FlightRising-style colorwheel RNG pet generator. 

- Dead simple to install docker compose setup for local dev with Django + Vite + Postgres

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

# References
- [Django Docker setup](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/)
- [Django tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/)
- [LearnDjango](https://learndjango.com/)
- [Django/React Boilerplate](https://gist.github.com/lucianoratamero/7fc9737d24229ea9219f0987272896a2)