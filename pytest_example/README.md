# PyTest example
Example tests that make use of the pytest library.

&nbsp;
# Setup
Create the environment based off the the requirements.txt file located in the project root. Then, cd into this folder.

&nbsp;
# Directory Structure
* `advanced`
  * More extreme tests, have a heavy focus on fixtures
* `intro`
  * Simpler tests with minimal setup / tear down elements
* `conftest`
  * PyTest config file
  * Sets up fixtures to be used across the entire project

&nbsp;
# Run Tests
## In Terminal
### All
```shell
pytest
```

### Single Directory
```shell
pytest <directory>

example
pytest intro
```

### Single File
```shell
pytest <file_path>

example
pytest intro/test_intro.py
```

### Single Function
```shell
pytest <file_path> -k "<function>"

example
pytest intro/test_intro.py -k "update_with_id"
```