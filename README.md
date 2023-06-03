![Project Screenshot](cire.png)

Uncover the brilliance: Explore profiles, groundbreaking work, and cutting-edge research by the exceptional minds of Coventry University.


## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Note](note)

## Overview
The Coventry PureHuB Search Engine is a web application that allows users to search for research publications and authors affiliated with Coventry University. The application utilizes natural language processing techniques, such as stemming and TF-IDF and other technique like inverse indexer to provide accurate search results in a user friendly manner.


## Features

- Research Publication Search: Users can search for research publications by entering relevant keywords or phrases. The search engine employs advanced techniques such as stemming and TF-IDF to match the user's query with the indexed publication data accurately.
- 
- Author Search: Users can also search for specific authors by their names or related keywords. The search engine applies the same advanced techniques to match the user's input with the indexed author data.
Stemming and TF-IDF: The search engine utilizes stemming to reduce words to their base or root form, enabling broader search coverage. Additionally, the application employs TF-IDF to calculate the importance of each term in the documents and generate relevance scores for accurate ranking of search results.

- Inverse Indexer: The search engine includes an inverse indexer that indexes and stores the publication and author data in a structured manner, enabling efficient retrieval and retrieval of relevant information.



![Light mode](CPhub.png)


## Installation
1. Clone the repository:
   
   `git clone https://github.com/maladeep/Coventry-PureHub-Search-Engine.git`

2. Install the required dependencies:
   
   `pip install -r requirements.txt`

## Usage
 [Run Live App](https://maladeep-coventry-purehub-search-engine-app-okesr5.streamlit.app/)
 
 or 
 1. Run locally 
 
   `Streamlit run clone https://github.com/maladeep/Coventry-PureHub-Search-Engine.git`
 
2. Open the provided URL in your web browser.
3. Enter your search query, select the search filter and search type, and click the "SEARCH" button.
4. View the search results displayed in cards.
5. Scroll down to view more search results.

## Dependencies

The project has the following vital dependencies:

The Coventry PureHub Search Engine relies on the following dependencies:

- streamlit: The web application framework used for building the user interface.
- Pillow: A library for opening and manipulating images, used to display an image in the streamlit application.
- ujson: A fast JSON encoder and decoder library, used to load JSON data.
- scikit-learn: A machine learning library, used for text preprocessing, TF-IDF vectorization, and cosine similarity calculation.
- nltk: The Natural Language Toolkit, used for tokenization, stemming, and stop-word removal.
- numpy: A powerful library for numerical computations in Python.
- pandas: A data manipulation library, used for handling and processing structured data.
- seaborn: A data visualization library, used for creating attractive and informative plots.
- matplotlib: A versatile plotting library, used for generating various types of charts and graphs.
- scikit-multilearn: A library for multi-label classification, used for advanced search features.
- requests: A library for making HTTP requests, used for fetching external resources.
- beautifulsoup4: A library for web scraping, used for extracting data from web pages.
- selenium: A library for web automation, used for interacting with web pages.
- webdriver_manager: A library for managing web drivers, used for browser automation.

## Contributing

Contributions to this project are welcome. If you find any issues or would like to suggest improvements, please open an issue or submit a pull request. 

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Note
This work is done for the partial fulfillment of STW7071CEM Information Retrieval coursework provided by Coventry University. 
