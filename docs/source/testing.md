# Running Pyevolve tests

1. Install the package with its test dependencies (from the repository root):

   ```
   pip install -e ".[test]"
   ```

2. Run tests with coverage:

   ```
   coverage run -m pytest
   ```

3. Create coverage report and it's html presentation:

   ```
   coverage report -m
   coverage html
   ```

4. Now you can find report in `htmlcov/index.html`
