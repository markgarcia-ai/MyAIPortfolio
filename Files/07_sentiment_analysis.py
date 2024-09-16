import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Function to scrape website text
def fetch_website_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting visible text
        texts = soup.findAll(text=True)
        visible_texts = filter(visible, texts)
        return " ".join(t.strip() for t in visible_texts)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

# Helper function to filter visible elements
def visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True

# Function to analyze sentiment of text using VADER
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    return score

# Function to analyze the sentiment of a stock based on a list of websites and save to a file
def analyze_stock_sentiment(stock_symbol, file_path):
    aggregated_sentiment = {
        'neg': 0,
        'neu': 0,
        'pos': 0,
        'compound': 0
    }
    valid_urls = 0

    with open(file_path, 'a') as file:
        file.write(f"\nAnalyzing sentiment for {stock_symbol}:\n")

        urls = [
            f'https://finance.yahoo.com/quote/{stock_symbol}/?guccounter=1',
            f'https://www.marketwatch.com/investing/stock/{stock_symbol}'
        ]

        for url in urls:
            print(f"Fetching and analyzing {url}...")
            file.write(f"Fetching and analyzing {url}...\n")
            website_text = fetch_website_text(url)
            if website_text:
                sentiment = analyze_sentiment(website_text)
                file.write(f"Sentiment for {url}: {sentiment}\n")

                # Aggregate the sentiment scores
                aggregated_sentiment['neg'] += sentiment['neg']
                aggregated_sentiment['neu'] += sentiment['neu']
                aggregated_sentiment['pos'] += sentiment['pos']
                aggregated_sentiment['compound'] += sentiment['compound']
                valid_urls += 1

        # Normalize the aggregated sentiment scores by the number of valid URLs
        if valid_urls > 0:
            for key in aggregated_sentiment:
                aggregated_sentiment[key] /= valid_urls

            file.write(f"\nAggregated Sentiment for {stock_symbol}: {aggregated_sentiment}\n")
        else:
            file.write(f"No valid data found for {stock_symbol}\n")

# Main function to analyze multiple tickers and save results in a txt file
if __name__ == "__main__":
    # Get three tickers from user
    tickers = input("Enter three stock tickers separated by spaces: ").upper().split()

    # Check if exactly three tickers are provided
    if len(tickers) != 3:
        print("Please enter exactly three stock tickers.")
        exit()

    # Path to save the sentiment analysis results
    file_path = "sentiment_analysis_results.txt"

    # Clear the file before starting
    with open(file_path, 'w') as file:
        file.write("Stock Sentiment Analysis Results\n")

    # Perform sentiment analysis for each ticker
    for ticker in tickers:
        ticker = ticker.strip()
        print(f"Analyzing sentiment for {ticker}...")
        analyze_stock_sentiment(ticker, file_path)

    print(f"Sentiment analysis completed. Results saved in {file_path}.")
