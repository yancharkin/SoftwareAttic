#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; -*-

# Web Gallery of Art: www.wga.hu

import os, sys, random, lxml, PIL
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import zipfile

try:
    from urllib2 import Request as urllib_request
    from urllib2 import urlopen as urllib_urlopen
    from urllib2 import URLError as urllib_urlerror
    from urllib2 import HTTPError as urllib_httperror
except:
    from urllib.request import Request as urllib_request
    from urllib.request import urlopen as urllib_urlopen
    from urllib.request import URLError as urllib_urlerror
    from urllib.request import HTTPError as urllib_httperror

if sys.platform.startswith('linux'):
    config_dir = os.path.expanduser('~/.config/wga_wallpapers/')
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    tmp_dir = '/tmp/'
elif sys.platform.startswith('win'):
    config_dir = os.path.expanduser('~/wga_wallpapers/')
    font_path = 'C:\\Windows\\Fonts\\Arial.ttf'
    tmp_dir = 'C:\\Windows\\Temp\\'

config_path = config_dir + 'config'
catalog_path = config_dir + 'catalog.csv'

if not os.path.exists(config_dir):
    os.makedirs(config_dir)

if not os.path.exists(config_path):

    text_color_1 = 'white'
    text_color_2 = 'grey'
    info_outline = 'grey'
    info_background_r = 0
    info_background_g = 0
    info_background_b = 0
    info_background_a = 164

    config_file = open(config_path, 'w')
    config_file.write('text_color_1 = white\n')
    config_file.write('text_color_2 = grey\n')
    config_file.write('info_outline = grey\n')
    config_file.write('info_background_r = 0\n')
    config_file.write('info_background_g = 0\n')
    config_file.write('info_background_b = 0\n')
    config_file.write('info_background_a = 164\n')
    config_file.close()

else:

    config_file = open(config_path, 'r')

    text_color_1 = config_file.readline().split(' = ')[1].replace('\n', '')
    text_color_2 = config_file.readline().split(' = ')[1].replace('\n', '')
    info_outline = config_file.readline().split(' = ')[1].replace('\n', '')
    info_background_r = int(config_file.readline().split(' = ')[1].replace('\n', ''))
    info_background_g = int(config_file.readline().split(' = ')[1].replace('\n', ''))
    info_background_b = int(config_file.readline().split(' = ')[1].replace('\n', ''))
    info_background_a = int(config_file.readline().split(' = ')[1].replace('\n', ''))

    config_file.close()

info_background = (
                    info_background_r,
                    info_background_g,
                    info_background_b,
                    info_background_a
)

def get_catalog():

    archive_path = tmp_dir + 'data_txt.zip'

    if not os.path.exists(catalog_path):

        if not os.path.exists(archive_path):
            url = urllib_urlopen('https://www.wga.hu/database/download/data_txt.zip')
            f = open(archive_path, 'wb')
            f.write(url.read())
            f.close()

        zip_file = zipfile.ZipFile(archive_path, 'r')
        zip_file.extractall(config_dir)
        zip_file.close()

def get_raw_data(keywords):

    get_catalog()

    catalog_file = open(catalog_path, 'rb')
    catalog_list_b = catalog_file.readlines()
    catalog_file.close()

    catalog_list = []
    for line in catalog_list_b:
        catalog_list.append(line.decode('ibm850'))

    if keywords != None:
        keywords_list = keywords.split(',')
        new_catalog_list = []
        for line in catalog_list:
            for keyword in keywords_list:
                if keyword.lower() in line.lower():
                    new_catalog_list.append(line)
        catalog_list = list(new_catalog_list)


    number = random.randrange(1, len(catalog_list))

    raw_data = catalog_list[number].split(';')

    if len(raw_data[0].split(',')) > 1:
        author_firstname = raw_data[0].split(',')[1].lstrip().title()
        author_lastname = raw_data[0].split(',')[0].title()
        author = '{} {}'.format(author_firstname, author_lastname)
    else:
        author = raw_data[0].title()

    born_died = raw_data[1]
    title = raw_data[2]
    date = raw_data[3]
    technique = raw_data[4]
    location = raw_data[5]
    url = raw_data[6]
    form = raw_data[7]
    type = raw_data[8]
    school = raw_data[9]
    timeline = raw_data[10]

    req = urllib_request(url)

    try:
        page = urllib_urlopen(req)
        page_content = page.read()
        soup = BeautifulSoup(page_content, 'lxml')

        for line in soup.find_all('a'):
            if '.jpg' in line.get('href'):
                image_link = 'http://www.wga.hu' + line.get('href')

        image_req = urllib_request(image_link)

        image_data = urllib_urlopen(image_req).read()
        image_file = open(tmp_dir + 'wga_wallpapers_image.jpg', 'wb')
        image_file.write(image_data)
        image_file.close()

        return author, born_died, title, date, \
        technique, location, form, type, school, timeline

    except urllib_urlerror as e:
        print(e.reason)
    except urllib_httperror as e:
        print(e.code)
        print(e.read())

def create_wallpaper(path, width, height, font_size, details, keywords):

    width = int(width)
    height = int(height)
    font_size = int(font_size)
    details = int(details)

    author, born_died, title, date, \
    technique, location, form, type, \
    school, timeline = get_raw_data(keywords)

    pic_src = Image.open(tmp_dir + 'wga_wallpapers_image.jpg')
    scale_lvl = width/float(pic_src.size[0])

    scaled_width = int(float(pic_src.size[0])*scale_lvl)
    scaled_height = int(float(pic_src.size[1])*scale_lvl)

    if scaled_height > height:
        scale_lvl = height/float(pic_src.size[1])
        scaled_width = int(float(pic_src.size[0])*scale_lvl)
        scaled_height = int(float(pic_src.size[1])*scale_lvl)

    pic = pic_src.resize((scaled_width, scaled_height), PIL.Image.ANTIALIAS)

    offset = (int((width - scaled_width)/2), int((height - scaled_height)/2))

    background_image = config_dir + 'background.jpg'
    if os.path.exists(background_image):
        wallpaper = Image.open(background_image)
        wallpaper = wallpaper.resize((width, height), PIL.Image.ANTIALIAS)
    else:
        wallpaper = Image.new('RGB', (width, height), 'black')

    wallpaper.paste(pic, offset)

    draw = ImageDraw.Draw(wallpaper)
    font = ImageFont.truetype(font_path, font_size)

    if details != 0:

        text_height = font.getsize(author)[1]
        spacing = text_height/2
        margin = text_height/2
        x_offset = 5
        y_offset = 40

    if details == 1:

        author_width = font.getsize(author)[0]
        title_width = font.getsize(title)[0]

        text_block_width = author_width
        if title_width > text_block_width:
            text_block_width = title_width

        rectangle = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        rectangle_draw = ImageDraw.Draw(rectangle)

        rectangle_draw.rectangle([width - (text_block_width + margin*2), \
        height - (text_height*2 + spacing + margin*2 + y_offset), width - x_offset, height - y_offset],
        fill=info_background, outline=info_outline
        )

        wallpaper.paste(rectangle, mask=rectangle)

        draw.text((width - (text_block_width + margin), \
        height - (text_height*2 + spacing + margin + y_offset)), author, fill=text_color_1, font=font)

        draw.text((width - (text_block_width + margin), \
        height - (text_height + margin + y_offset)), title, fill=text_color_1, font=font)

    if details == 2:

        author_prefix = 'Author: '
        born_died_prefix = 'Born/died: '
        title_prefix = 'Title: '
        date_prefix = 'Date: '
        technique_prefix = 'Technique: '
        school_prefix = 'School: '
        location_prefix = 'Location: '
        # Not important / not useful (?)
        #~ #form
        #~ #type
        #~ #timeline

        author_width = font.getsize(author)[0]
        born_died_width = font.getsize(born_died)[0]
        title_width = font.getsize(title)[0]
        date_width = font.getsize(date)[0]
        technique_width = font.getsize(technique)[0]
        school_width = font.getsize(school)[0]
        location_width = font.getsize(location)[0]

        author_prefix_width = font.getsize(author_prefix)[0]
        born_died_prefix_width = font.getsize(born_died_prefix)[0]
        title_prefix_width = font.getsize(title_prefix)[0]
        date_prefix_width = font.getsize(date_prefix)[0]
        technique_prefix_width = font.getsize(technique_prefix)[0]
        school_prefix_width = font.getsize(school_prefix)[0]
        location_prefix_width = font.getsize(location_prefix)[0]

        text_block_width = author_width + author_prefix_width
        if (born_died_width + born_died_prefix_width) > text_block_width:
            text_block_width = born_died_width + born_died_prefix_width
        if (title_width + title_prefix_width) > text_block_width:
            text_block_width = title_width + title_prefix_width
        if (date_width + date_prefix_width) > text_block_width:
            text_block_width = date_width + date_prefix_width
        if (technique_width + technique_prefix_width) > text_block_width:
            text_block_width = technique_width + technique_prefix_width
        if (school_width + school_prefix_width) > text_block_width:
            text_block_width = school_width + school_prefix_width
        if (location_width + location_prefix_width) > text_block_width:
            text_block_width = location_width + location_prefix_width

        rectangle = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        rectangle_draw = ImageDraw.Draw(rectangle)

        rectangle_draw.rectangle([width - (text_block_width + margin*2), \
        height - (text_height*7 + spacing*6 + margin*2 + y_offset), width - x_offset, height - y_offset],
        fill=info_background, outline=info_outline
        )

        wallpaper.paste(rectangle, mask=rectangle)

        draw.text((width - (text_block_width + margin), \
        height - (text_height*7 + spacing*6 + margin + y_offset)), author_prefix, fill=text_color_2, font=font)
        draw.text((width - (text_block_width + margin) + author_prefix_width, \
        height - (text_height*7 + spacing*6 + margin + y_offset)), author, fill=text_color_1, font=font)

        draw.text((width - (text_block_width + margin), \
        height - (text_height*6 + spacing*5 + margin + y_offset)), born_died_prefix, fill=text_color_2, font=font)
        draw.text((width - (text_block_width + margin) + born_died_prefix_width, \
        height - (text_height*6 + spacing*5 + margin + y_offset)), born_died, fill=text_color_1, font=font)

        draw.text((width - (text_block_width + margin), \
        height - (text_height*5 + spacing*4 + margin + y_offset)), title_prefix, fill=text_color_2, font=font)
        draw.text((width - (text_block_width + margin) + title_prefix_width, \
        height - (text_height*5 + spacing*4 + margin + y_offset)), title, fill=text_color_1, font=font)

        draw.text((width - (text_block_width + margin), \
        height - (text_height*4 + spacing*3 + margin + y_offset)), date_prefix, fill=text_color_2, font=font)
        draw.text((width - (text_block_width + margin) + date_prefix_width, \
        height - (text_height*4 + spacing*3 + margin + y_offset)), date, fill=text_color_1, font=font)

        draw.text((width - (text_block_width + margin), \
        height - (text_height*3 + spacing*2 + margin + y_offset)), technique_prefix, fill=text_color_2, font=font)
        draw.text((width - (text_block_width + margin) + technique_prefix_width, \
        height - (text_height*3 + spacing*2 + margin + y_offset)), technique, fill=text_color_1, font=font)

        draw.text((width - (text_block_width + margin), \
        height - (text_height*2 + spacing*1 + margin + y_offset)), school_prefix, fill=text_color_2, font=font)
        draw.text((width - (text_block_width + margin) + school_prefix_width, \
        height - (text_height*2 + spacing*1 + margin + y_offset)), school, fill=text_color_1, font=font)

        draw.text((width - (text_block_width + margin), \
        height - (text_height + margin + y_offset)), location_prefix, fill=text_color_2, font=font)
        draw.text((width - (text_block_width + margin) + location_prefix_width, \
        height - (text_height + margin + y_offset)), location, fill=text_color_1, font=font)

    if sys.platform.startswith('linux'):
        dir_path_list = path.split('/')
        del dir_path_list[-1]
        dir_path = '/'.join(dir_path_list)
    elif sys.platform.startswith('win'):
        dir_path_list = path.split('\\')
        del dir_path_list[-1]
        dir_path = '\\'.join(dir_path_list)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if os.path.exists(path + '.bak'):
        os.remove(path + '.bak')

    if os.path.exists(path):
        os.rename(path, path + '.bak')

    wallpaper.save(path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 6:
        create_wallpaper(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], None)
    elif len(sys.argv) == 7:
        create_wallpaper(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    else:
        print('\nWrong number of arguments!\
        \n\
        \nUsage:\n\
        \nwga_wallpapers.py <path><width><height><font_size><info> [<keywords>]\
        \n\
        \n  <path>              - where to save image (example: /home/user/wallpaper.jpg)\
        \n  <width>             - image width in pixels (example: 1920)\
        \n  <height>            - image height in pixels (example: 1080)\
        \n  <font_size>         - font size (example: 18)\
        \n  <info>              - how much info print on the image (possible values: 0, 1, 2)\
        \n  <keywords>          - filter images by this keywords (example: "painting, monet, van gogh")\n')
