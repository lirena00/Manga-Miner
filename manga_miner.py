# imports
import os
import shutil
import img2pdf  
import cfscrape 

from io import BytesIO
from PIL import Image

def scrape(manga, chapter):
    """
    We are using cfscrape instead of requests here because this site is protected by CloudFlare 
    and cfscrape helps to bypass that 😎
    """

    # creating a cloudflare scraper instance
    scraper = cfscrape.create_scraper() 
    # replacing spaces with dashes
    manga = manga.lower().replace(" ","-")


    if not os.path.exists(f"Mangas/{manga}"):
        # this will create directory with the name of manga
        os.makedirs(f"Mangas/{manga}") 

    if not os.path.exists(f"Mangas/{manga}/{chapter}"):
        # this will create directory with the name of chapter number 
            os.makedirs(f"Mangas/{manga}/{chapter}") 

    paths=[]

    # we are looping it from 1 to 70 because I havent seen any manga which exceed over 70 pages you can change it according to your choice
    for z in range(1,70): 
        url = f"https://img.mghubcdn.com/file/imghub/{manga}/{str(chapter)}/{str(z)}.jpg"
        img = scraper.get(url)

        if img.status_code == 200:
            # reading the contents of page and making it making it image
            image = Image.open(BytesIO(img.content)) 
            path = f"Mangas/{manga}/{chapter}/{str(z)}.jpg"
            image.save(path)
            
            paths.append(path)
        else:
            # sometimes image is in png format so we have to check this one too ... you can use a better way if you know ofc 
            url=f"https://img.mghubcdn.com/file/imghub/{manga}/{str(chapter)}/{str(z)}.png"
            img=scraper.get(url)

            if img.status_code == 200:
                image = Image.open(BytesIO(img.content))
                path = f"Mangas/{manga}/{chapter}/{str(z)}.jpg"
                image.save(path)
                paths.append(path)  
            else: 
                break      
    
    if len(paths) != 0:
        # sorting paths according to their name
        paths = sorted(paths,key=os.path.getmtime) 

        with open(f"Mangas/{manga}/Ch-{chapter}.pdf","wb") as f:
            # converting all images into pdf
            f.write(img2pdf.convert(paths)) 

            # deleting directory which had images since we got our pdf
            shutil.rmtree(f'Mangas/{manga}/{chapter}') 

            print(f'{chapter} of {manga} successfully downloaded')
    else:
        # if manga isnt available it will print this
        print("Manga or chapter isn't available" ) 


if __name__ == "__main__":
    """
    This is the main function which will be called when you run this script
    """

    # inputting manga name and chapter number
    manga = input("Enter manga name: ")
    chapter = input("Enter chapter number: ")
    
    # calling scrape function
    scrape(manga=manga, chapter=chapter)