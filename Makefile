.PHONY: test
test:
	mkdir -p log
	python3.9 -m unittest src/*_test.py
