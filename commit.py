import requests
import urllib
import urlparse
import re
from lxml import html
import pdb
import os

BASE_URL = 'http://www.commitstrip.com/en/{0}/{1}/page/{2}'

def fixurl(url):
    # turn string into unicode
    if not isinstance(url,unicode):
        url = url.decode('utf8')

    # parse it
    parsed = urlparse.urlsplit(url)

    # divide the netloc further
    userpass,at,hostport = parsed.netloc.rpartition('@')
    user,colon1,pass_ = userpass.partition(':')
    host,colon2,port = hostport.partition(':')

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = urllib.quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = urllib.quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'),'')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'),'=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user,colon1,pass_,at,host,colon2,port))
    return urlparse.urlunsplit((scheme,netloc,path,query,fragment))

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
    
    for i in range(1,100):
        url = BASE_URL.format(year,month,i)
        pdb.set_trace()
        r = requests.get(url)
        text = r.text
        tree = html.fromstring(text)
        
        try:
            pdb.set_trace()
            img_url = tree.xpath('//div[@class="entry-content"]/p/img/@src')[0]
            img_url = fixurl(img_url)
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
