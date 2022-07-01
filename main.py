
import requests
from flask import Flask, render_template, url_for, redirect, jsonify, Response, abort, session, request, send_file
import json
from bs4 import BeautifulSoup

import content_scraper as cs

import re
import string
from tqdm import tqdm


results = dict()
prices = dict()


url: str = "https://cryptonews.com/news/"
cryptonews_url = "https://cointelegraph.com/"
coindesk_url = "https://www.coindesk.com/"


app = Flask(__name__)

ml_summary = False # Make it True, Will require GPU Enabled System

if ml_summary:
    from transformers import pipeline
    summarizer = pipeline("summarization") 

summary_text_limit = 200

def  clean_text_func(text):
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


# Function to remove tags
def remove_html_tags(html):
  
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


def summarize(text):
    summarized = summarizer(clean_text_func(text)[:10000], min_length=100, max_length=summary_text_limit)
    return summarized[0]['summary_text']






@app.route('/', methods=['get', 'post'])
def main_page():
    global results
    return render_template('main.html', user=("Username", "Name"), results=results)


@app.route('/table/', methods=['get', 'post'])
def price_table():
    data = requests.get("https://api.binance.com/api/v3/ticker/price")
    data = data.json()
    return render_template('table.html', user=("Username", "Name"), results=data)
    

@app.errorhandler(404)
def nice(_):
    return render_template('error_404.html')

app.secret_key = 'q12q3q4e5g5htrh@werwer15454'

if __name__ == '__main__':
    print("\n"*5)
    print("Started")
    

    print("\n\nScraping for Cryptonews")
    # https://cryptonews.com/news/
    soup = cs.make_soup(url)
    op1 = cs.cryptonews_scraper(soup)[:5]
    for i in tqdm(range(len(op1))):
        op1[i]['url'] = "https://cryptonews.com"+op1[i]['url']
        print(op1[i]['url'])
        r = requests.get(op1[i]['url'], headers={'User-Agent': 'Mozilla/5.0'})
        clean_text = remove_html_tags(r.text).splitlines()
        max_length = 0
        max_index = 0
        for j in range(len(clean_text)):
            length = len(clean_text[j])
            if length > max_length:
                max_index = j
                max_length = length

        if ml_summary:
            selected_text = clean_text[max_index][:3000].strip()
            op1[i]['summary'] = summarize(selected_text)
        else:
            selected_text = clean_text[max_index][:summary_text_limit].strip()
            op1[i]['summary'] = selected_text

    results['Crypto News'] = op1


    print("\n\nScraping for Cointelegraph")
    # https://cointelegraph.com/
    soup = cs.make_soup(cryptonews_url)
    op2 = cs.cointelegraph_scraper(soup)[:5]

    for i in tqdm(range(len(op2))):
        op2[i]['url'] = "https://cointelegraph.com/"+op2[i]['url']
        print(op2[i]['url'])
        r = requests.get(op2[i]['url'], headers={'User-Agent': 'Mozilla/5.0'})
        clean_text = remove_html_tags(r.text).splitlines()
        max_length = 0
        max_index = 0
        for j in range(len(clean_text)):
            length = len(clean_text[j])
            if length > max_length:
                max_index = j
                max_length = length

        if ml_summary:
            selected_text = clean_text[max_index][:3000].strip()
            op2[i]['summary'] = summarize(selected_text)
        else:
            selected_text = clean_text[max_index][:summary_text_limit].strip()
            op2[i]['summary'] = selected_text

    results['Coin Telegraph'] = op2


    print("\n\nScraping for coindesk")
    # https://www.coindesk.com/ 
    soup = cs.make_soup(coindesk_url)
    op3 = cs.coindesk_scraper(soup)[:5]

    for i in tqdm(range(len(op3))):
        op3[i]['url'] = "https://www.coindesk.com/"+op3[i]['url']
        print(op3[i]['url'])
        r = requests.get(op3[i]['url'], headers={'User-Agent': 'Mozilla/5.0'})
        clean_text = remove_html_tags(r.text).splitlines()
        max_length = 0
        max_index = 0
        for j in range(len(clean_text)):
            length = len(clean_text[j])
            if length > max_length:
                max_index = j
                max_length = length

        if ml_summary:
            selected_text = clean_text[max_index][:3000].strip()
            op3[i]['summary'] = summarize(selected_text)
        else:
            selected_text = clean_text[max_index][:summary_text_limit].strip()
            op3[i]['summary'] = selected_text

    results['Coin Desk'] = op3

    app.run(host='0.0.0.0', port= 5000)#80)

