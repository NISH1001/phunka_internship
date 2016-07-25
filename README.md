# phunka_internship
A repository for pushing my practice session during internship at Phunka.  
The projects are:  

--------------------------------

## Zillow Scraper
Scrap the site [Zillow](http://zillow.com)

--------------------------------

## Amplitude
Use api from [Amplitude](https://amplitude.com) to fetch data from **start time-end time**.  
And insert the data to **PostgreSQL** database using **SQLAlchemy**

--------------------------------

## GeoCoding
Fetch geocode information (lat/long) for the address provided in the excel sheet.

--------------------------------

## Logs
Generate apache logs along with transactions (login attempt) with server with the template provided as JSON.  
Also, dump the transactions data to MySQL database.

--------------------------------

## LoanPredict
A machine learning project to predict whether a customer will get the loan. For now it uses [Random Forest](https://en.wikipedia.org/wiki/Random_forest) algorithm
to train the dataset and hence predict.  

--------------------------------

## InstagramCrawler
A project for crawling [Instagram](https://wwww.instagram.com). The crawler logs in to the user account and fetches all the general information of 
**followers** // **following** like:
- Full Name
- Username
- Biography text
- Followers count
- Following count

The dump data is like:  

```json
{
    "full_name"     : "Full Name",
    "username"      : "username",
    "followers"     : [ user1_data, user2_data, ...],
    "following"     : [ user1_data, user2_data, ...]
}
```

Since **Instagram** is fully dynamic and its api is sandboxed(limited), [Selenium](http://selenium-python.readthedocs.io/index.html) is used to automate
the login, click on the followers/following link and extract all the usernames.

Finally, [Scrapy](http://doc.scrapy.org/en/latest/index.html) is used to crawl all the relevant data for the usernames collected.

--------------------------------







