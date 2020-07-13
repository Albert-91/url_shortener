# URL Shortener

Repository contains Django application with service getting URL from user and next hashes whole URL with Base64 encoding.
User gets hashed URL with following structure:
[SCHEME_OF_LUNCHED_SERVICE]://[DOMAIN_OF_LUNCHED_SERVICE]/[CREATED_HASH]
If user clicks above URL then it will redirect him to his previous provided URL.

### Procedures to run application

Firstly copy file with environ variables `.env_template` with new name `.env`. You can do it by command:
```bash
cp .env_template .env
```
Because of whole environment is containerized by Docker. You have to make sure that docker and docker-compose are installed.
To run pull all images, create database store directory and finally run all service run command:
```bash
docker-compose up -d
```

### Form

After running application, to get hashed URL let visit your domain. If you run it locally, you can visit `localhost:8000`.
Next provide some correct URL and click "Make shorter". One the next screen you will see new, hashed URL.

