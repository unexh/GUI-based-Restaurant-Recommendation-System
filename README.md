# Brasserie-App

This project implements a Restaurant Recommendation System using AI./the search algorithm used here is a __content-based-filtering__ technique. Which takes city, locality and restaurant name and generates a similarity score index. The search results would then be shown based on generated similarity score index .

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things (libraries) you need to run the program and how to install them

```
1. PyQt5
2. NLTK
3. pandas
5. sklearn
5. numpy
```

### Installing

A step by step series of commands that will help your development env running.

Use Python 3.7 :

```
pip install pyqt5
pip install pyqt5-tools
pip install nltk
pip install sklearn
```

After Installing ntlk, do

```
import nltk
nltk.download()
```

Download all the data shown.


## Running the program

Just open your terminal, head to cloned directory, do:

```
python Brasserie-App.py
```

Note: __/python__ must be added to your system's Global path

### Using Brasserie App

To get a recommendation from the app, user can follow two pathways:

```
1. By Entering Restaurant Details (like city, locality and restaurant name).
2. By Selecting one of the Top Recommended Restaurant.
```

After filling the details above specified, user will be given its recommendation by searching and generating a
similarity score index and top five recommendations will be shown.


## Built With

* [PyQT5](https://pypi.org/project/PyQt5/) - The GUI framework used

## Authors

* **Nishant Pandey** - *Initial work* - [unexh](https://github.com/unexh)
* **Sehajbir Thind** - *Initial work* - [SehajbirThind](https://github.com/SehajbirThind)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Acknowledgments

* Inspiration : [Nagesh Singh Chauhan](https://medium.com/analytics-vidhya/how-to-build-a-restaurant-recommendation-engine-part-1-21aadb5dac6e)
