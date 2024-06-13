# MonitorSSINDEX
Model LLM for scoring pillar in a NLP.


## Code Quality checks with docker.

> Run `docker-compose up -d --build` from console.
>
> In case you want to see the logs, run `docker-compose logs --follow`

Once the container is running, there are 3 commands:

* Code Formatting: `docker-compose exec dash_app black . -S`
* Maintainability Index (Closer to 100% is better): `docker-compose exec dash_app radon mi .`
* Code Complexity (Lower is better): `docker-compose exec dash_app radon cc .`
