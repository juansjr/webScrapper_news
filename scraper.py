import requests
import lxml.html as html
import os
import datetime
from requests.models import Response

url ='https://www.elespectador.com/'
XPATH_LINK_TO_ARTICLE = '//h2[@class="Card-Title Title Title"]/a/@href'
XPATH_TITLE = '//h1[@class = "Title ArticleHeader-Title Title_article"]/text()'
XPATH_SUMMARY = '//div[@class = "Hook ArticleHeader-Hook Hook_main"]/div/text()'
XPATH_BODY = '//p[@class ="font--secondary"]/text()'


def parse_notice(link, today):

    try :
        response = requests.get(link)
        if response.status_code == 200 :
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'news/{today}/{title}', 'w', encoding = 'utf-8') as f:
                f.write(title)
                f.write(os.linesep)
                f.write(os.linesep)
                f.write(summary)
                f.write(os.linesep)
                f.write(os.linesep)
                for paragraph in body:
                    f.write(paragraph )
                    f.write(os.linesep)
                                   



        else:
            raise ValueError(f'Error:{response.status_code}')

    except ValueError as ve:
        print(ve)


def parse_home():
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)
            links_to_notices_complete = []

            for i in links_to_notices :                             
                i = url[:-1]+i
                #print(i)
                links_to_notices_complete.append(i)            
            
            #print(links_to_notices_complete)      
                   
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices_complete:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error:{response.status_code}')
    except ValueError as ve:
        print(ve)
        


def run():
    parse_home()


if __name__ =='__main__':
    run()