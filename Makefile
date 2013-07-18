APP_NAME?=shibeidao

tests:
	@nosetests --with-coverage --cover-package shibeidao -v

clean:
	@find . -type f -name \*.pyc -exec rm {} \;

pep8:
	@pep8 shibeidao

rename:
	@perl -e "s/shibeidao/$(APP_NAME)/g;" -pi $$(find . -type f)
	@mv shibeidao $(APP_NAME)
