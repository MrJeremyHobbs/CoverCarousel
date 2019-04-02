import configparser
import requests
import xmltodict
import re
import os
import shutil
from PIL import Image
from PIL import ImageFilter
from random import randint

# clean-up
os.system("clean.bat")

# configs
config = configparser.ConfigParser()
config.read('config.ini')

alma_api         = config['general']['alma_apikey']
cc_id            = config['general']['cc_id']
set_id           = config['general']['set_id']
retrieval_method = config['retrieval']['method']
search_limit     = config['retrieval']['search_limit']


# main
def main():
    # get number of items in set
    set_xml = requests.get("https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/"+set_id+"?apikey="+alma_api).text
    
    set_summary = xmltodict.parse(set_xml)
    total_items = int(set_summary['set']['number_of_members']['#text'])
    offsets = []
    
    if retrieval_method == 'random':
        search_range = total_items + total_items
        
    if retrieval_method == 'incremental':
        search_range = total_items
        
    if retrieval_method == 'set_limit':
        search_range = search_limit
    
    for i in range(search_range):
        # start console log
        print("---------------------------------------------------------------------------------------")
        print("#"+str(i+1))
    
        # generate pseudo-random number string within set range
        if retrieval_method == 'random':
            offset = str(randint(0,total_items))
            if offset in offsets:
                print("STATUS:\t\tSKIPPED. RANDOM INTEGER ALREADY CHOSEN.")
                continue
            else:
                offsets.append(offset)
        else:
            offset = str(i + 1)
            
        # check if last item in set already reached
        if i + 1 > total_items:
            print("STATUS:\t\tSKIPPED. RANDOM INTEGER OUT OF BOUNDS.")
            continue
        
        # get set
        limit = str(1) # only want one item at a time
        set_member_xml = requests.get("https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/"+set_id+"/members?limit="+limit+"&offset="+offset+"&apikey="+alma_api).text
        set_member_dict = xmltodict.parse(set_member_xml)
        link = set_member_dict['members']['member'].get('@link')
        link_split = link.split("/")
        mms_id = link_split[6]
        
        # get isbn from summary
        bib_xml = requests.get("https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/"+mms_id+"?view=brief&expand=None&apikey="+alma_api).text
        bib_dict = xmltodict.parse(bib_xml)
        title = str(bib_dict['bib'].get('title'))
        isbn = bib_dict['bib'].get('isbn')
        
        if isbn == None:
            print(title[:55])
            print("STATUS:\t\tSKIPPED. NO ISBN")
            continue
        
        isbn = re.sub('[^0-9]','', isbn) #removes non-numerical chars
        isbn = str(isbn)
        
        # continue console log
        print(title[:55])
        print(isbn)
        
        # check if isbn already rejected
        already_rejected = os.listdir("./rejects/")
        if isbn+".jpg" in already_rejected:
            print("STATUS:\t\tSKIPPED. ALREADY REJECTED (LOW QUALITY)")
            continue
        
        # check if cover already downloaded today        
        already_downloaded_today = os.listdir("./daily/")
        if isbn+".jpg" in already_downloaded_today:
            print("STATUS:\t\tSKIPPED. ALREADY DOWNLOADED TODAY")
            continue
        
        # check if cover already downloaded in cache
        already_downloaded_cache = os.listdir("./cache/")
        if isbn+".jpg" in already_downloaded_cache:
            shutil.copyfile("./cache/"+isbn+".jpg", "./daily/"+isbn+".jpg")
            print("STATUS:\t\tSKIPPED. ALREADY DOWNLOADED IN CACHE")
            continue
        
        # get cover image
        cover_raw = requests.get("http://contentcafecloud.baker-taylor.com/Jacket.svc/"+cc_id+"/"+isbn+"/Original/Empty", stream=True)
        save_file = "./transit/"+isbn+".jpg"
        file = open(save_file, 'wb')
        file.write(cover_raw.content)
        file.close()
        
        # open image for editing
        try:
            im = Image.open(save_file)
        except OSError:
            print("STATUS:\t\tSKIPPED. BAD FILE")
            continue
            
        # check quality
        if os.path.getsize(save_file) < 50000:
            shutil.copyfile("./transit/"+isbn+".jpg", "./rejects/"+isbn+".jpg")
            print("STATUS:\t\tSKIPPED. LOW QUALITY IMAGE.")
            continue
            
        # resize image    
        resized_image = im.resize((1080, 1920), Image.LANCZOS)
        resized_image.save("./cache/"+isbn+".jpg", 'JPEG', quality=95)
        resized_image.save("./daily/"+isbn+".jpg", 'JPEG', quality=95)
        
        # finish
        print("STATUS:\t\tFOUND.")
        
    # copy appropriate number of slides into main folder
    slides = os.listdir('.\\daily\\slides\\')
    num_of_slides = len(slides)
    files = os.listdir('.\\daily\\')
    total_slides_needed = int(len(files)*.60)
    copy_multipler = int(total_slides_needed / num_of_slides)
    
    copy_counter = 1
    for slide in slides:
        for i in range(copy_multipler):
            shutil.copyfile(f'.\\daily\\slides\{slide}', f'.\\daily\\slide{copy_counter}.png')
            copy_counter += 1
        
        
    # end of script
    print("Finished. Entire set has been searched.")
        
if __name__ == '__main__':
    main()