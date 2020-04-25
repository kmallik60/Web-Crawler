# Web-Crawler
This web crawler, gets names, images and personality traits of persons from Wikipedia and stores them in Excel and SQL Database

The uploaded files are the final output from the python file. To run this on your system, create a directory named 'images' and run the .py file from the parent directory.

File unavailable.jpg must be stored in images folder.

The code in this program goes through 2 main websites to get the Names of Indian Film Actors/Actresses, from the main website it crawls and scraps individual Actor/Actress Wikipedia page and gets the URL and DOB of the person. 

URL of the person is used to download the image in .jpg format and store in /images folder, from the /images folder the images are converted to BLOB format for SQLlite Database storage of images.
As all the Actors/Actresses photos are not available in Wikipedia Database, unavailable.jpg is attached to the folder, using that the program stores the name and personality traits in the database even if the photo is unavailable. 

Personality Traits are determined by their respective DOB and Zodiac Signs.
