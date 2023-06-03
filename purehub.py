import streamlit as st
from PIL import Image
import ujson
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

nltk.download('stopwords')
nltk.download('punkt')

# Set up the NLTK components
stemmer = PorterStemmer()
stop_words = stopwords.words('english')
tfidf = TfidfVectorizer()

# Load the data
with open('publication_list_stemmed.json', 'r') as f:
    pub_list_first_stem = ujson.load(f)
with open('author_list_stemmed.json', 'r') as f:
    author_list_first_stem = ujson.load(f)
with open('author_names.json', 'r') as f:
    author_name = ujson.load(f)
with open('pub_name.json', 'r') as f:
    pub_name = ujson.load(f)
with open('pub_url.json', 'r') as f:
    pub_url = ujson.load(f)
with open('pub_cu_author.json', 'r') as f:
    pub_cu_author = ujson.load(f)
with open('pub_date.json', 'r') as f:
    pub_date = ujson.load(f)

# Build the inverted indexer
data_dict = {}
for i, doc in enumerate(pub_list_first_stem):
    words = set(word_tokenize(doc))
    for word in words:
        if word not in stop_words:
            stemmed_word = stemmer.stem(word)
            if stemmed_word not in data_dict:
                data_dict[stemmed_word] = []
            data_dict[stemmed_word].append(i)

def search_data(input_text, operator_val, search_type):
    output_data = {}
    if operator_val == 2:
        input_text = input_text.lower().split()
        pointer = []
        for token in input_text:
            if len(input_text) < 2:
                st.warning("Please enter at least 2 words to apply the operator.")
                break

            stem_temp = ""
            stem_word_file = []
            temp_file = []
            word_list = word_tokenize(token)

            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)

            if search_type == "publication" and data_dict.get(stem_word_file[0].strip()):
                pointer = data_dict.get(stem_word_file[0].strip())

            if len(pointer) == 0:
                output_data = {}
            else:
                for j in pointer:
                    if search_type == "publication":
                        temp_file.append(pub_list_first_stem[j])
                    elif search_type == "author":
                        temp_file.append(author_list_first_stem[j])

                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in pointer:
                    output_data[j] = cosine_output[pointer.index(j)]

    else:  # Relevant operator (OR)
        input_text = input_text.lower().split()
        pointer = []
        match_word = []
        for token in input_text:
            if len(input_text) < 2:
                st.warning("Please enter at least 2 words to apply the operator.")
                break

            temp_file = []
            set2 = set()
            stem_word_file = []
            word_list = word_tokenize(token)
            stem_temp = ""
            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)

            if search_type == "publication" and data_dict.get(stem_word_file[0].strip()):
                set1 = set(data_dict.get(stem_word_file[0].strip()))
                pointer.extend(list(set1))

            if match_word == []:
                match_word = list({z for z in pointer if z in set2 or (set2.add(z) or False)})
            else:
                match_word.extend(list(set1))
                match_word = list({z for z in match_word if z in set2 or (set2.add(z) or False)})

        if len(input_text) > 1:
            match_word = {z for z in match_word if z in set2 or (set2.add(z) or False)}

            if len(match_word) == 0:
                output_data = {}
            else:
                for j in list(match_word):
                    if search_type == "publication":
                        temp_file.append(pub_list_first_stem[j])
                    elif search_type == "author":
                        temp_file.append(author_list_first_stem[j])

                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in list(match_word):
                    output_data[j] = cosine_output[list(match_word).index(j)]
        else:
            if len(pointer) == 0:
                output_data = {}
            else:
                for j in pointer:
                    if search_type == "publication":
                        temp_file.append(pub_list_first_stem[j])
                    elif search_type == "author":
                        temp_file.append(author_list_first_stem[j])

                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in pointer:
                    output_data[j] = cosine_output[pointer.index(j)]

    return output_data


def app():

    # Load the image and display it
    image = Image.open('cire.png')
    st.image(image)

    # Add a text description
    st.markdown("<p style='text-align: center;'> Uncover the brilliance: Explore profiles, groundbreaking work, and cutting-edge research by the exceptional minds of Coventry University.</p>", unsafe_allow_html=True)

    input_text = st.text_input("Search research:", key="query_input")
    operator_val = st.radio(
        "Search Filters",
        ['Exact', 'Relevant'],
        index=1,
        key="operator_input",
        horizontal=True,
    )
    search_type = st.radio(
        "Search in:",
        ['Publications', 'Authors'],
        index=0,
        key="search_type_input",
        horizontal=True,
    )

    if st.button("SEARCH"):
        if search_type == "Publications":
            output_data = search_data(input_text, 1 if operator_val == 'Exact' else 2, "publication")
        elif search_type == "Authors":
            output_data = search_data(input_text, 1 if operator_val == 'Exact' else 2, "author")
        else:
            output_data = {}

        # Display the search results
        show_results(output_data, search_type)

    st.markdown("<p style='text-align: center;'> Brought to you with ❤ by <a href='https://github.com/maladeep'>Mala Deep</a> | Data © Coventry University </p>", unsafe_allow_html=True)


def show_results(output_data, search_type):
    if output_data:
        if search_type == "Publications":
            for k, v in output_data.items():
                st.subheader(pub_name[k])
                st.write("Authors:", author_name[pub_cu_author[k]])
                st.write("Published on:", pub_date[k])
                st.write("Similarity Score:", v)
                st.write("Read more:", pub_url[k])
                st.write("---")
        elif search_type == "Authors":
            for k, v in output_data.items():
                st.subheader(author_name[k])
                st.write("Similarity Score:", v)
                st.write("---")
    else:
        st.warning("No results found for the given query.")


if __name__ == '__main__':
    app()
