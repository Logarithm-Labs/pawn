
import requests

from datetime import datetime
from typing import Dict, List, Optional


class LlamaFeed:
    """Llamafeed REST API Wrapper to load latest crypto events
    such as news, tweets, hacks, polymarket, unlocks, raises, transfers, governance
    """

    def __init__(self):
        self._url: str = "https://feed-api.llama.fi"

    def _make_request(self, endpoint: str) -> List[Dict]:
        response = requests.get(self._url + endpoint)
        if response.status_code != 200:
            raise Exception(
                f"Failed to make request to {self._url + endpoint}: {response.status_code}({response.text})"
            )
        return response.json()

    def get_news(self, since_timestamp: Optional[float] = None) -> List[Dict]:
        """Args:
        ----
            since_timestamp (Optional[float]): Фильтровать новости, опубликованные после указанного timestamp

        Returns
        -------
            List[Dict]: Новости с ключевыми полями для анализа:
        [
            {
                'title': 'Jailed Binance exec's Nigeria trial postponed...',
                'content': 'Tigran Gambaryan is so sick that Nigerian prison...',
                'pub_date': '2024-10-18T13:32:57.000Z',
                'topic': 'Legal Issues in Financial Sectors',
                'sentiment': 'negative',
                'entities': ['Tigran Gambaryan', 'Binance', 'Nigeria']
            },
            ...
        ]

        """
        raw_news = self._make_request("/news")
        processed = [
            {
                "title": item["title"],
                "content": item["content"],
                "pub_date": item["pub_date"],
                "topic": item["topic"],
                "sentiment": item["sentiment"],
                "link": item["link"],
            }
            for item in raw_news
        ]

        if since_timestamp is not None:
            processed = [
                item
                for item in processed
                if datetime.fromisoformat(item["pub_date"].replace("Z", "+00:00")).timestamp() > since_timestamp
            ]
        return processed

    def get_tweets(self, since_timestamp: Optional[float] = None) -> List[Dict]:
        """Args:
        ----
            since_timestamp (Optional[float]): Фильтровать твиты созданные после указанного timestamp

        Returns
        -------
            List[Dict]: Tweets from DefillamaFeed
        [
            {
                'tweet': 'Azra Games raises $42.7 million in Series A...',
                'tweet_created_at': '2024-10-15T15:26:19.341Z',
                'user_name': 'The Block',
                'sentiment': 'positive',
                'link': 'https://x.com/theblockco/status/1846895776116379747'
            }
            ...
        ]

        """
        raw_tweets = self._make_request("/tweets")
        processed = [
            {
                "tweet": item["tweet"],
                "tweet_created_at": item["tweet_created_at"],
                "user_name": item["user_name"],
                "sentiment": item["sentiment"],
                # "link": item["link"],
            }
            for item in raw_tweets
        ]
        if since_timestamp is not None:
            processed = [
                tweet
                for tweet in processed
                if datetime.fromisoformat(tweet["tweet_created_at"].replace("Z", "+00:00")).timestamp()
                > since_timestamp
            ]
        return processed

    def get_hacks(self, since_timestamp: Optional[float] = None) -> List[Dict]:
        """Args:
        ----
            since_timestamp (Optional[float]): Фильтровать хаки с timestamp больше указанного

        Returns
        -------
            Dict: Hacks from DefillamaFeed

        [
            {
                'name': 'Ambient',
                'timestamp': 1729123200,
                'amount': None,
                'source_url': 'https://x.com/ambient_finance/status/1846895776116379747',
                'technique': 'Frontend Attack'
            },
            ...
        ]

        """
        hacks = self._make_request("/hacks")
        if since_timestamp is not None:
            hacks = [hack for hack in hacks if hack["timestamp"] > since_timestamp]
        return hacks

    def get_polymarket(self, since_timestamp: Optional[float] = None) -> List[Dict]:
        polymarkets = self._make_request("/polymarket")
        if since_timestamp is not None:
            polymarkets = [
                pm
                for pm in polymarkets
                if datetime.fromisoformat(pm["created_at"].replace("Z", "+00:00")).timestamp() > since_timestamp
            ]
        return polymarkets

    def get_unlocks(self, since_timestamp: Optional[float] = None) -> List[Dict]:
        unlocks = self._make_request("/unlocks")
        if since_timestamp is not None:
            unlocks = [unlock for unlock in unlocks if unlock["next_event"] > since_timestamp]
        return unlocks

    def get_raises(self, since_timestamp: Optional[float] = None) -> List[Dict]:
        raises = self._make_request("/raises")
        if since_timestamp is not None:
            raises = [r for r in raises if r["timestamp"] > since_timestamp]
        return raises

    def get_transfers(self, since_timestamp: Optional[float] = None) -> List[Dict]:
        transfers = self._make_request("/transfers")
        if since_timestamp is not None:
            transfers = [
                t
                for t in transfers
                if datetime.fromisoformat(t["block_time"].replace("Z", "+00:00")).timestamp() > since_timestamp
            ]
        return transfers

    def get_governance(self, since_timestamp: Optional[float] = None) -> List[Dict]:
        governance = self._make_request("/governance")
        if since_timestamp is not None:
            governance = [gov for gov in governance if gov["start"] > since_timestamp]
        return governance
