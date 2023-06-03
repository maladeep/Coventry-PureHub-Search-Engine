import streamlit as st
from PIL import Image
import ujson
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Import Stopwords and punkt
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
with open('publication_indexed_dictionary.json', 'r') as f:
    pub_index = ujson.load(f)
with open('author_list_stemmed.json', 'r') as f:
    author_list_first_stem = ujson.load(f)
with open('author_indexed_dictionary.json', 'r') as f:
    author_index = ujson.load(f)
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


# Streamlit Decorator to cache the function's output, this will improve performance when the function is called multiple times
@st.cache
def build_inverted_index(documents):
    inverted_index = {}

    for doc_id, doc in enumerate(documents):
        words = word_tokenize(doc)

        for word in words:
            if word.lower() not in stop_words:
                stemmed_word = stemmer.stem(word)
                if stemmed_word in inverted_index:
                    inverted_index[stemmed_word].append(doc_id)
                else:
                    inverted_index[stemmed_word] = [doc_id]

    return inverted_index


# Searching data based on user input
def search_data(input_text, operator_val, search_type, inverted_index):
    output_data = {}

    if operator_val == 1:  # Exact operator (AND)
        input_text = input_text.lower().split()
        pointer = set()

        for token in input_text:
            if len(token) <= 3:
                st.warning("Please enter more than 3 characters.")
                break

            stemmed_word = stemmer.stem(token)
            if stemmed_word in inverted_index:
                pointer.update(inverted_index[stemmed_word])

        if len(pointer) == 0:
            output_data = {}
        else:
            temp_file = [pub_list_first_stem[i] for i in pointer]
            temp_file = tfidf.fit_transform(temp_file)
            cosine_output = cosine_similarity(temp_file, tfidf.transform(input_text))

            for i, j in zip(pointer, cosine_output):
                output_data[i] = j

    else:  # Relevant operator (OR)
        input_text = input_text.lower().split()
        pointer = []
        match_word = []

        for token in input_text:
            if len(token) <= 3:
                st.warning("Please enter more than 3 characters.")
                break

            stem_word_file = []
            stem_temp = ""
            word_list = word_tokenize(token)

            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)

            if search_type == "publication" and pub_index.get(stem_word_file[0].strip()):
                set1 = set(pub_index.get(stem_word_file[0].strip()))
                pointer = pointer + list(set1)

        for i in pointer:
            if search_type == "publication":
                match_word.append(pub_list_first_stem[i])
            else:
                match_word.append(author_list_first_stem[i])

        output_data = match_word

    return output_data


def show_results(output_data, search_type):
    
   aa = 0
    print(f"Output Data: {output_data}")
    print(f"Output Data Type: {type(output_data)}")
    rank_sorting = None

    if output_data:
        print("Output Data is not empty")
        rank_sorting = sorted(output_data.items(), key=lambda z: z[1], reverse=True)
        print(f"Rank Sorting: {rank_sorting}")

    
    # Show the total number of research results
    st.info(f"Showing results for: {len(rank_sorting)}")

    # Show the cards
    N_cards_per_row = 3
    for n_row, (id_val, ranking) in enumerate(rank_sorting):
        i = n_row % N_cards_per_row
        if i == 0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # Draw the card
        with cols[n_row % N_cards_per_row]:
            if search_type == "Publications":
                st.caption(f"{pub_date[id_val].strip()}")
                st.markdown(f"**{pub_cu_author[id_val].strip()}**")
                st.markdown(f"*{pub_name[id_val].strip()}*")
                st.markdown(f"**{pub_url[id_val]}**")
            elif search_type == "Authors":
                st.caption(f"{pub_date[id_val].strip()}")
                st.markdown(f"**{author_name[id_val].strip()}**")
                st.markdown(f"*{pub_name[id_val].strip()}*")
                st.markdown(f"**{pub_url[id_val]}**")
                st.markdown(f"Ranking: {ranking[0]:.2f}")

        aa += 1

    if aa == 0:
        st.info("No results found. Please try again.")
    else:
        st.info(f"Results shown for: {aa}")


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
            output_data = search_data(input_text, 1 if operator_val == 'Exact' else 2, "publication", inverted_index)
        elif search_type == "Authors":
            output_data = search_data(input_text, 1 if operator_val == 'Exact' else 2, "author", inverted_index)
        else:
            output_data = {}

        # Display the search results
        show_results(output_data, search_type)

    st.markdown("<p style='text-align: center;'> Brought To you with ❤ By <a href='https://github.com/maladeep'>Mala Deep</a> | Data © Coventry University </p>", unsafe_allow_html=True)


# Build the inverted index
inverted_index = build_inverted_index(pub_list_first_stem)

if __name__ == '__main__':
    app()
