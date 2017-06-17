# glpi-cli

[![Build Status](https://travis-ci.org/mtulio/glpi-cli.svg?branch=master)](https://travis-ci.org/mtulio/glpi-cli)
[![PyPi Version](https://img.shields.io/pypi/v/glpi-cli.svg)](https://pypi.python.org/pypi/glpi-cli)

GLPI Command Line Interface.

Easy way to iterate with GLPI using Command Line Interface.

This CLI use this [GLPI SDK](https://github.com/truly-systems/glpi-sdk-python)

## Config

Install from repository

```
git clone https://github.com/mtulio/glpi-cli
cd glpi-cli
make install-me
```

OR install it using pip:

`pip install glpi-cli`

Setup the environment with your GLPI

```shell
export GLPI_API_URL=http://path/to/glpi/apirest.php
export GLPI_USERNAME=<Your username>
export GLPI_PASSWORD=<Your password>
export GLPI_APP_TOKEN=<Your User APP Token>
```

## USAGE

* Get all Ticket items

```shell
$ glpi-cli --item ticket --command get_all
```

* Get an Ticket by ID

```shell
$ glpi-cli --item ticket --command get_all --id 10
```

* Get all Knowledge Base Titles - filtered output with json util `jq`

```shell
$ glpi-cli --item knowbase --command get_all |jq .[].name
```

* Get Item deleted flag

```shell
$ glpi-cli -i ticket -c get -id 52 |jq .is_deleted
```

* Delete Ticket

```shell
$ glpi-cli -i ticket -c delete -id 52
```

* Update Ticket

```shell
$ glpi-cli -i ticket -c update -id 52 -p '{ "status": 5, "impact": 2}'
```

* Update Ticket, forcing

```shell
$ glpi-cli -i ticket -c update -id 52 -p '{ "status": 5, "impact": 2}' -f
```

* Update Ticket, forcing and verbosiity

```shell
$ glpi-cli -i ticket -c update -id 52 -p '{ "status": 5, "impact": 2}' -v -f
```

## Get Involved

PR are always welcome. =]

Please make sure that the code have passed in following tests:

```shell
make  dependencies
make check-syntax
make install-me
```
