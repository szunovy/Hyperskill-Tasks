import requests
from bs4 import BeautifulSoup
import string
import os


def stage1():
    url = input()
    try:
        response = requests.get(url)
        # print(response)
    except:
        pass
    else:
        response_code = response.status_code
        if response_code == 200 and 'content' in response.json().keys():
            print(response.json()['content'])
        else:
            print('Invalid quote resource!')


def stage2():
    # url = 'https://www.nature.com/articles/d41586-023-00103-3'
    url = input()

    if not{'www.nature.com', 'articles'}.issubset(set(url.split('/'))):
        print('Invalid page!')
        return None

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())
    # print('---------------')

    # print(soup.find_all('meta'))
    description = soup.find('meta', attrs = {'name':'description'}).get('content')
    contents_dict = {'title': soup.title.string, 'description': description}
    print(contents_dict)

    # for line in soup.find_all('meta'):
    #     print(line)
    #     if line['name'] == 'dc.description':
    #         print('smig')
    # response_code = response.status_code
    # if response_code == 200:
    #     print(response.json())
    # else:
    #     print('Invalid quote resource!')

def stage3():
    # url = 'https://www.nature.com/articles/d41586-023-00103-3'
    url = input()
    response = requests.get(url)
    # print(response.status_code)
    if response.status_code == 200:
        with open('source.html', 'wb') as file:
            file.write(response.content)
            status = 'Content saved'

    else:
        status = f'The URL returned {response.status_code}'

    print(status)


def stage4():
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser' )
    articles = soup.find_all('article')
    for a in articles:
        article_type = a.findNext('span', {'data-test':'article.type'}).contents[1].text
        if article_type == 'News':
            link = a.findNext('a', href=True)['href']
            article_page = requests.get('https://www.nature.com'+link)
            soup_article = BeautifulSoup(article_page.content, 'html.parser')

            title = soup_article.find('h1').get_text()
            title = title.strip(string.punctuation+"’")
            title = title.replace(' ','_')

            text = soup_article.find('p', attrs = {'class' : 'article__teaser'}).get_text()
            with open(title+'.txt', 'wb') as file:
                file.write(text.encode('UTF-8'))

def stage5(Number_of_pages, article_type_searched):
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='

    for i in range(1, Number_of_pages + 1):
        directory = f'./Page_{i}/'
        print(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)

        url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='+str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser' )
        articles = soup.find_all('article')

        for a in articles:
            article_type = a.findNext('span', {'data-test':'article.type'}).contents[1].text
            if article_type == article_type_searched:
                link = a.findNext('a', href=True)['href']
                article_page = requests.get('https://www.nature.com'+link)
                soup_article = BeautifulSoup(article_page.content, 'html.parser')

                title = soup_article.find('h1').get_text()

                pct = string.punctuation
                title = title.strip(pct+"’")
                title = title.replace(' ','_')

                text = soup_article.find('p', attrs = {'class' : 'article__teaser'}).get_text()

                print(title)
                print(text)
                with open(directory+title+'.txt', 'wb') as file:
                    file.write(text.encode('UTF-8'))





def main():
    # stage1()
    # stage2()
    # stage3()
    # stage4()
    # stage5(Number_of_pages = input(), article_type_searched = input())
    stage5(Number_of_pages = int(10), article_type_searched = 'News')
if __name__ == "__main__":
    main()