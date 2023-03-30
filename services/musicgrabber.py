from bs4 import BeautifulSoup
import requests, os, re
from urllib.parse import urlparse
from urllib.parse import unquote
import eyed3

download_folder = "C:/Users/harsha galla/Music"


def grab_albums(urls: list):
    links = {}
    for url in urls:
        links[url] = grab_album(url)
    return links


def grab_album(url: str):
    try:
        album_page = requests.get(url)
        album_soup = BeautifulSoup(album_page.text, 'html.parser')
        links = album_soup.find('span', class_='entry-content').findAll('a')
        hq_links = [k['href'] for k in links if 'HQ' in k['href']]
        if len(hq_links) == 0:
            hq_links = set([a['href'] for a in links])
        album_info = deduce_album(album_soup)
        download_links(album_info, hq_links)
    except Exception as ex:
        print(ex)
        print('Error processing url::' + url)
    return hq_links


def deduce_album(album_soup):
    album_text = album_soup.find('h1').text
    regex = r"\w+"
    matches = [x for x in re.findall(regex, album_text) if 'Songs' not in x]
    return {"album": matches[0], "year": matches[1]}


def download_links(album_info: str, links: list):
    album_name = album_info['album'] + " (" + album_info['year'] + ")"
    directory = os.path.join(download_folder, album_name)
    if not os.path.exists(directory):
        os.mkdir(directory)
    for link in links:
        a = urlparse(link)
        file_name = unquote(os.path.basename(a.path))

        download = requests.get(link, allow_redirects=True)
        fname_fixed_with_path = directory + '/' + file_name
        with open(fname_fixed_with_path, 'wb') as r:
            r.write(download.content)
            r.flush()
            audio_file = eyed3.load(fname_fixed_with_path)
            audio_file.tag.album = album_name
            audio_file.tag.save()
