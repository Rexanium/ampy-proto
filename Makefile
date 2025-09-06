.PHONY: gen lint build test py-build py-install cpp-build clean

gen:
	buf generate proto

lint:
	buf lint proto

build:
	buf build proto

test:
	PYTHONPATH=gen/python python tests/roundtrip/python_roundtrip.py

py-build: gen
	python -m build

py-install:
	pip install --force-reinstall dist/ampy_proto-*.whl

cpp-build:
	cmake -S gen/cpp -B build/cpp
	cmake --build build/cpp -j

clean:
	rm -rf gen/go gen/python gen/cpp build dist *.egg-info
