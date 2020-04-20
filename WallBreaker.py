#!/usr/bin/env python
# coding: utf-8

# # NewsReader

# In[1]:


# Import required modules
import requests
import streamlit as st
from bs4 import BeautifulSoup

# Info
st.sidebar.title('WallBreaker')
st.sidebar.info('WallBreaker enables you to break past paywall-locked articles on popular news sites.\n\nChoose a source, input a URL, and hit Get Article!')

# Radio buttons to select source
news_source = st.sidebar.radio(
    'Select a news source:',
    ('Straits Times', 'New York Times')
)

# Text input
article_url = st.sidebar.text_input('Article URL:', '')

# Run button
get_article_btn = st.sidebar.button('Get Article!', key='get_article_btn')

if news_source == 'Straits Times':
    
    # Image
    st.markdown('<div align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/The_Straits_Times_Logo.svg/1280px-The_Straits_Times_Logo.svg.png" height=70></div>', unsafe_allow_html=True)

    # If clicked
    if get_article_btn:
        if article_url[:4] == 'http':
            
            # Scrape site
            response = requests.get(
                article_url,
                headers= {
                    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
                    "cache-control":"max-age=0",
                    "if-modified-since":"Mon, 20 Apr 2020 12:17:01 GMT",
                    "if-none-match":"\"1587385021-0-gzip\"",
                    "sec-fetch-dest":"document",
                    "sec-fetch-mode":"navigate",
                    "sec-fetch-site":"none",
                    "sec-fetch-user":"?1",
                    "upgrade-insecure-requests":"1"
                })
            soup = BeautifulSoup(response.content)

            # Extract title
            title = '# ' + soup.find('div', attrs={'class': 'a2a-buttons a2a_kit a2a_kit_size_32 a2a_default_style'})['data-a2a-title']

            # Extract article
            text_list = soup.find_all('div', attrs={'class': 'field-items'})[4]

            article = title + '\n\n'

            for i, t1 in enumerate(text_list.find_all()[1:]):
                if 'Related Story' in t1.text:
                    continue
                if 'class' in t1.attrs.keys():
                    if 'related-story' in ' '.join(list(t1.attrs.values())[0]) or 'label-above' in ' '.join(list(t1.attrs.values())[0]):
                        continue
                if any(x in str(t1) for x in ['<scr', '<fig', '<br', '<img', '<ifr', '<ul', '<strong']):
                    continue

                if str(t1)[:3] == '<a ':
                    continue
                if str(t1)[:3] == '<hr':
                    continue

                if str(t1)[:4] == '<div':
                    for j, t2 in enumerate(t1.find_all()):
                        if str(t2)[:4] != '<div' and str(t2)[:4] != '<scr' and str(t2)[:4] != '<ifr' and str(t2)[:4] != '<fig' and str(t2)[:3] != '<a ' and str(t2)[:4] != '<img' and str(t2)[:3] != '<br':
                            if str(t2)[:3] == '<h2':
                                print(i,j,'\n## ' + t2.text.replace('\n', ''))
                                print()
                                article += '## ' + t2.text.replace('\n', '') + '\n\n'
                            elif str(t2)[:3] == '<h3':
                                print(i,j,'\n### ' + t2.text.replace('\n', ''))
                                print()
                                article += '## ' + t2.text.replace('\n', '') + '\n\n'
                            elif str(t2)[:3] == '<h4':
                                print(i,j,'\n#### ' + t2.text.replace('\n', ''))
                                print()
                                article += '### ' + t2.text.replace('\n', '') + '\n\n'
                            else:
                                if 'figcaption' in str(t2):
                                    continue
                                else:
                                    print(i,j,t2.text)
                                    print()
                                    article += t2.text.replace('\n', '') + '\n\n'
                elif str(t1)[:4] == '<li ':
                    article += '**[SUSPECTED AD]**\n\n'
                    print(i, '\n<SUSPECTED AD>')
                elif str(t1)[:3] == '<h2':
                    article += '## ' + t1.text.replace('\n', '') + '\n\n'
                    print(i,'\n## ' + t1.text.replace('\n', ''))
                elif str(t1)[:3] == '<h3':
                    article += '## ' + t1.text.replace('\n', '') + '\n\n'
                    print(i,'\n### ' + t1.text.replace('\n', ''))
                elif str(t1)[:3] == '<h4':
                    article += '### ' + t1.text.replace('\n', '') + '\n\n'
                    print(i,'\n#### ' + t1.text.replace('\n', ''))
                else:
                    article += t1.text.replace('\n', '') + '\n\n'
                    print(i,'\n' + t1.text.replace('\n', ''))

            # Print
            st.markdown(article)

elif news_source == 'New York Times':
    
    # Image
    st.markdown('<div align="center"><img src="https://civiliansinconflict.org/wp-content/uploads/2017/09/New-York-Times-Logo.png" height=140></div>', unsafe_allow_html=True)
    
    # If clicked
    if get_article_btn:
        if article_url[:4] == 'http':
    
            # Scrape site
            response = requests.get(article_url)
            soup = BeautifulSoup(response.content)
            
            # Extract title
            title = '# ' + soup.find('h1', attrs={'itemprop': 'headline'}).text

            # Extract authors
            authors = soup.find('p', attrs={'itemprop': 'author'}).text

            # Extract date
            
            date = soup.find('article').find('time').text

            # Subtitle
            subtitle = '*' + authors + ' - ' + date + '*'
            
            # Configure article
            top = title + '\n' + subtitle + '\n\n'
            
            # Scrape header image
            img_url = soup.find('div', attrs={'class': 'css-79elbk'}).find('figure')['itemid']
            
            # Initialise article body text
            article = ''
            
            # Scrape article
            for div in soup.find_all('div', attrs={'class': 'css-53u6y8'}):
                for p in div.find_all('p', attrs={'class': 'css-exrw3m evys1bk0'}):
                    article += '\n\n' + p.text + '\n\n'
            
            # Print
            st.markdown(top)
            st.markdown('<div align="center"><img src="' + img_url + '"></div>', unsafe_allow_html=True)
            st.markdown('\n\n')
            st.markdown('<div style="text-align: justify">' + article + '</div>', unsafe_allow_html=True)