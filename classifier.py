
import numpy as np  # Enables working with arrays and mathematical operations
import pandas as pd  # Provides data structures and data analysis tools
import seaborn as sns; sns.set()  # Enhances the visual appearance of plots and figures
from nltk.corpus import stopwords  # Provides stopwords for natural language processing tasks
from nltk.stem import PorterStemmer  # Implements the Porter stemming algorithm for word normalization
from nltk.tokenize import word_tokenize  # Splits text into words or tokens
from sklearn.feature_extraction.text import TfidfVectorizer  # Transforms text data into numerical features
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, classification_report  # Evaluates model performance metrics
from sklearn.naive_bayes import MultinomialNB  # Implements the Multinomial Naive Bayes classifier
from skmultilearn.problem_transform import ClassifierChain  # Implements problem transformation techniques for multi-label classification
import matplotlib.pyplot as plt  # Creates visualizations and plots
import pickle  # Enables object serialization and deserialization
from sklearn.pipeline import Pipeline  # Chains multiple steps into a single unit for machine learning workflows



train_data = pd.read_csv('Train.csv')
test_data = pd.read_csv('Test.csv')

abstract_list_train = []
abstract_list_test = []
stemmer = PorterStemmer()
stop_words = stopwords.words('english')

#Remove StopWords and Stemming
def remove_stopwords(data = []):
    data_list = []
    for name in data:
        words = word_tokenize(name)
        stem_word = ""
        for a in words:
            if a.lower() not in stop_words:
                stem_word += stemmer.stem(a) + ' '
        data_list.append(stem_word.lower())
    return data_list

#Remove Special Characters
def remove_special_character(data = []):
    abstract_list_wo_sc = []
    special_characters = '''!()-—[]{};:'"\, <>./?@#$%^&*_~0123456789+=’‘'''
    for file in data:
        word_wo_sc = ""
        if len(file.split()) == 1:
            abstract_list_wo_sc.append(file)
        else:
            for a in file:
                if a in special_characters:
                    word_wo_sc += ' '
                else:
                    word_wo_sc += a
            abstract_list_wo_sc.append(word_wo_sc)
    return abstract_list_wo_sc

#Remove stopwords from Train Data
data_train = np.array(train_data['ABSTRACT'])
abstract_list_train = remove_stopwords(data_train)

#Remove stopwords from Test Data
data_test = np.array(test_data['ABSTRACT'])
abstract_list_test = remove_stopwords(data_test)

#Removing speaial characters from Train Data and Test Data
abstract_list_wo_sc_train = remove_special_character(abstract_list_train)
abstract_list_wo_sc_test = remove_special_character(abstract_list_test)

categories=['Engineering', 'Business', 'Art']

x_train = abstract_list_wo_sc_train
y_train = train_data[categories]
x_test = abstract_list_wo_sc_test
y_test = test_data[categories]

print("There are ", len(x_train), " input training samples")
print("There are ", len(x_test), " input testing samples")
print("There are ", y_train.shape, " output training samples")
print("There are ", y_test.shape, " output testing samples")





# defining parameters for pipeline
parameters = Pipeline([('tfidf', TfidfVectorizer(stop_words=stop_words)),('clf', ClassifierChain(MultinomialNB())),])

# train data
parameters.fit(x_train, y_train)


# predict
predictions = parameters.predict(x_test)



# Print accuracy score
accuracy = accuracy_score(y_test, predictions)
print('Accuracy:', accuracy)

# Print F1 score
f1 = f1_score(y_test, predictions, average='micro')
print('F1 score:', f1)

# Print classification report
report = classification_report(y_test, predictions)
print('Classification Report:')
print(report)




# Confusion Matrix and HeatMap Generation
mat = confusion_matrix(y_test.values.argmax(axis=1), predictions.argmax(axis=1))

plt.figure(figsize=(8, 6))
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False, cmap='Blues')
plt.xlabel('True Label')
plt.ylabel('Predicted Label')
plt.title('Confusion Matrix')

plt.show()


# Save as picklefile
with open('model_MultiNB.pkl', 'wb') as picklefile:
    pickle.dump(parameters.named_steps['clf'], picklefile)
