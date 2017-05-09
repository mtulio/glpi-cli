PATH_VENV=venv
PATH_REQUIREMENTS=glpi-cli/requirements.txt

.PHONY: venv
venv:
	rm -rf $(PATH_VENV)
	virtualenv $(PATH_VENV)

.PHONY: dependencies
dependencies:
	@if [ ! -d $(PATH_VENV) ]; then virtualenv $(PATH_VENV) ; fi
	. $(PATH_VENV)/bin/activate && pip install -r $(PATH_REQUIREMENTS)

.PHONY: check-syntax
check-syntax:
	. $(PATH_VENV)/bin/activate && pep8 glpi-cli/*.py

.PHONY: clean
clean:
	@if [ -d $(PATH_VENV) ]; then rm -rf $(PATH_VENV); fi
	@if [ -d $(PATH_VENV_SETUP) ]; then rm -rf $(PATH_VENV_SETUP); fi
