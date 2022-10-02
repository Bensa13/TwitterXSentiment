import pathlib
import pandas as pd
import sentiment.sentiment_classifier as sent
import tweets.utils as tu
import tweets.tweet_extractor as te
import tweepy





def main():
    
    # Model config 
    model_path = (pathlib.Path().cwd() / "configs" / "model.yaml").resolve()
    model_config = tu.load_yaml(model_path)

    # Twitter Credentials and search query config
    twitter_credentails_path = (pathlib.Path().cwd() / "configs" / "twitter_credentials.yaml").resolve()
    twitter_query_path = (pathlib.Path().cwd() / "configs" / "twitter_options.yaml").resolve()

    twitter_credentials = tu.load_yaml(twitter_credentails_path)
    twitter_query_config = tu.load_yaml(twitter_query_path)

    token_handler = tu.TokenHandler(
        twitter_credentials["ACCESS_TOKEN"], twitter_credentials["ACCESS_TOKEN_SECRET"]
    )
    auth = tweepy.OAuthHandler(
        twitter_credentials["CONSUMER_KEY"], twitter_credentials["CONSUMER_SECRET"]
    )

    tweets_extractor = te.TweetExtractor(auth, token_handler)

    number_of_tweets = twitter_query_config['NUMBER_OF_TWEETS']
    language = twitter_query_config['LANGUAGE']
    hashtag = twitter_query_config['HASHTAG']
    tweets = tweets_extractor.get_tweets(number_of_tweets, language, hashtag)

    # transform tweets into a pandas dataframe
    df_tweets = pd.DataFrame(tweets)

    # extract the cleanedText
    txt_lst = list(df_tweets["cleanedText"].values)

    # init sentiment analysis
    task = "sentiment-analysis"
    model_url = model_config["MODEL_URL"]
    sentiment = sent.SentimentAnalysis(task, model_url)
    sentiments = sentiment.get_sentiment(txt_lst)

    # turn the lst of dct into a dataframe
    df_sents = pd.DataFrame(sentiments)

    # put everything together
    df = pd.concat([df_tweets, df_sents], axis=1)
    return df


if __name__ == "__main__":
    tweets = main()
