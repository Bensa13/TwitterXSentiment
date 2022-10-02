from transformers import pipeline


class SentimentAnalysis:
    """Sentiment Analysis class
    Takes in a task and a model_url and
    can then score a text or a list of text's sentiment
    """

    def __init__(self, task: str, model_url: str = ""):
        self.task = task
        self.model_url = model_url
        if model_url:
            self.model_pipeline = pipeline(self.task, model=self.model_url)
        else:
            self.model_pipeline = pipeline(self.task)

    def get_sentiment(
        self, txt: str | list[str]
    ) -> dict[str, str] | list[dict[str, str]]:
        """Applies the sentiment analysis on a string or a list of strings"""
        return self.model_pipeline(txt)
