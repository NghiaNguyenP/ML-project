from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://x.com/search?q=hate&src=typed_query&f=top")

time.sleep(120)  #log in time

tweets = []
tweet_id = 1 

while len(tweets) < 20: #number of data u want
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)  #wait between scroll time
    
    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for tweet in soup.find_all("article"):
        content = tweet.get_text()
        user = tweet.find("span", {"class": "username"}).get_text() if tweet.find("span", {"class": "username"}) else "N/A"
        
        # Avoid duplicates
        if content not in [t['content'] for t in tweets]:
            tweets.append({"id": tweet_id, "user": user, "content": content})
            tweet_id += 1

        if len(tweets) >= 20:
            break

driver.quit()

df = pd.DataFrame(tweets)
df.to_csv("tweets.csv", index=False)
print("Data saved to tweets.csv")
