# Intellireading backend

[![PyPI - Version](https://img.shields.io/pypi/v/intellireading-backend.svg)](https://pypi.org/project/intellireading-backend)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/intellireading-backend.svg)](https://pypi.org/project/intellireading-backend)
[![GitHub - Lint](https://github.com/0x6f677548/intellireading-backend/actions/workflows/lint.yml/badge.svg)](https://github.com/0x6f677548/intellireading-backend/actions/workflows/lint.yml)
[![GitHub - Test](https://github.com/0x6f677548/intellireading-backend/actions/workflows/test.yml/badge.svg)](https://github.com/0x6f677548/intellireading-backend/actions/workflows/test.yml)

Intellireading backend represents a server that exposes the Intellireading Library through FastAPI and that is the backend of the [Intellireading website](https://intellireading.com/).

If you are looking to metaguide an EPUB file, you may visit the [Intellireading website](https://intellireading.com/) and upload your file there or, alternatively, you can use the Intellireading CLI, which is a command-line tool that is part of the Intellireading library.

If you want to know more about the Intellireading Library, please visit the [Intellireading Library repository](https://github.com/0x6f677548/intellireading-cli).


## What is Epub Metaguiding?
**Metagu**iding **i**s **a** **techn**ique **th**at **ca**n **b**e **us**ed **t**o **impr**ove **yo**ur **read**ing **foc**us **an**d **spe**ed **(some**times **cal**led **Bio**nic **Readi**ng). **I**t **i**s **bas**ed **o**n **th**e **id**ea **th**at **yo**u **ca**n **us**e **a** **vis**ual **gui**de **t**o **he**lp **yo**ur **ey**es **foc**us **o**n **th**e **te**xt **yo**u **ar**e **read**ing. **I**n **th**is **cas**e, **th**e **vis**ual **gui**de **i**s **do**ne **b**y **bold**ing **a** **pa**rt **o**f **th**e **tex**t, **crea**ting **vis**ual **anch**ors **th**at **yo**ur **ey**es **ca**n **us**e **t**o **foc**us **o**n **th**e **tex**t. **Th**is **i**s **simi**lar **t**o **th**e **wa**y **a** **fin**ger **ca**n **b**e **us**ed **t**o **gui**de **yo**ur **ey**es **alo**ng **a** **li**ne **o**f **tex**t, **whi**ch **ha**s **be**en **sho**wn **t**o **impr**ove **read**ing **spe**ed **an**d **foc**us. ([**stu**dy: **"Do**es **finger-t**racking **poi**nt **t**o **chi**ld **read**ing **strate**gies"](https://ceur-ws.org/Vol-2769/paper_60.pdf))

**Howe**ver, **unl**ike **a** **fing**er, **th**e **vis**ual **gui**de **i**s **no**t **distra**cting, **an**d **i**t **ca**n **b**e **us**ed **t**o **gui**de **yo**ur **ey**es **alo**ng **mult**iple **lin**es **o**f **te**xt **a**t **onc**e. **Th**is **all**ows **yo**u **t**o **re**ad **fast**er, **an**d **wi**th **le**ss **effo**rt.

**Metagu**iding **i**s **partic**ulary **use**ful **fo**r **peo**ple **wi**th **dysl**exia **o**r **ADH**D, **bu**t **i**t **ca**n **b**e **us**ed **b**y **any**one **wh**o **wan**ts **t**o **impr**ove **the**ir **read**ing **foc**us **an**d **spe**ed. **Fo**r **mo**re **inform**ation, **vis**it **th**e [**Intelli**reading **webs**ite.](https://intellireading.com/)


## Developing - build and run

### start all docker containers with all project components  (except dev profile)
attached mode:
`docker compose up`

detached mode:
`docker compose up -d`

### start all docker containers with all project components (including dev profile)
attached mode:
`docker compose --profile dev up`

detached mode:
`docker compose --profile dev up -d`

stoping all containers, rebuild images and start all containers again:
`docker compose down && docker compose build && docker compose up`

deleting ALL docker images & containers and starting from scratch:
`docker compose down -v --rmi all && docker compose up -d`

deleting ALL docker images & containers and starting from scratch (including dev profile):
`docker compose --profile dev down -v --rmi all && docker compose --profile dev up -d`

### using client docker image
attaching to the shell of a running client image
`docker attach client`
(detach using ctrl+p ctrl+q)

running a new client image and attaching to its shell
`docker run --rm -it client`


### testing

#### Calling the api_server using curl (from the test directory)

`curl -X POST http://localhost:81/metaguiding/epub/transform -H "accept: application/json" -H "Content-Type: multipart/form-data" -H "X-API-KEY: 123" -F "file=@test_data/input/400files.epub;type=application/epub+zip"  -o test_data/output/test.epub -w "\n\rx-response-time: %{time_total}s\n\rstatus-code: %{http_code}\n\r"`

(using api-key in the query string)
`curl -X POST http://localhost:80/metaguiding/epub/transform?api-key=myapikey -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@test_data/input/400files.epub;type=application/epub+zip"  -o /dev/null -w "\n\rx-response-time: %{time_total}s\n\rstatus-code: %{http_code}\n\r`


## troubleshooting
### docker
#### diagnosing a docker container that keeps restarting
`docker logs --tail 50 --follow --timestamps <container_name>`

### goaccess log analyzer
#### analyzing the api_server access log
sudo goaccess .log/api_server/unit-access.log --log-format='%h %e %^[%d:%t %^] %v "%r" %s %b "%R" "%u" %^' --date-format='%d/%b/%Y' --time-format='%H:%M:%S'

#### analyzing the api_proxy access log
##### api.intellireading.com
sudo goaccess .log/api_proxy/api.intelireading.com.nginx-access.log --log-format='%h %e %^[%d:%t %^] %v "%r" %s %b "%R" "%u" %^' --date-format='%d/%b/%Y' --time-format='%H:%M:%S'
#### general nginx access log
sudo goaccess .log/api_proxy/nginx-access.log --log-format='%h %e %^[%d:%t %^] %v "%r" %s %b "%R" "%u" %^' --date-format='%d/%b/%Y' --time-format='%H:%M:%S'


### mapping a local folder to a remote folder on the server
 Ensure you have a config file in ~/.ssh/config with the following content:
 ``` language=bash
    Host server
        HostName <server ip address>
        User <username>
        IdentityFile ~/.ssh/<private key file>
 ```
Then, execute the following command:
``` language=bash
    sshfs user@server:/home/user /mnt/c/temp/user
```
where:
- user is the username
- server is the server name or ip address
- /home/user is the remote folder
- /mnt/c/temp/user is the local folder

### mapping a local port to a remote port on the server
`ssh -L 8080:localhost:80 user@server -i ~/.ssh/private_key_file`
where:
- user is the username
- server is the server name or ip address
- private_key_file is the private key file
- 8080 is the local port
- 80 is the remote port
- localhost is the remote host to be used (in this case, the same as the local host)

 then you can access the remote server using [http://localhost:8080](http://localhost:8080)
