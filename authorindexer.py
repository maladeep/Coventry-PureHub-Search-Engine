import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import ujson

# Load the JSON file containing scraped results
with open('scraper_results.json', 'r') as doc:
    scraper_results = doc.read()

# Extract author names from the JSON data
authors = []
data_dict = ujson.loads(scraper_results)
for item in data_dict:
    authors.append(item["cu_author"])

# Write the author names to a JSON file
with open('author_names.json', 'w') as f:
    ujson.dump(authors, f)

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

# Load the JSON file containing author names
with open('author_names.json', 'r') as f:
    author_data = f.read()

# Load JSON data
authors = ujson.loads(author_data)

# Preprocess the author names
stop_words = stopwords.words('english')
stemmer = PorterStemmer()
authors_list_first_stem = []
authors_list = []

for author in authors:
    words = word_tokenize(author)
    stem_word = ""
    for word in words:
        if word.lower() not in stop_words:
            stem_word += stemmer.stem(word) + " "
    authors_list_first_stem.append(stem_word)
    authors_list.append(author)

# Indexing process
data_dict = {}
for i in range(len(authors_list_first_stem)):
    for word in authors_list_first_stem[i].split():
        if word not in data_dict:
            data_dict[word] = [i]
        else:
            data_dict[word].append(i)

# Write the preprocessed author names and indexed dictionary to JSON files
with open('author_list_stemmed.json', 'w') as f:
    ujson.dump(authors_list_first_stem, f)

with open('author_indexed_dictionary.json', 'w') as f:
    ujson.dump(data_dict, f)