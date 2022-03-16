import os
from io import BytesIO
import shutil
import img2pdf  #pip install img2pdf
import cfscrape #pip install cfscrape
from PIL import Image

def scrape():
"""
We are using cfscrape instead of requests here because this site is protected by CloudFlare 
and cfscrape helps to bypass that 😎
"""

scraper = cfscrape.create_scraper() #creating a cloudflare scraper instance
manga=input("Enter Manga:")
manga=manga.lower().replace(" ","-") 
chapter=input("Enter Chapter No.:") 
if not os.path.exists(f'Mangas/{manga}'):
        os.makedirs(f'Mangas/{manga}') #this will create directory with the name of manga

if not os.path.exists(f'Mangas/{manga}/{chapter}'):
        os.makedirs(f'Mangas/{manga}/{chapter}') #this will create directory with the name of chapter number 

paths=[]
for z in range(1,70): #we are looping it from 1 to 70 because I havent seen any manga which exceed over 70 pages you can change it according to your choice
    url=f"https://img.mghubcdn.com/file/imghub/{manga}/{str(chapter)}/{str(z)}.jpg"
    img=scraper.get(url)
    if img.status_code == 200:
        image = Image.open(BytesIO(img.content)) #reading the contents of page and making it making it image
        path = f'Mangas/{manga}/{chapter}/{str(z)}.jpg'
        image.save(path)
        
        paths.append(path)
    else:
        #sometimes image is in png format so we have to check this one too ... you can use a better way if you know ofc 
        url=f"https://img.mghubcdn.com/file/imghub/{manga}/{str(chapter)}/{str(z)}.png"
        img=scraper.get(url)
        if img.status_code == 200:
            image = Image.open(BytesIO(img.content))
            path = f'Mangas/{manga}/{chapter}/{str(z)}.jpg'
            image.save(path)
            paths.append(path)  
        else: 
            break      
 
if len(paths) != 0:
    paths=sorted(paths,key=os.path.getmtime) #sorting paths
    with open(f"Mangas/{manga}/Ch-{chapter}.pdf","wb") as f:
        f.write(img2pdf.convert(paths)) #converting all images into pdf
        shutil.rmtree(f'Mangas/{manga}/{chapter}') #deleting directory which had images since we got our pdf
        print(f'{chapter} of {manga} successfully downloaded')
else:
    print("Manga or chapter isn't available" ) #if manga isnt available it will print this
