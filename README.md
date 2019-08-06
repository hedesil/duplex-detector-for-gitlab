# Duplicity detector for GitLab repositories
Are you tired of handling many repositories in GitLab and that developers double every time they need new functionality?

This application connects to GitLab API by token authentication to search projects by a criteria array and returns a 
json object with each repository and its possible coincidences with other finded repositories.   

NOTE: Comments in source code are in spanish, I will translate it soon.

## Getting started


### Prerequisites

- Python version:
    - 2.7 or higher

### Installing

You need to install the following packages before you can run the project:

- Packages:

    - python-gitlab (version 1.9.0)
    
        ```
        pip install --upgrade python-gitlab
        ```
    - fuzzywuzzy (version 0.17.0)
    
        ```
        pip install --upgrade fuzzywuzzy
        ```
    - python-Levenshtein (optional, provides a 4-10x speedup in String Matching)
    
        ```
        pip install --upgrade python-Levenshtein
        ```

### Running the program

When you have installed the packages above and introduced your GitLab credentials, search criteria and modified one 
method commented in the source, you can run the application by executing:

  ```
        python main.py
   ```

The list with GitLab repositories and its possible coincidences will appears in the command prompt.

## Running the tests

I don't write unit test yet **:-(**


## Deployment



## Built With

* [GitlabPython](https://python-gitlab.readthedocs.io/en/stable/) - The main module used
* [Fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) - The other main module used

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of 
conduct, and the process for submitting pull requests to me.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Author

* **Mariano Moreno Molina** - *Initial work* - [Hedesil](https://github.com/hedesil)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
