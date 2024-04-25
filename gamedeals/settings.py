# -*- coding: utf-8 -*-
from os import getenv


class RedditSettings:
    def __init__(self) -> None:
        self.client_id = getenv('REDDIT_CLIENT_ID')
        self.client_secret = getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = getenv('REDDIT_USER_AGENT')
        self.username = getenv('REDDIT_USERNAME')
        self.password = getenv('REDDIT_PASSWORD')
        self.use_read_only = bool(getenv('REDDIT_READ_ONLY'))


class GuildedSettings:
    def __init__(self) -> None:
        self.webhook_url = getenv('GUILDED_WEBHOOK_URL')


class Settings:
    def __init__(self) -> None:
        self.reddit = RedditSettings()
        self.guilded = GuildedSettings()
