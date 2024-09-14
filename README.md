# intellireading

## Lint Status
[![GitHub Super-Linter all codebase](https://github.com/0x6f677548/intellireading/actions/workflows/lint-super-linter-all-codebase.yml/badge.svg)](https://github.com/0x6f677548/intellireading/actions/workflows/lint-super-linter-all-codebase.yml)
[![GitHub Super-Linter](https://github.com/0x6f677548/intellireading/actions/workflows/lint-super-linter.yml/badge.svg)](https://github.com/0x6f677548/intellireading/actions/workflows/lint-super-linter.yml)

## Deploy Status
[![Deploy to GCP](https://github.com/0x6f677548/intellireading/actions/workflows/deploy-server.yml/badge.svg)](https://github.com/0x6f677548/intellireading/actions/workflows/deploy-server.yml)
[![Deploy to Clouflare](https://github.com/0x6f677548/intellireading/actions/workflows/deploy-www.yml/badge.svg)](https://github.com/0x6f677548/intellireading/actions/workflows/deploy-www.yml)
[![Deploy to ghcr.io](https://github.com/0x6f677548/intellireading/actions/workflows/build-containers.yml/badge.svg)](https://github.com/0x6f677548/intellireading/actions/workflows/build-containers.yml)



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

### activate environment
`source ~/intellireading/.virtualenv/bin/activate`

### run the api_server locally using uvicorn
`uvicorn main:app --reload --lifespan on`

### run the api_server locally using uvicorn and loading env variables from .env
`uvicorn main:app --reload --lifespan on --env-file ../../.env`


### testing

#### Calling the api_server from client
Using a  fully local hosted env:
(make sure you are in the client/cli directory)
`python call-metaguide_epub.py ../../test/test_data/input/400files.epub ../../test/test_data/output/test.epub http://localhost:80/metaguiding/epub/transform`

using the client docker image (api_proxy)
`python call-metaguide_epub.py ../../test/test_data/input/400files.epub ../../test/test_data/output/test.epub http://api_proxy/metaguiding/epub/transform`

#### metaguiding an individual file
(client directory)
`python metaguide_epub.py ../../test/test_data/input/400files.epub ../../test/test_data/output/test.epub`

using curl:
(store the output in a file - execute from the test directory)
`curl -X POST http://localhost:80/metaguiding/epub/transform -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@test_data/input/400files.epub;type=application/epub+zip"  -o test_data/output/test.epub -w "\n\rx-response-time: %{time_total}s\n\rstatus-code: %{http_code}\n\r"`

`curl -X POST http://localhost:80/metaguiding/epub/transform -H "accept: application/json" -H "Content-Type: multipart/form-data" -H "X-API-KEY: myapikey" -F "file=@test_data/input/400files.epub;type=application/epub+zip"  -o test_data/output/test.epub -w "\n\rx-response-time: %{time_total}s\n\rstatus-code: %{http_code}\n\r"`



(don't store the output)
`curl -X POST http://localhost:80/metaguiding/epub/transform -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@test_data/input/400files.epub;type=application/epub+zip"  -o /dev/null -w "\n\rx-response-time: %{time_total}s\n\rstatus-code: %{http_code}\n\r"`

(using api-key in the query string)
`curl -X POST http://localhost:80/metaguiding/epub/transform?api-key=myapikey -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@test_data/input/400files.epub;type=application/epub+zip"  -o /dev/null -w "\n\rx-response-time: %{time_total}s\n\rstatus-code: %{http_code}\n\r`

(using api-key in the header)
`curl -X POST http://localhost:80/metaguiding/epub/transform -H "accept: application/json" -H "Content-Type: multipart/form-data" -H "X-API-KEY: myapikey" -F "file=@test_data/input/400files.epub;type=application/epub+zip"  -o /dev/null -w "\n\rx-response-time: %{time_total}s\n\rstatus-code: %{http_code}\n\r`


#### metaguiding all epub files in a directory
(client directory)
`python metaguide_epub_dir.py ../../test/test_data/input/`



## deploy
### all services in the same host
.env.prod should be updated
`docker compose --env-file .env.prod up -d`


### service by service deploy
(replace "api_server" by the desired service to deploy)

rebuild the images
`docker compose --env-file .env.prod build api_server`
deploy and run the container without dependencies
`docker compose --env-file .env.prod up --no-deps -d api_server`

### generate deploy folder
(not deleting files that are not in the source folder)
`rsync -av --exclude-from=rsync-exclusions ./ /mnt/c/temp/intellireading`
(deleting files that are not in the source folder)
`rsync -av --delete --exclude-from=rsync-exclusions ./ /mnt/c/temp/intellireading`

(create a ZIP file from the deploy folder named "intellireading.ZIP", but not including the deploy folder itself)
`zip -r /mnt/c/temp/intellireading.zip /mnt/c/temp/intellireading`

### how to create a server release and deploy it

1) update API_SERVER_VERSION in .env and .env.prod
2) run the script to create the server release
`./create-server-release.sh` . This will create a ZIP file named "intellireading-server-<version>.ZIP" in the "releases\<version>" folder
3) copy the ZIP file to the server
4) stop all running containers with `docker compose --env-file .env.prod down`
5) rename the intellireading folder to intellireading.old
6) unzip the new release file to a new intellireading folder executing `unzip intellireading-server-<version>.zip -d intellireading`
7) copy the .env.prod file from the old intellireading folder to the new intellireading folder. Verify that .env.prod has the correct values for the new release, namely the correct version number
8) move all logs from the old intellireading folder to the new intellireading folder, using the same folder structure
9) start the containers with `docker compose --env-file .env.prod up -d`

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

### view logs
Logs are sent to otel_collector, that should fwd to new-relic.

### connecting to the host server
`ssh user@server -i ~/.ssh/private_key_file`
where:
- user is the username
- server is the server name or ip address
- private_key_file is the private key file

 If the server is hosted in GCP, make sure the public key is added to the project metadata and mapped to the username

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
