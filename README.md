![Intellireading.com](https://raw.githubusercontent.com/0x6f677548/intellireading-www/main/src/img/intellireading.png)
# API Server for Intellireading CLI

[![GitHub - Stars](https://img.shields.io/github/stars/0x6f677548/intellireading-api_server.svg?style=social&label=Stars)](
[![PyPI - Version](https://img.shields.io/pypi/v/intellireading-cli.svg)](https://pypi.org/project/intellireading-cli)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/intellireading-cli.svg)](https://pypi.org/project/intellireading-cli)
[![Deploy to GHCR](https://github.com/0x6f677548/intellireading-api_server/actions/workflows/build-and-publish-to-ghcr.yml/badge.svg)](https://github.com/0x6f677548/intellireading-api_server/actions/workflows/build-and-publish-to-ghcr.yml)
[![Deploy](https://github.com/0x6f677548/intellireading-api_server/actions/workflows/deploy-to-dockerhost.yml/badge.svg)](https://github.com/0x6f677548/intellireading-api_server/actions/workflows/deploy-to-dockerhost.yml)
[![GitHub - Lint](https://github.com/0x6f677548/intellireading-api_server/actions/workflows/lint.yml/badge.svg)](https://github.com/0x6f677548/intellireading-api_server/actions/workflows/lint.yml)
[![GitHub - Test](https://github.com/0x6f677548/intellireading-api_server/actions/workflows/test.yml/badge.svg)](https://github.com/0x6f677548/intellireading-api_server/actions/workflows/test.yml)

Intellireading API server exposes the [Intellireading CLI Library](https://www.github.com/0x6f677548/intellireading-cli) through FastAPI. It is the backend of the [Intellireading site](https://intellireading.com/).

Example of a text converted to a metaguided text:
![Intellireading.com](https://raw.githubusercontent.com/0x6f677548/intellireading-www/main/src/img/sample.png) 


This repo is part of the [Intellireading](https://intellireading.com/) project, which aims to help people with dyslexia, ADHD, or anyone who wants to improve their reading focus and speed. 

## [Other Intellireading Code Repositories](https://github.com/stars/0x6f677548/lists/intellireading)
- [Intellireading site](https://www.github.com/0x6f677548/intellireading-www), which allows anyone to convert an EPUB to the metaguided version.
- [API Server](https://www.github.com/0x6f677548/intellireading-api_server), that support the Intellireading site.
- [Command-Line tool](https://www.github.com/0x6f677548/intellireading-cli). A standalone tool and library that can be used to metaguide EPUB files.
- [Calibre Plugins](https://www.github.com/0x6f677548/intellireading-calibre-plugins). A set of plugins that can be used to metaguide EPUB files using Calibre.


## What is EPUB Metaguiding?
**Metagu**iding **i**s **a** **techn**ique **th**at **ca**n **b**e **us**ed **t**o **impr**ove **yo**ur **read**ing **foc**us **an**d **spe**ed **(some**times **cal**led **Bio**nic **Readi**ng). **I**t **i**s **bas**ed **o**n **th**e **id**ea **th**at **yo**u **ca**n **us**e **a** **vis**ual **gui**de **t**o **he**lp **yo**ur **ey**es **foc**us **o**n **th**e **te**xt **yo**u **ar**e **read**ing. **I**n **th**is **cas**e, **th**e **vis**ual **gui**de **i**s **do**ne **b**y **bold**ing **a** **pa**rt **o**f **th**e **tex**t, **crea**ting **vis**ual **anch**ors **th**at **yo**ur **ey**es **ca**n **us**e **t**o **foc**us **o**n **th**e **tex**t. **Th**is **i**s **simi**lar **t**o **th**e **wa**y **a** **fin**ger **ca**n **b**e **us**ed **t**o **gui**de **yo**ur **ey**es **alo**ng **a** **li**ne **o**f **tex**t, **whi**ch **ha**s **be**en **sho**wn **t**o **impr**ove **read**ing **spe**ed **an**d **foc**us. ([**stu**dy: **"Do**es **finger-t**racking **poi**nt **t**o **chi**ld **read**ing **strate**gies"](https://ceur-ws.org/Vol-2769/paper_60.pdf))

**Howe**ver, **unl**ike **a** **fing**er, **th**e **vis**ual **gui**de **i**s **no**t **distra**cting, **an**d **i**t **ca**n **b**e **us**ed **t**o **gui**de **yo**ur **ey**es **alo**ng **mult**iple **lin**es **o**f **te**xt **a**t **onc**e. **Th**is **all**ows **yo**u **t**o **re**ad **fast**er, **an**d **wi**th **le**ss **effo**rt.

**Metagu**iding **i**s **partic**ulary **use**ful **fo**r **peo**ple **wi**th **dysl**exia **o**r **ADH**D, **bu**t **i**t **ca**n **b**e **us**ed **b**y **any**one **wh**o **wan**ts **t**o **impr**ove **the**ir **read**ing **foc**us **an**d **spe**ed. **Fo**r **mo**re **inform**ation, **vis**it **th**e [**Intelli**reading **webs**ite.](https://intellireading.com/)

# Architecture
This project is also a playground for my FastAPI-bootstrap, which is a project template that includes a lot some best practices and tools that I use in my FastAPI projects. You can find more information about the bootstrap in the [FastAPI-bootstrap repository](http://www.github.com/0x6f677548/fastapi-bootstrap).
A typical deployment would be composed of the following containers:
- **api-proxy**: An NGINX server that acts as a reverse proxy for api-server (FastAPI). 
- **api-server**: A FastAPI server that exposes the Intellireading CLI library through a REST API and is instrumented with OpenTelemetry, sending traces, metrics, and logs to an otel-collector.
- **otel_collector**: An OpenTelemetry collector that exposes syslog and otel endpoints to receive logs, traces, and metrics from the api-proxy and api-server and forwards them to a remote OTEL compliant backend, which may be Jaeger, Prometheus, New Relic, Datadog, or any other backend that supports the OpenTelemetry protocol.
 
## Other components
Some of the tools and libraries used in this project are:
- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Hatch**: A modern project, package, and virtual env manager for Python.
- **OpenTelemetry**: A set of APIs, libraries, agents, and instrumentation to provide observability.