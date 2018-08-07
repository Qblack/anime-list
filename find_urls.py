import csv

from anime import AnimeSchema, Anime

schema = AnimeSchema()

already_scrapped = {}
with open('anime_scrubbing.csv', 'r') as fh:
    dr = csv.DictReader(fh, delimiter='\t')
    for row in dr:
        anime, errors = schema.load(row)
        already_scrapped[anime.title] = anime

to_write = already_scrapped
with open('anime_names.csv') as fh:
    dr = csv.DictReader(fh, delimiter='\t')
    for row in dr:
        if row['japanese_title'] not in already_scrapped:
            anime, errors = schema.load(row)
            to_write[anime.title] = anime
        elif row['japanese_title'] != already_scrapped[row['japanese_title']]:
            row = {**schema.dump(already_scrapped[row['japanese_title']])[0], **row}
            anime, errors = schema.load(row)
            to_write[anime.title] = anime

sorted_animes = sorted(to_write.values(), key=lambda a: a.my_rating if a.my_rating else 10)

with open('anime_list.html', 'w+') as out, open('anime_scrubbing.csv', 'w+') as out_csv:
    dw = csv.DictWriter(out_csv, fieldnames=(
        'title', 'japanese_title', 'english_title', 'mal_score', 'mal_rating', 'mal_ranking', 'mal_genres', 'mal_url',
        'mal_image_link', 'mal_summary', 'my_rating'), delimiter='\t')
    dw.writeheader()
    for anime in sorted_animes:
        try:
            print(anime.make_list_element(), file=out)
            rep, _ = schema.dump(anime)
            dw.writerow(rep)
        except Exception as e:
            print(anime.title)
