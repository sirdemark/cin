import csv
import uuid

yappy_link_base = 'https://cdn-st.rutubelist.ru/media/'
yappy_thumbnail_base = 'https://cdn-st.rutubelist.ru/static/pic/thumbnails/'
rutube_base = 'https://rutube.ru/play/embed/'

def generate_yappy_link_and_thumbnail(yappy_uuid):
    yappy_uuid = uuid.UUID(yappy_uuid).hex
    link = f'{yappy_link_base}{yappy_uuid[0:2]}/{yappy_uuid[2:4]}/{yappy_uuid[4:]}/hd.mp4'
    thumbnail = f'{yappy_thumbnail_base}{yappy_uuid}.jpeg'
    return link, thumbnail

def generate_rutube_embed(rutube_link):
    rutube_uuid = rutube_link.split('/')[-1]
    return f'{rutube_base}{rutube_uuid}'


with open('films.csv') as ff:
    with open('feed.py', 'w') as feedf:
        feedf.write('FEED_ITEMS = [\n')
        for row in csv.DictReader(ff, delimiter=';'):
            yappy_uuid = row['UUID']
            description = row['Описание']
            rutube_link = row['Ссылка рутуб']
            if not rutube_link:
                continue
            feedf.write('\t{\n')
            link, thumbnail = generate_yappy_link_and_thumbnail(yappy_uuid)
            embed = generate_rutube_embed(rutube_link)
            feedf.write(f'\t\t"link": "{link}", "description": "{description}", "embed_url": "{embed}", "thumbnail_url": "{thumbnail}"\n')
            feedf.write('\t},\n')
        
        feedf.write(']\n')
