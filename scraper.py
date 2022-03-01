import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_URL ='https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  VIDEO_DIV_TAG='ytd-video-renderer'
  driver.get(YOUTUBE_TRENDING_URL)
  driver.page_source # <=== This line is very for this function to work
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID, "video-title")
  title = title_tag.text
  url = title_tag.get_attribute('href')
  
  channel = video.find_element(By.ID, 'channel-name').text
  description = video.find_element(By.ID, 'description-text').text
  thumbnail_url = video.find_element(By.TAG_NAME, 'img').get_attribute('src')
  video_duration = video.find_element(By.ID, 'text').text

  meta_data = video.find_element(By.ID, 'metadata-line').find_elements(By.TAG_NAME, 'span')
  number_of_views = meta_data[0].text
  publication_date = meta_data[1].text
  
  return {
    "title":title,
    "url":url,
    "video_duration":video_duration,
    "publication_date":publication_date,
    "number_of_views":number_of_views,
    "channel":channel,
    "thumbnail_url":thumbnail_url,
    "description":description
  }

  
if __name__=="__main__":
  driver = get_driver()
  print("Fetch data from Youtube")
  
  videos = get_videos(driver)
  print(f'========> We found {len(videos)} videos')

  print('========> Parse top ten vidéo')
  
  videos_parses = [parse_video(video) for video in videos[:10]]

  data = pd.DataFrame(videos_parses)
  print(data)

  data.to_csv("trending.csv", index=None)

