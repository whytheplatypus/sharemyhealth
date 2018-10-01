# ShareMyHealth

A consumer-directed health information exchange.

This application is built using Python 3.7 and Django 2.1.x.

The default port for this application is 8001. This avoids 
conflicts when running the OIDC Server on the same machine.

Docker is supported. Run docker with:

     docker-compose -f .development/docker-compose.yml up
     
If you make changes to requirements.txt to add libraries re-run 
docker-compose with the --build option.


