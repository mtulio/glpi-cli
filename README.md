# glpi-cli

[![Build Status](https://travis-ci.org/mtulio/glpi-cli.svg?branch=master)](https://travis-ci.org/mtulio/glpi-cli)

GLPI Command Line Interface.

Easy way to iterate with GLPI using Command Line Interface.

This CLI use this [GLPI SDK](https://github.com/truly-systems/glpi-sdk-python)

## Config

Clone this repository

`git clone https://github.com/mtulio/glpi-cli`

OR install it using pip

`pip install glpi-cli`

Setup the environment with your GLPI

```shell
export GLPI_API_URL=http://path/to/glpi/apirest.php
export GLPI_USERNAME=<Your username>
export GLPI_PASSWORD=<Your password>
export GLPI_APP_TOKEN=<Your User APP Token>
```

## Use it

* Get all Ticket items

```shell
python glpi-cli.py --item knowbase --command get_all
```

* Get an Ticket by ID

```shell
python glpi-cli.py --item knowbase --command get_all --id 10
```

* Get all Knowledge Base items filtering output with json util `jq`

```shell
python glpi-cli.py --item knowbase --command get_all |jq .[].name
```

## Get Involved

PR are always welcome. =]

Please make sure that the code have passed in following tests:

```shell
make  dependencies
make check-syntax
make install-me
```
