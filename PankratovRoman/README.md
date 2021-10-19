## Python command-line RSS reader  
#### EPAM Python Training final task 2021.09  

---
## INSTALLATION

The program is written in Python 3.9.  
To install the modules required for work, enter:
```bash
pip install -r requirements.txt
```
To install the required modules for development, enter:
```bash
pip install -r dev-requirements.txt
```

---
## USAGE

```bash
usage: main.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      show program's version number and exit
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
```

---
## Example output  

Text output:   

```
Channel:
    Title: Yahoo News - Latest News & Headlines
    Description: The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.
    Date: 2021-10-19 14:31:11-04:00
    Link: https://www.yahoo.com/news
    Image: http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png

Items:
    Number: 1
    Title: Ice-T remembers path not taken in memoir 'Split Decision'
    Description: None
    Date: 2021-10-19 16:46:02+00:00
    Link: https://news.yahoo.com/ice-t-remembers-path-not-164602839.html
    Content: https://s.yimg.com/uu/api/res/1.2/AqpgdtKycupkD_8ahwefKw--~B/aD0yNzc1O3c9MTgzODthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/8f8fa50d0a7b75d406f301aefc14a1eb

    Number: 2
    Title: Trump calls Colin Powell a 'classic RINO' who 'made big mistakes' in Iraq: 'But anyway, may he rest in peace!'
    Description: None
    Date: 2021-10-19 15:12:17+00:00
    Link: https://news.yahoo.com/trump-calls-colin-powell-classic-151217258.html
    Content: https://s.yimg.com/uu/api/res/1.2/iZlNBjADsSf0ceCdh3aMGA--~B/aD0zNjQ4O3c9NDg2NDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/business_insider_articles_888/21625ac31426aecb2d2893ffe31943ee
```

---
Json output:  

```
{
   "title":"Yahoo News - Latest News & Headlines",
   "link":"https://www.yahoo.com/news",
   "description":"The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.",
   "language":"en-US",
   "copyright":"Copyright (c) 2021 Yahoo! Inc. All rights reserved",
   "managing_editor":null,
   "web_master":null,
   "pub_date":"2021-10-19 14:36:11-04:00",
   "last_build_date":null,
   "category":null,
   "generator":null,
   "docs":null,
   "ttl":5,
   "image":{
      "title":"Yahoo News - Latest News & Headlines",
      "link":"https://www.yahoo.com/news",
      "url":"http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png",
      "description":null,
      "width":null,
      "height":null
   },
   "cloud":null,
   "rating":null,
   "text_input":null,
   "items":[
      {
         "title":"Ice-T remembers path not taken in memoir 'Split Decision'",
         "link":"https://news.yahoo.com/ice-t-remembers-path-not-164602839.html",
         "description":null,
         "author":null,
         "category":null,
         "comments":null,
         "enclosure":null,
         "guid":{
            "is_perm_link":false,
            "text":"ice-t-remembers-path-not-164602839.html"
         },
         "pub_date":"2021-10-19 16:46:02+00:00",
         "source":{
            "url": "http://www.ap.org/",
            "text":"Associated Press"
         },
         "content":{
            "url":"https://s.yimg.com/uu/api/res/1.2/AqpgdtKycupkD_8ahwefKw--~B/aD0yNzc1O3c9MTgzODthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/8f8fa50d0a7b75d406f301aefc14a1eb",
            "width":130,
            "height":86
         }
      },
      {
         "title":"Trump calls Colin Powell a 'classic RINO' who 'made big mistakes' in Iraq: 'But anyway, may he rest in peace!'",
         "link":"https://news.yahoo.com/trump-calls-colin-powell-classic-151217258.html",
         "description":null,
         "author":null,
         "category":null,
         "comments":null,
         "enclosure":null,
         "guid":{
            "is_perm_link":false,
            "text":"trump-calls-colin-powell-classic-151217258.html"
         },
         "pub_date":"2021-10-19 15:12:17+00:00",
         "source":{
            "url":"https://www.businessinsider.com/",
            "text":"Business Insider"
         },
         "content":{
            "url":"https://s.yimg.com/uu/api/res/1.2/iZlNBjADsSf0ceCdh3aMGA--~B/aD0zNjQ4O3c9NDg2NDthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/business_insider_articles_888/21625ac31426aecb2d2893ffe31943ee",
            "width":130,
            "height":86
         }
      }
   ]
}
```