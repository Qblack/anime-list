from marshmallow import Schema, fields, post_load

import procure_images


class Anime(object):
    def __init__(self, japanese_title=None, english_title=None, my_rating=None, mal_score=None, mal_rating=None,
                 mal_ranking=None, mal_genres=None, mal_url=None, mal_image_link=None, mal_summary=None):
        self.japanese_title = japanese_title
        self.english_title = english_title
        self.my_rating = my_rating
        self.mal_score = mal_score
        self.mal_rating = mal_rating
        self.mal_ranking = mal_ranking
        self.mal_genres = mal_genres
        self.mal_url = mal_url
        self.mal_image_link = mal_image_link
        self.mal_summary = mal_summary.strip()

    @property
    def title(self):
        return self.japanese_title if self.japanese_title else self.english_title

    def __repr__(self):
        return f'<Anime(title={self.title})>'

    def make_list_element(self):
        return f'''<li>
            <div class="col s12 m8 offset-m2 l6 offset-l3">
                <div class="card-panel grey lighten-5 z-depth-1">
                    <div class="row valign-wrapper">
                        <div class="col s2">
                            <img src="{self.mal_image_link}" alt="{self.title}"
                                 class="display-image responsive-img">
                        </div>
                        <div class="col s10">
                            <div class="row">
                                <div class="col s3">
                                    <a href="{self.mal_url}" target="_blank">
                                        <h4 class="title top-title">{self.title}</h4>
                                    </a>
                                    <h5 class="display-inline">My Tier: </h5>
                                    <div class="display-inline loud">{self.my_rating}</div>
                                </div>
                                <div class="col s2">
                                    <h5 class="display-inline">Score: </h5>
                                    <div class="display-inline loud">{self.mal_score}</div>
                                    <br>
                                    <h5 class="display-inline">Ranking:</h5>
                                    <div class="display-inline loud">{self.mal_ranking}</div>
                                    <h5 class="display-inline">Rating:</h5>
                                    <div class="display-inline loud">{self.mal_rating}</div>
                                </div>
                                <div class="col s2">
                                    <h5 class="top-title">Genres:</h5>
                                    {', '.join(self.mal_genres)}
                                </div>
                            </div>
                            <div class="row">
                                <div class="col col-12">
                                    <h5>Summary:</h5>
                                    <p>
                                        {self.mal_summary}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </li>'''


class AnimeSchema(Schema):
    japanese_title = fields.Str()
    english_title = fields.Str()
    my_rating = fields.Str()
    mal_score = fields.Str()
    mal_rating = fields.Str()
    mal_ranking = fields.Str()
    mal_genres = fields.Str()
    mal_url = fields.Str()
    mal_image_link = fields.Str()
    mal_summary = fields.Str()
    soup = fields.Str()

    @post_load
    def scrape_soup(self, data):
        mal_url = data.get('mal_url')
        if mal_url and data.get('mal_score') is None:
            soup = procure_images.get_soup(mal_url)
            title = data.get('japanese_title') if data.get('japanese_title') else data.get('english_title')
            data['mal_image_link'] = procure_images.get_image(title, soup)
            data['mal_score'] = procure_images.get_score(soup)
            data['mal_summary'] = procure_images.get_summary(soup)
            data['mal_ranking'] = procure_images.get_ranking(soup)
            data['mal_rating'] = procure_images.get_rating(soup)
            data['mal_genres'] = procure_images.get_genres(soup)

        return Anime(**data)
