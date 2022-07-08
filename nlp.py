from bs4 import BeautifulSoup
import requests
import nltk
from requests.api import get
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_headlines(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = soup.find_all("a", class_="tab-link-news")
        return headlines
    return False

def get_sentiment_score(ticker):
    score = 0
    num = 0
    vader = SentimentIntensityAnalyzer()
    headlines = get_headlines(ticker)
    if headlines:
        for i in headlines:
            score += vader.polarity_scores(i.text)["compound"]
            num += 1
        try:
            return score/num
        except:
            return 0
    return 0

def get_all_sentiment_score():
    tickers = { 
    "XLC":"Communication Services",
    "XLY":"Consumer Cyclical",
    "XLP":"Consumer Defensive",
    "XLE":"Energy",
    "XLF":"Financial Services",
    "XLV":"Healthcare",
    "XLI":"Industrials",
    "XLB":"Basic Materials",
    "XLRE":"Real Estate",
    "XLK":"Technology",
    "XLU":"Utilities",
    }
    outList = []
    for i,j in tickers.items():
        score = 0
        num = 0
        vader = SentimentIntensityAnalyzer()
        headlines = get_headlines(i)
        if headlines:
            for i in headlines:
                score += vader.polarity_scores(i.text)["compound"]
                num += 1
            try:
                outList.append([j, score/num])
            except:
                outList.append([j, 0])
    return outList