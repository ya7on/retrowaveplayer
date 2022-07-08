install:
	virtualenv venv ; ./venv/bin/pip3 install -r requirements.txt

play:
	./venv/bin/python3 retrowave.py

download:
	./venv/bin/python3 compare.py