import requests
import urllib
import re
from lxml import html
import pdb
import os

BASE_URL = 'http://www.commitstrip.com/en/{0}/{1}/page/{2}'

def create_dir(year, month):
    
    month_dict = {
        '1':'January',
        '2':'February',
        '3':'March',
        '4':'April',
        '5':'May',
        '6':'June',
        '7':'July',
        '8':'August',
        '9':'September',
        '10':'October',
        '11':'November',
        '12':'December'
    }

    dir_name = "{0} {1}".format(month_dict[str(month)],year)
    os.mkdir(dir_name)
    os.chdir(dir_name)

    download(year,month)

def download(year, month):
    
    for i in range(4,100):
        url = BASE_URL.format(year,month,i)
        pdb.set_trace()
        r = requests.get(url)
        text = r.text
        tree = html.fromstring(text)
        
        try:
            pdb.set_trace()
            img_url = tree.xpath('//div[@class="entry-content"]/p/img/@src')[0]
            title = tree.xpath( '//h1[@class="entry-title"]/a/text()')[0].encode('utf-8').decode('ascii','ignore')
            print 'Downloading {0}'.format(title)
            urllib.urlretrieve(img_url,title+'.jpg')
        
        except IndexError:
            
            print 'Enough for this month'
            break
        
        except Exception as e:
            
            print 'Looks like some problem came'
            print 'It is due to {0}'.format(e)
            break

if __name__ == "__main__":
    create_dir(2014,11)
