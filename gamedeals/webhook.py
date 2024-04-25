# -*- coding: utf-8 -*-
from requests import post, Response


class Embed:
    def __init__(
        self,
        title: str = None,
        description: str = None,
        url: str = None
    ) -> None:
        self.title = title
        self.description = description
        self.url = url

    def to_dict(self) -> dict:
        result = {}
        if self.title:
            result['title'] = self.title
        if self.description:
            result['description'] = self.description
        if self.url:
            result['url'] = self.url
        return result


class Webhook:
    def __init__(self, *, url: str, embeds: list[Embed]) -> None:
        self.url = url
        self.embeds = embeds

    def send(self) -> Response:
        return post(url=self.url, json=dict(embeds=[
            e.to_dict() for e in self.embeds
        ]))
