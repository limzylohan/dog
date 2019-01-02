from bs4 import BeautifulSoup
import requests
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from nltk.tokenize import word_tokenize




url = 'https://www.straitstimes.com/'
page = requests.get(url, timeout=1)
# here, we fetch the content from the url, using the requests library

soup = BeautifulSoup(page.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

news_stories_links = []
news_stories_summaries = []
# news_stories = {}

def straits(): 
    #extracting out relevant stories
    for link in soup.find_all('span', class_= 'story-headline'):
        news_stories_links.append(link.a.get('href'))
        news_stories_summaries.append(link.a.text)
        if len(news_stories_links) == 5:
            break
    news_stories =[news_stories_summaries,news_stories_links]
    return news_stories


def remove_tag(text, tag):
    return text.replace("</{}>".format(tag), '').replace("<{}>".format(tag), '').replace("<{}".format(tag), '')

def return_url(lister, num):
        #header to mimic web browser surfing
        headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        url =  'https://www.straitstimes.com/' + lister[1][num]
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        paragraphs = str(soup.findAll('p'))

        #remove tags
        tag_list = ['a', 'p', 'div', 'li', 'span', 'img', 'ul', 'ol', 'label', 'h', 'h1', 'h2', 'h3', 'h4', 'h5']
        for tag in tag_list:
                paragraphs = remove_tag(paragraphs, tag)
        #remove tags
        others = ['href=', '<', '>', '[]', '[', ']', '\n', '   ', '{', '}', '#']
        #hardcoding removal of some text
        for s in others:
                paragraphs = paragraphs.replace(s, '')

        paragraphs = paragraphs.replace(',  class="copy"SPH Digital News / Copyright © 2019 Singapore Press Holdings Ltd. Co. Regn.' ,'')
        paragraphs = paragraphs.replace('Until we resolve the issues, subscribers need not log in to access ST Digital articles.','')

        #calling API to summarize text
        text_list = ""
        plaintext = PlaintextParser.from_string(paragraphs,Tokenizer("english"))
        stemmer = Stemmer("english")
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")
        for sentence in summarizer(plaintext.document, 4): 
                text_list += str(sentence) + " "
        return text_list

#test code
# test = straits()
# return_url(test, 2)