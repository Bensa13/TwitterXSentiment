import tweepy
import re
from .protocols import TwitterAccessTokenHandler
from tqdm import tqdm


class TweetExtractor:
    def __init__(
        self,
        auth: tweepy.auth.OAuthHandler,
        access_token_handler: TwitterAccessTokenHandler,
    ):
        self.auth = auth
        self.auth.set_access_token(
            access_token_handler.access_token, access_token_handler.access_token_secret
        )
        self.API = tweepy.API(self.auth, wait_on_rate_limit=True)

    def get_tweets(
        self, tweets_number: int, language: str, hashtag: str = ""
    ) -> list[dict[str, str]]:
        """gets all the tweets for a specific hashtag if no hashtag is provided, it will such provide
        as many tweets as specified without any specific looking pattern"""
        filter = " -filter:retweets"

        # Creating a cursor that can fetch multiple tweets
        tweepy_cursor = tweepy.Cursor(
            self.API.search_tweets, q=f"{hashtag}{filter}", lang=language
        ).items(tweets_number)

        # convert tweets into the right format
        tweets = [
            self._structure_tweet(tweet)
            for tweet in tqdm(
                tweepy_cursor,
                desc=f"Fetching tweets for SearchTerm: {hashtag} ...",
                total=tweets_number,
            )
        ]
        return tweets

    def _structure_tweet(self, tweet) -> dict[str, str]:
        # structures a tweet and extracts  specific pieces of information
        tweet_data = {}
        tweet_data["userName"] = tweet.user.name
        tweet_data["tweetText"] = tweet.text
        tweet_data["cleanedText"] = self._clean_text(tweet.text)
        tweet_data["createdAt"] = tweet.created_at.__str__()
        return tweet_data

    def _clean_text(self, txt: str) -> str:
        """Cleans the text of a tweet. Applies the following transformations
        1. everything lower case
        2. no special characters such, i.e., äüö
        3. no tags and content between tags
        4. no links
        5. remove all @
        """

        txt = txt.lower()

        # replacing special characters, if needed the char_mappings could be expanded
        char_mappings = {"ö": "oe", "ä": "ae", "ü": "ue"}
        for special_char, char in char_mappings.items():
            txt = txt.replace(special_char, char)

        # Pattern that gets rid of <>content<> and (content)
        pattern = r"(<.*?>.*?<.*?>)(<*.?>)|((\(.*?\)))|(\.)"
        pattern = re.compile(pattern)
        txt = re.sub(pattern, "", txt)

        # get rid of all links
        txt_clean_lst = list(
            filter(
                lambda x: not x.startswith("http") and not x.startswith("@"),
                txt.split(),
            )
        )
        # join txt_clean_lst back together
        txt_cleaned = " ".join(txt_clean_lst)

        # only allow [a-z]
        pattern = r"[a-z]+"
        pattern = re.compile(pattern)
        txt_cleaned = " ".join(re.findall(pattern, txt_cleaned))

        return txt_cleaned
