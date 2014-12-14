import requests
import urllib
import urlparse
import re
from lxml import html
import pdb
import os
import sys

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
    
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    
    os.chdir(dir_name)

    download(year,month, month_dict[str(month)])

def download(year, month, month_full):
    
    for i in range(1,100):
        url = BASE_URL.format(year,month,i)
        r = requests.get(url)
        
        text = r.text
        tree = html.fromstring(text)
        #pdb.set_trace()
         
        try:

            month_list = tree.xpath('//ul[@id="collapsArch-{0}:3"]/li[@class="collapsing archives"]/a/@title'.format(year))
            count_list = tree.xpath('//ul[@id="collapsArch-{0}:3"]/li[@class="collapsing archives"]/a/span[@class="monthCount"]/text()'.format(year))
            for_an_error = tree.xpath('//ul[@id="collapsArch-{0}:3"]/li[@class="collapsing archives"]/a/span[@class="monthCount"]/text()'.format(year))[0]
            
            cur_month = month_list.index(month_full)
            cur_count = count_list[cur_month]

            cur_count = cur_count[1:-1]
            
            if tree.xpath('//div[@class="entry-content"]/p/img'):
                img_url = tree.xpath('//div[@class="entry-content"]/p/img/@src')[0]
            elif tree.xpath('//div[@class="entry-content"]/p/a/img/@src'):
                img_url = tree.xpath('//div[@class="entry-content"]/p/a/img/@src')[0]
            else:
                continue

            img_url = fixurl(img_url)
            title = tree.xpath( '//h1[@class="entry-title"]/a/text()')[0].encode('utf-8').decode('ascii','ignore')
            print 'Downloading ({1} of {2}) {0}'.format(title,i,cur_count)
            urllib.urlretrieve(img_url,title+'.jpg')
        
        except IndexError:
            
            print '{0} images downloaded'.format(i-1)
            print 'Enough for this month'
            break
        
        except Exception as e:
            
            print 'Looks like some problem came'
            print 'It is due to {0}'.format(e)
            break

if __name__ == "__main__":
    
    year = sys.argv[1]
    month = sys.argv[2]
    create_dir(year,month)
