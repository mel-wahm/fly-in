PY= python
FILE = maps/easy/01_linear_path.txt
install:
	@pip install pydantic arcade


run:
	@echo "\033[92mRunning Fly-IN...\033[0m"
	@uv run $(PY) fly-in.py $(FILE)


debug:
	@echo "\033[92mDebug mode activated...\033[0m" 
	@pdb3 fly-in.py


clean:
	@echo "\033[92mCleaning up..."
	@rm -rf .mypy_cache
	@rm -rf __pycache__


lint:
	@echo "\033[92mChecking Flake8 and Mypy ...\033[0m'"
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@flake8 . --exclude=.venv
