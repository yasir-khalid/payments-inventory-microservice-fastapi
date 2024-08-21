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

products: 
	@uvicorn api.products:app --reload --port 8000

orders: 
	@uvicorn api.orders:app --reload --port 9000

# Target that kills processes on a specific port
kill_port:
	@echo "killing all processes associated with 'port: ${port}'"
	@lsof -i :$(port) -t | xargs kill -9

kill:
	@$(MAKE) port=8000 kill_port
	@$(MAKE) port=9000 kill_port

