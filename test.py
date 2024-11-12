from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://twitter.com/search?q=racist&src=typed_query")

time.sleep(60)  #Time to log in before start scrolling

tweets = []
tweet_id = 1

while len(tweets) < 5: #number of samples
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)  # Time between scroll
    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for tweet in soup.find_all("article"):
        try:
            user = None
            user_span = tweet.find("span", {"class": "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"})
            user_div = tweet.find("div", {"data-testid": "User-Names"})
            if user_span:
                user = user_span.get_text()
            elif user_div:
                user = user_div.get_text()
            
            if not user:
                user_container = tweet.find("div", {"dir": "ltr"})
                user = user_container.get_text() if user_container else "N/A"
            
            content_div = tweet.find("div", {"lang": True})
            content = content_div.get_text() if content_div else "N/A"

            if content and content not in [t['content'] for t in tweets]:
                tweets.append({"id": tweet_id, "user": user, "content": content})
                tweet_id += 1

            if len(tweets) >= 5:
                break

        except Exception as e:
            print(f"Error parsing tweet: {e}")

driver.quit()
df = pd.DataFrame(tweets)
df.to_csv("tweets.csv", index=False)
print("Data saved to tweets.csv")