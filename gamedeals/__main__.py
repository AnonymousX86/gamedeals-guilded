# -*- coding: utf-8 -*-
from logging import basicConfig, getLogger, INFO, StreamHandler
from time import sleep

from praw import Reddit
from praw.models import Subreddit
from rich.logging import RichHandler

from .settings import Settings
from .webhook import Embed, Webhook


def main() -> None:
    basicConfig(
        level=INFO,
        format='%(message)s',
        handlers=[
            RichHandler(
                omit_repeated_times=False,
                markup=True,
                rich_tracebacks=True
            )
        ]
    )
    log = getLogger('rich')
    settings = Settings()
    read_only = False

    # Check required settings
    if not (reddit_settings := settings.reddit).client_id:
        log.critical('Reddit client ID is missing!')
        return
    if not reddit_settings.client_secret:
        log.critical('Reddit client secret is missing!')
        return
    if not reddit_settings.user_agent:
        log.critical('Reddit user agent is missing!')
        return
    if not settings.guilded.webhook_url:
        log.critical('Guilded webhook url is missing!')
        return

    # Check optional settings
    if not reddit_settings.username:
        log.warn('Reddit username is missing.')
        read_only = True
    if not reddit_settings.password:
        log.warn('Reddit password is missing.')
        read_only = True

    if not (read_only or settings.reddit.use_read_only):
        reddit = Reddit(
            client_id=settings.reddit.client_id,
            client_secret=settings.reddit.client_secret,
            user_agent=settings.reddit.user_agent,
            username=settings.reddit.username,
            password=settings.reddit.password
        )
    else:
        log.warn('Using in read only mode.')
        reddit = Reddit(
            client_id=settings.reddit.client_id,
            client_secret=settings.reddit.client_secret,
            user_agent=settings.reddit.user_agent
        )

    sub_name = 'GameDeals'
    subreddit: Subreddit = reddit.subreddit(sub_name)
    if not subreddit.display_name:
        log.critical(f'Subreddit r/{sub_name} not found!')
        return
    log.info(f'Connected to r/{sub_name}')

    while True:
        subs = []
        for sub in subreddit.new(limit=5):
            # TODO - check if game deal was already sent
            # TODO - setting for specific platform check
            # if 'steam' in (title := sub.title.lower()):
            if any(x in sub.title.lower() for x in ['free', '100%']):
                subs.append(sub)

        if not subs:
            log.info('No new game deals 😭')

        else:
            embeds = []
            for sub in subs:
                embeds.append(Embed(
                    title='New game deal',
                    description=sub.title,
                    url=f'https://reddit.com{sub.permalink}'
                ))
                log.info(f'New free game: "{sub.title}" - "{sub.permalink}"')

            webhook = Webhook(
                url=settings.guilded.webhook_url,
                embeds=embeds
            )

            response = webhook.send()
            if (code := response.status_code) != 200:
                log.critical(f'Webhook not sent because of: "{response.text}"')
            else:
                log.info('Webhook sent!')

        # Sleep for 1 hour
        log.info('Waiting one hour')
        sleep(3600)


if __name__ == '__main__':
    main()
