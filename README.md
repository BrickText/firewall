# FireWall

![FireWall](./docs/img/logo.png)

FireWall is an expert system for predicting fires around the world based on weather cast data. The project is powered by machine learning algorithms and user friendly interface so that people can take advantage of all the data we have about this disasters.

## Presentation
[FireWall Presentation](https://docs.google.com/presentation/d/17Qqk8pE5YUIkOPb3wCbS2FpxyK5tPegBr9Fb8IbOQaY/edit?usp=sharing)

## How to install and run the app?

We are using **Python** as main programming languages, so we will have to set up a **Python** environment.

### Installation

1) Of course you will need to download the **Python** programming language. You can do so from [here](https://www.python.org/).

2) Now, because we are using virtual environment to manage our dependencies, you will need to download **Pipenv**.
<br> Check out [here](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) to understand how to do so.

3) Clone/download this repository on you local machine.
<br> Run this in your terminal to clone the repo.
    ```bash
    git clone https://github.com/BrickText/firewall
    ```

4) Once you have installed **Pipenv** you are ready to install the requirements specified in the `Pipfile`.
<br>Navigate to the root directory (```cd ./firewall```) of the project and run the following:
    ```bash
    pipenv install
    ```

5) Good Job! Now you are all setup to run the app.

### Running

* Navigate to the `firewall/webbapp` directory and run the following:
    ```bash
    pipenv run python manage.py runserver
    ```
    Wait till something like this is shown:
    ```
    System check identified no issues (0 silenced).
    January 23, 2019 - 22:21:52
    Django version 2.1.5, using settings 'webapp.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    ```
    Now the server is run. You can go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Built With

* [Django](https://www.djangoproject.com/) - The web framework
* [NumPy](http://www.numpy.org/) - Fundamental package for scientific computing with Python
* [Scikit-Learn](https://scikit-learn.org/stable/) - Machine Learning in Python
* [XGBoost](https://xgboost.readthedocs.io/en/latest/) - Gradient Boosting framework

## Authors

* **Victor Velev** - *Initial work* - [VIVelev](https://github.com/VIVelev)
* **Nikolay Stanishev** - *Initial work* - [nikolaystanishev](https://github.com/nikolaystanishev)
* **Ivan Milev** - *Initial work* - [ivanmilevtues](https://github.com/ivanmilevtues)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
