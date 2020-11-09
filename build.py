#!/usr/bin/env python3


# Python imports
import os
import sys
import argparse
import json


from PIL import Image
from PIL import ImageFile
from PIL.ExifTags import TAGS
# Edit PIL configuration
Image.MAX_IMAGE_PIXELS = None # Display no warning for big files (panoramas of several pictures may raise it)
ImageFile.LOAD_TRUNCATED_IMAGES = True # Enforce thumbnail creation


# Script main frame
def main():
    # Init argparse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('folder', help='The input folder path to crawl (absolute or relative), mind to run with -t if new files are in scanned folder')
    ap.add_argument('-t', '--thumbs', help='Generate 200px thumbails. Required if any new pictures are in folder', action='store_true')
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
    if files == 0 and folders == 0:
        print('ERROR: No files or folder to analyze. Exiting script...')
        sys.exit(-1)
    else:
        with open('MyPictures.json', 'w', encoding='utf-8') as file:
            json.dump(pathToDict(args, args['folder'], files + folders), file, ensure_ascii=False, indent=2)


objectId = 0
def pathToDict(args, path, total):
    if os.path.basename(path) != '_thumbnails':
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
            objKey['path'] = os.path.abspath(path) # Add folder base path
        # Crawler met a directory. Recurse call on each of its elements
        if os.path.isdir(path):
            objKey['type'] = 'directory'
            children = []
            childrenDict = dict((key, obj[key]) for obj in [pathToDict(args, os.path.join(path, x), total) for x in os.listdir(path)] for key in obj)
            for x in childrenDict.values():
                children.append(x)
            objKey['children'] = children
        else: # Crawler met a file
            extension = path.split('.')[-1].lower()
            if extension == 'jpg' or extension == 'png' or extension == 'bmp':
                image = Image.open(path)
                if args['thumbs'] == True:
                    outfile = './_thumbnails/' + str(objectId) + '.jpg'
                    image.thumbnail((256, 256), Image.ANTIALIAS)
                    # Convert savage RGBA in jpg (jpg renamed with no respect)
                    if image.mode in ('RGBA', 'P'):
                        image = image.convert('RGB')
                    image.save(outfile, 'JPEG')
                objKey['type'] = 'file'
                objKey['extension'] = extension
                objKey['size'] = os.path.getsize(path)
                objKey['path'] = os.path.abspath(path)
                objKey['width'] = image.size[0]
                objKey['height'] = image.size[1]
                objKey['exif'] = {}
                # Browse exifs
                exif = image.getexif()
                for tagId in exif:
                    tag = TAGS.get(tagId, tagId)
                    data = exif.get(tagId)
                    ignored = ['MakerNote', 'PrintImageMatching', 'XPTitle', 'XPComment', 'ExifOffset', 59932, 36873]
                    if tag not in ignored:
                        # Decode exif is encoded in bytes
                        if isinstance(data, (bytes, bytearray)):
                            data = data.decode()
                        # Save tag into output dict
                        objKey['exif'][tag] = str(data)
        return obj
    else:
        return {}


def progressBar(current, total, barLength = 30):
    percent = float(current) * 100 / total
    arrow   = '▒' * int(percent / 100 * barLength)
    spaces  = ' ' * (barLength - len(arrow))
    print(' > ▓%s%s▓ Scan progress: %d%%' % (arrow, spaces, percent), end='\r')


# Script start point
if __name__ == '__main__':
    main()
