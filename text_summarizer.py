from transformers import pipeline
import re
import string

summarizer = pipeline("summarization")

def  clean_text(text):
    # text =  text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"I'm", "I am", text)
    text = re.sub(r"\r", "", text)

    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"He's", "He is", text)

    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"She's", "She is", text)

    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "that is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"n'", "ng", text)
    text = re.sub(r"'bout", "about", text)
    text = re.sub(r"'til", "until", text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation)) 
    text = re.sub("(\\W)"," ",text) 
    text = re.sub('\S*\d\S*\s*','', text)
    
    return text

def summarise(text):
    summarized = summarizer(clean_text(text), min_length=300, max_length=500)
    return summarized