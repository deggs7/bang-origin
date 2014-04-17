APP_NAME?=bang_server

tests:
	@nosetests --with-coverage --cover-package bang_server -v

clean:
	@find . -type f -name \*.pyc -exec rm {} \;

pep8:
	@pep8 bang_server

rename:
	@perl -e "s/bang_server/$(APP_NAME)/g;" -pi $$(find . -type f)
	@mv bang_server $(APP_NAME)
