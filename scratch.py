import requests
from bs4 import BeautifulSoup

YOUTUBE_TRENDING_URL ='https://www.youtube.com/feed/trending'

response = requests.get(YOUTUBE_TRENDING_URL)

print("Status code : ",response.status_code )

with open('trending.html', 'w') as f:
  f.write(response.text)

doc = BeautifulSoup(response.text, 'html.parser')

print("Page title : ", doc.title.text)

videos_divs = doc.find_all('div', class_="ytd-video-renderer")

print(f'We have found {len(videos_divs)} videos')