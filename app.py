import streamlit as st 
import pickle 
import string 
import nltk 
from nltk.stem.porter import PorterStemmer 
from nltk.corpus import stopwords 

cv = pickle.load(open("vectorizor.pkl" , "rb"))
model = pickle.load(open("model.pkl" , "rb"))


st.title("Email/SMS Classifier")
input_sms = st.text_input("Enter your message here to check")




def transform_text(text):                               # I dont think this punctuation is required..
    text = text.lower()                                 # Lower
    text = nltk.word_tokenize(text)                     # Tokenizer 
    y = []
    ps = PorterStemmer()
    stop_word_list = stopwords.words('english')         # Stopwords list 
    for i in text:
        if i.isalnum():                                 #Check for stopwords and punctuations with Stemmer...
            if i not in stop_word_list and i not in string.punctuation: 
                i = ps.stem(i)
                y.append(i)

    return " " . join(y)



if st.button('Predict'):
    #1 :- Preprocess
    transform_message = transform_text(input_sms)

    #2 :- Vectorize
    vector = cv.transform([transform_message])

    #3 :- Predict
    result = model.predict(vector)[0]

    #4 :- Display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")