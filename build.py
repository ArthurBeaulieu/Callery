#!/usr/bin/env python3


# Python imports
import os
import sys
import argparse
import json


from PIL import Image
from PIL import ImageFile
from PIL.ExifTags import TAGS
ImageFile.LOAD_TRUNCATED_IMAGES = True # Enforce thumbnail creation


# Script main frame
def main():
    # Init argparse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('folder', help='The input folder path to crawl (absolute or relative)')
    ap.add_argument('-s', '--scan', help='Scan a folder to create its associated JSON to be read in the web page', action='store_true')
    args = vars(ap.parse_args())
    # Preventing path from missing its trailing slash (or backslash for win compatibility)
    if not args['folder'].endswith('\\') and not args['folder'].endswith('/'):
        print('ERROR: The given folder path doesn\'t ends with a \\ or a /. Exiting script...')
        sys.exit(-1)
    # Crawl given path and build JSON
    crawlFolder(args)


def crawlFolder(args):
    files = folders = 0
    for _, dirnames, filenames in os.walk(args['folder']):
        files += len(filenames)
        folders += len(dirnames)
        try:
            os.mkdir('./_thumbnails')
        except:
            pass
    with open('MyPictures.json', 'w', encoding='utf-8') as f:
        json.dump(pathToDict(args['folder'], files + folders), f, ensure_ascii=False, indent=2)


objectId = 0
def pathToDict(path, total):
    global objectId
    obj = { os.path.basename(path): {} }
    objKey = obj[os.path.basename(path)]
    objKey['id'] = objectId
    objKey['name'] = os.path.basename(path)
    objectId = objectId + 1
    progressBar(objectId, total)
    # Root element must have a key to be parsed in Js later
    if objKey['name'] == '':
        obj = { os.path.split(os.path.dirname(path))[-1]: {} }
        objKey = obj[os.path.split(os.path.dirname(path))[-1]]
        objKey['name'] = os.path.split(os.path.dirname(path))[-1]
    # Crawler met a directory. Recurse call on each of its elements
    if os.path.isdir(path):
        objKey['type'] = 'directory'
        children = []
        childrenDict = dict((key, obj[key]) for obj in [pathToDict(os.path.join(path, x), total) for x in os.listdir(path)] for key in obj)
        for x in childrenDict.values():
            children.append(x)
        objKey['children'] = children
    else: # Crawler met a file
        extension = path.split('.')[-1].lower()
        if extension == 'jpg' or extension == 'png' or extension == 'bmp':
            outfile = './_thumbnails/' + str(objectId) + '.jpg'
            image = Image.open(path)
            if extension == 'jpg':
                image.thumbnail((200, 200), Image.ANTIALIAS)
                image.save(outfile, 'JPEG')
            objKey['type'] = 'file'
            objKey['extension'] = extension
            objKey['path'] = os.path.abspath(path)
            objKey['size'] = os.path.getsize(path)
            objKey['width'] = image.size[0]
            objKey['height'] = image.size[1]
            objKey['exif'] = {}
            exif = image.getexif()
            for tagId in exif:
                tag = TAGS.get(tagId, tagId)
                data = exif.get(tagId)
                ignored = ['MakerNote', 'PrintImageMatching', 'XPTitle', 'XPComment', 'ExifOffset', 59932, 36873]
                if tag not in ignored:
                    if isinstance(data, (bytes, bytearray)):
                        data = data.decode()
                    #print(tag, data)
                    objKey['exif'][tag] = str(data)
    return obj


def progressBar(current, total, barLength = 30):
    percent = float(current) * 100 / total
    arrow   = '▒' * int(percent / 100 * barLength)
    spaces  = ' ' * (barLength - len(arrow))
    print(' > ▓%s%s▓ Scan progress: %d%%' % (arrow, spaces, percent), end='\r')


# Script start point
if __name__ == '__main__':
    main()
