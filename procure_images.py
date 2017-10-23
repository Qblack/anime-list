import functools

import time
from bs4 import BeautifulSoup
import requests

urls = (
    'https://myanimelist.net/anime/1535/Death_Note',
    'https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood',
    'https://myanimelist.net/anime/28171/Shokugeki_no_Souma',
    'https://myanimelist.net/anime/22297/Fate_stay_night__Unlimited_Blade_Works',
    'https://myanimelist.net/anime/23273/Shigatsu_wa_Kimi_no_Uso',
    'https://myanimelist.net/anime/33206/Kobayashi-san_Chi_no_Maid_Dragon',
    'https://myanimelist.net/anime/31964/Boku_no_Hero_Academia',
    'https://myanimelist.net/anime/2001/Tengen_Toppa_Gurren_Lagann',
    'https://myanimelist.net/anime/31043/Boku_dake_ga_Inai_Machi',
    'https://myanimelist.net/anime/18153/Kyoukai_no_Kanata', 'https://myanimelist.net/anime/31953/New_Game',
    'https://myanimelist.net/anime/19815/No_Game_No_Life', 'https://myanimelist.net/anime/31798/Kiznaiver',
    'https://myanimelist.net/anime/23755/Nanatsu_no_Taizai', 'https://myanimelist.net/anime/35062/Mahoutsukai_no_Yome',
    'https://myanimelist.net/anime/18679/Kill_la_Kill', 'https://myanimelist.net/anime/16498/Shingeki_no_Kyojin',
    'https://myanimelist.net/anime/22199/Akame_ga_Kill',
    'https://myanimelist.net/anime/30276/One_Punch_Man',
    'https://myanimelist.net/anime/28121/Dungeon_ni_Deai_wo_Motomeru_no_wa_Machigatteiru_Darou_ka',
    'https://myanimelist.net/anime/31646/3-gatsu_no_Lion',
    'https://myanimelist.net/anime/31764/Nejimaki_Seirei_Senki__Tenkyou_no_Alderamin',
    'https://myanimelist.net/anime/9756/Mahou_Shoujo_Madoka%E2%98%85Magica',
    'https://myanimelist.net/anime/27989/Hibike_Euphonium',
    'https://myanimelist.net/anime/31859/Hai_to_Gensou_no_Grimgar', 'https://myanimelist.net/anime/34599/Made_in_Abyss',
    'https://myanimelist.net/anime/34104/Knights___Magic',
    'https://myanimelist.net/anime/33489/Little_Witch_Academia_TV',
    'https://myanimelist.net/anime/28907/Gate__Jieitai_Kanochi_nite_Kaku_Tatakaeri',
    'https://myanimelist.net/anime/28623/Koutetsujou_no_Kabaneri',
    'https://myanimelist.net/anime/8795/Panty___Stocking_with_Garterbelt',
    'https://myanimelist.net/anime/28497/Rokka_no_Yuusha',
    'https://myanimelist.net/anime/30901/Utawarerumono__Itsuwari_no_Kamen',
    'https://myanimelist.net/anime/34561/Re_Creators', 'https://myanimelist.net/anime/6213/Toaru_Kagaku_no_Railgun',
    'https://myanimelist.net/anime/2966/Ookami_to_Koushinryou', 'https://myanimelist.net/anime/32615/Youjo_Senki',
    'https://myanimelist.net/anime/28423/Kyoukai_no_Rinne_TV', 'https://myanimelist.net/anime/34012/Isekai_Shokudou',
    'https://myanimelist.net/anime/35240/Princess_Principal', 'https://myanimelist.net/anime/34494/Sakura_Quest',
    'https://myanimelist.net/anime/25013/Akatsuki_no_Yona', 'https://myanimelist.net/anime/20853/Hitsugi_no_Chaika',
    'https://myanimelist.net/anime/31240/Re_Zero_kara_Hajimeru_Isekai_Seikatsu',
    'https://myanimelist.net/anime/30831/Kono_Subarashii_Sekai_ni_Shukufuku_wo',
    'https://myanimelist.net/anime/35079/Kino_no_Tabi__The_Beautiful_World_-_The_Animated_Series',
    'https://myanimelist.net/anime/31442/Musaigen_no_Phantom_World',
    'https://myanimelist.net/anime/32951/Rokudenashi_Majutsu_Koushi_to_Akashic_Records',
    'https://myanimelist.net/anime/31339/Drifters')


def get_image(title, soup):
    try:
        img = soup.find('img', attrs={'alt': title})
        image_path = img.attrs['src']
    except Exception as e:
        image_path = soup.find_all('img')[1].attrs['src']
    return image_path


def get_rating(soup: BeautifulSoup):
    rating_span = soup.find('span', attrs={'itemprop': 'ratingValue'})
    return rating_span.text


@functools.lru_cache(maxsize=128, typed=False)
def get_soup(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    return soup


def get_title(url):
    return url.split('/')[-1].replace('_', ' ')


def get_full_title(soup):
    name_span = soup.find('span', attrs={'itemprop': 'name'})
    return name_span.text


def get_summary(soup):
    try:
        description = soup.find('span', attrs={'itemprop': "description"})
    except:
        description = soup.find('span', attrs={'itemprop': "synopsis"})

    return description.text


def get_genres(soup):
    section = soup.find('span', text='Genres:')
    genres = [genre.text for genre in section.parent.find_all('a')]
    return genres


def get_ranking(soup):
    span = soup.find('span', attrs={'class': 'numbers ranked'})
    rank = span.text
    return rank


def main():
    with open('anime_list.csv', 'w+') as fh:
        import csv
        dw = csv.DictWriter(fh, fieldnames=('title', 'score', 'ranking', 'genres', 'url', 'image_path', 'summary'))
        dw.writeheader()

        for url in urls:
            try:
                soup = get_soup(url)
                # title = get_title(url)
                title = get_full_title(soup)
                image_path = get_image(title, soup)
                rating = get_rating(soup)
                summary = get_summary(soup)
                genres = ', '.join(get_genres(soup))
                ranking = get_ranking(soup)
                li = '''<li>
            <div class="col s12 m8 offset-m2 l6 offset-l3">
                <div class="card-panel grey lighten-5 z-depth-1">
                    <div class="row valign-wrapper">
                        <div class="col s2">
                            <img src="{image_path}" alt="{title}"
                                 class="display-image responsive-img">
                        </div>
                        <div class="col s10">
                            <div class="row">
                                <div class="col s3">
                                    <a href="{url}">
                                        <h4 class="title top-title">{title}</h4>
                                    </a>
                                </div>
                                <div class="col s2">
                                    <h5 class="display-inline">Score: </h5>
                                    <div class="display-inline loud">{score}</div>
                                    <br>
                                    <h5 class="display-inline">Ranking:</h5>
                                    <div class="display-inline loud">{ranking}</div>
                                </div>
                                <div class="col s2">
                                    <h5>Genres:</h5>
                                    {genres}
                                </div>
                            </div>
                            <div class="row">
                                <div class="col col-12">
                                    <h6>Summary:</h6>
                                    <p>
                                        {summary}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </li>'''.format(image_path=image_path, title=title, score=rating, summary=summary, url=url, genres=genres,
                        ranking=ranking)
                time.sleep(1)
                print(li)
                anime = dict(image_path=image_path, title=title, score=rating, summary=summary, url=url, genres=genres,
                             ranking=ranking)
                dw.writerow(anime)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
