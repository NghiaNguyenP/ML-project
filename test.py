import asyncio
import json
from twikit import Client

USERNAME = 'proj39460'
EMAIL = 'groupprojectml6@gmail.com'
PASSWORD = 'thisisanXtestaccountforMLproject'

# Initialize the client
client = Client('en-US')

async def main():
    # Log in to Twitter
    # await client.login(
    #     auth_info_1=USERNAME,
    #     auth_info_2=EMAIL,
    #     password=PASSWORD
    # )
    # client.save_cookies('cookies.json')
    client.load_cookies('cookies.json')
    
    # Search for tweets related to a keyword, for example, 'racist'
    tweets = await client.search_tweet('racist', 'Latest')

    # Limit the result to 10 tweets
    sample_tweets = tweets[:10]

    # Create a list to store tweet data
    tweet_data = []

    # Collect tweet data with an incremental 'id'
    for idx, tweet in enumerate(sample_tweets, start=1):
        tweet_data.append({
            'id': idx,
            'user': tweet.user.name,
            'text': tweet.text,
            'created_at': tweet.created_at
        })

    # Save the tweet data to a JSON file
    with open('tweets_data.json', mode='w', encoding='utf-8') as file:
        json.dump(tweet_data, file, ensure_ascii=False, indent=4)

# Run the asyncio event loop
asyncio.run(main())