# Accurate test data in FastAPI

This is an example of a simple FastAPI server for an article on adding test
data. It is shows how to set up a temporary, in-memory database for testing,
and how to easily load test data from YAML files with type checking.


## Installing

1. Clone the repository, and `cd` into the directory.
2. Install the dependencies. This project uses Poetry, because it's vastly
   easier to use than pip.<br>
   `$ poetry install`
3. Activate the environment.<br>
   `$ poetry shell`
4. Run the tests.<br>
   `$ pytest app`
