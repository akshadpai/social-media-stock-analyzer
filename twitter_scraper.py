from enum import Enum
import requests
import json
import os
import time

class SearchType(Enum):
    TOP = "Top"
    LATEST = "Latest"

class TwitterScraper():
    def __init__(self, cookie, csrf_token):
        self.cookie = cookie
        self.csrf_token = csrf_token

    def request_get(self, url, params):
        headers = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "content-type": "application/json",
                "cookie": self.cookie,
                "priority": "u=1, i",
                "referer": f"https://x.com/search?q=&src=typed_query",
                "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "x-csrf-token": self.csrf_token,
                "x-twitter-active-user": "yes",
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-client-language": "en",
            }
        return requests.get(url, headers=headers, params=params)

    def search(self, term, limit=20, search_type=SearchType.LATEST):
        tweets = []

        url = 'https://x.com/i/api/graphql/MJpyQGqgklrVl_0X9gNy3A/SearchTimeline'
        cursor = ''

        for i in range(limit // 20):
            params = {
                "variables": json.dumps({"rawQuery":term,"count":20,"querySource":"typed_query","product":search_type.value, "cursor": cursor}),
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}'
            }
            time.sleep(5)
            print(f'Searching for tweets with term "{term}" {i+1}/{limit // 20}...')
            response = self.request_get(url, params)
            if(response.status_code == 200):
                result = json.loads(response.content.decode("utf-8"))
                instructions = result['data']['search_by_raw_query']['search_timeline']['timeline']['instructions']
                for instruction in instructions:
                    if 'entry' in instruction and 'cursor-bottom' in instruction['entry']['entryId']:
                        cursor = instruction['entry']['content']['value']
                        
                if('entries' in instructions[0]):
                    items = instructions[0]['entries']
                    for item in items:
                        if('cursor' in item['entryId']):
                            if(item['entryId'] == "cursor-bottom-0"):
                                cursor = item['content']['value']
                        elif('tweet-' in item['entryId']):
                            if 'legacy' in item['content']['itemContent']['tweet_results']['result']:
                                text = item['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].strip().replace("\n", "")
                                tweet_id = item['entryId'].replace("tweet-", "")
                                favorite_count = item['content']['itemContent']['tweet_results']['result']['legacy']['favorite_count']
                                quote_count = item['content']['itemContent']['tweet_results']['result']['legacy']['quote_count']
                                reply_count = item['content']['itemContent']['tweet_results']['result']['legacy']['reply_count']
                                retweet_count = item['content']['itemContent']['tweet_results']['result']['legacy']['retweet_count']
                                print(f"Getting comments for tweet id {tweet_id}...")
                                comments = self.get_comments(tweet_id)
                                tweet = {
                                    "text": text,
                                    "tweet_id": tweet_id,
                                    "favorite_count": favorite_count,
                                    "quote_count": quote_count,
                                    "reply_count": reply_count,
                                    "retweet_count": retweet_count,
                                    "comments": comments,
                                }
                                tweets.append(tweet)
                else:
                    break

            elif(response.status_code == 429):
                raise Exception("Too many requests. Rate limit on search!")

        return tweets

    def get_comments(self, tweet_id):
        comments = []

        url = 'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail'
        params = {
            'variables': json.dumps({"focalTweetId":tweet_id,"referrer":"search","controller_data":"DAACDAAFDAABDAABDAABCgABAAAAAAACgAAAAAwAAgoAAQAAAAAAAAABCgACCH512fsqDAULAAMAAAAMZ29vZ2xlIHN0b2NrCgAFNaM6pefw3IUIAAYAAAABCgAHA6pwEfLwj2YAAAAAAA==","with_rux_injections":False,"rankingMode":"Relevance","includePromotedContent":True,"withCommunity":True,"withQuickPromoteEligibilityTweetFields":True,"withBirdwatchNotes":True,"withVoice":True}),
            'features': '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
            'fieldToggles': '{"withArticleRichContentState":true,"withArticlePlainText":false,"withGrokAnalyze":false,"withDisallowedReplyControls":false}',
        }

        time.sleep(5)
        response = self.request_get(url, params)
        if(response.status_code == 200):
            result = json.loads(response.content.decode("utf-8"))
            items = result['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']
            for item in items:
                if 'conversationthread' in item['entryId']:
                    reply_items = item['content']['items']
                    for reply_item in reply_items:
                        if('tweet_results' in reply_item['item']['itemContent']):
                            text = reply_item['item']['itemContent']['tweet_results']['result']['legacy']['full_text'].strip().replace("\n", "")
                            comments.append(text)
        
        elif(response.status_code == 429):
                raise Exception("Too many requests. Rate limit on get comments!")

        return comments
        

def merge_and_replace(existing_list, new_list):
    existing_dict = {item['tweet_id']: item for item in existing_list}
    for new_item in new_list:
        existing_dict[new_item['tweet_id']] = new_item
    return list(existing_dict.values())

def store_to_file(data, file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump([], file)

    with open(file_path, "r") as file:
        data = json.load(file)

    with open(file_path, "w") as file:
        data = merge_and_replace(data, result_tweets)
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    file_path = 'data.json'

    ########## Log in to your Twitter/X account and then get cookie and csrf_token from Network tab in Chrome developer tools. ##########
    ########## Make sure to also aware of rate limit. When it happens, we need to switch to new account. ##########
    scraper = TwitterScraper(
        cookie='COOKIE HERE',
        csrf_token='CSRF TOKEN HERE',
    )

    terms_to_search = [
        "stock market analysis",
        "stock today",
        "big tech stock",
        "meta stock",
        "google stock",
    ]

    for term in terms_to_search:
        result_tweets = scraper.search(term=term, limit=40, search_type=SearchType.LATEST)
        store_to_file(result_tweets, file_path)

    

