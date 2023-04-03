"""
This code will download all the videos on an MRSS feed's first page. 
It uses the feedparser python module to parse the xml feed
It uses Pool for parallel download 
usage:  python3 xml_parser.py 
Author: Antonio Orozco Sanchez

"""

import feedparser
import requests
import re
from multiprocessing import Pool


def download_entry(entry):
  #basic values from the mrss feed. Make sure those exist 	
  title 		= entry.title
  published 	= entry.published_parsed
  media			= entry.media_content[0]["url"]
        
  print(published)
  print(title)
  print(media)

  r = requests.get(media)
  title_stripped = title.replace(" ", "") #remove blank spaces
  title_stripped =re.sub("[^A-Z]", "", title_stripped,0,re.IGNORECASE) #remove special characters

  with open(title_stripped+'.mp4', 'wb') as fd: #download file
    fd.write(r.content)

  print("Done with: "+title_stripped+".mp4 complete.") 


def pool_handler():
  feed 			= feedparser.parse('https://moxie.foxbusiness.com/amazon-video.xml')
  feed_entries 	= feed.entries
  p 			= Pool(5)
  p.map(download_entry, feed_entries)


if __name__ == '__main__':
  pool_handler()


