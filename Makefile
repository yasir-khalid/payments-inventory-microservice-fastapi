SUPPORT_LIBS := black isort flake8 autopep8

health:
	@make --version
	@python --version

freeze:
	@pip install pipreqs
	@pipreqs api/ --savepath "requirements.txt" --force --encoding=utf-8

setup: health
	@pip install -r requirements.txt
	@pip install $(SUPPORT_LIBS)

format:
	@isort -rc api/ *.py
	@autopep8 --in-place --recursive api/
	@black api/
	@flake8 api/

run: setup
	@uvicorn api.main:app --reload


