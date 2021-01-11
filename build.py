#!/usr/bin/env python3


# Python imports
from os import mkdir, path, listdir, walk
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
    ap.add_argument('-m', '--minify', help='Minify the JSON output file', action='store_true')
    args = vars(ap.parse_args())
    # Crawl given path and build JSON
    crawlFolder(args)


def crawlFolder(args):
    print('##----------------------------------------##')
    print('##                                        ##')
    print('##    Callery build.py - version 0.0.1    ##')
    print('##                                        ##')
    print('##----------------------------------------##\n')
    print('> Retrieving folder information...')
    try:
        mkdir(path.join(args['folder'], '_thumbnails'))
    except:
        pass
    files = folders = 0
    for dirname, dirnames, filenames in walk(args['folder']):
        if dirname.find('_thumbnails') == -1: # Exclude thumbnails from count
            files += len(filenames)
            folders += len(dirnames)
    if files == 0 and folders == 0: # Not performing scan on empty folder
        print('ERROR: No files or folder to analyze. Exiting script...')
        sys.exit(-1)
    else: # Recursive method to build any sub-elements in provided path, and generate thumbnails if asked to
        print('> Creating JSON dump. This may take a while...\n')
        filename = path.join(args['folder'], 'LibraryData.json')
        with open(filename, 'w', encoding='utf-8') as file:
            if args['minify']:
                json.dump(pathToDict(args, args['folder'], files + folders), file, ensure_ascii=False, separators=(',', ':'))
            else:
                json.dump(pathToDict(args, args['folder'], files + folders), file, ensure_ascii=False, indent=2)
        print('\n\n> Output file generated!')


objectId = 0 # UID for any element in JSON output (folder ands files)
def pathToDict(args, folder, total):
    if path.basename(folder) != '_thumbnails': # We ignore thumbnails
        global objectId
        obj = { path.basename(folder): {} }
        objKey = obj[path.basename(folder)]
        objKey['id'] = objectId
        objKey['name'] = path.basename(folder)
        # Root element must have a key to be parsed in Js later
        if objKey['name'] == '':
            obj = { path.split(path.dirname(folder))[-1]: {} }
            objKey = obj[path.split(path.dirname(folder))[-1]]
            objKey['id'] = objectId
            objKey['name'] = path.split(path.dirname(folder))[-1]
            objKey['path'] = path.abspath(folder) # Add folder base path
        # Crawler met a directory. Recurse call on each of its elements
        if path.isdir(folder):
            objectId = objectId + 1
            progressBar(objectId, total)
            objKey['type'] = 'directory'
            objKey['path'] = path.abspath(folder) # Add folder base path
            children = []
            childrenDict = dict((key, obj[key]) for obj in [pathToDict(args, path.join(folder, x), total) for x in listdir(folder)] for key in obj)
            for x in childrenDict.values():
                children.append(x)
            objKey['children'] = children
            return obj
        else: # Crawler met a file
            extension = folder.split('.')[-1].lower() # lowercase extension to have consistent testing
            if extension == 'jpg' or extension == 'png' or extension == 'bmp':
                image = Image.open(folder)
                if args['thumbs'] == True: # Generating 256/256 thumb JPG, keeping aspect ratio
                    outfile = path.join(args['folder'], '_thumbnails', str(objectId) + '.jpg')
                    image.thumbnail((256, 256), Image.ANTIALIAS)
                    # Convert savage RGBA in RGB
                    if image.mode in ('RGBA', 'P'):
                        image = image.convert('RGB')
                    image.save(outfile, 'JPEG')
                objKey['type'] = 'image'
                objKey['extension'] = extension
                objKey['size'] = path.getsize(folder)
                objKey['path'] = path.abspath(folder)
                objKey['width'] = image.size[0]
                objKey['height'] = image.size[1]
                objKey['exif'] = {}
                # Browse image exifs
                exif = image.getexif()
                for tagId in exif:
                    tag = TAGS.get(tagId, tagId)
                    data = exif.get(tagId)
                    #ignored = ['MakerNote', 'PrintImageMatching', 'XPTitle', 'XPComment', 'ExifOffset', 59932, 36873]
                    saved = ['FocalLength', 'ExposureTime', 'FNumber', 'ISOSpeedRatings', 'Make', 'Model', 'LensModel', 'DateTimeOriginal']
                    #if tag not in ignored:
                    if tag in saved:
                        # Decode exif is encoded in bytes
                        if isinstance(data, (bytes, bytearray)):
                            data = data.decode()
                        if type(data) is tuple: # Convert tuple that are fractions (focal, time etc)
                            if data[1] == 0: # Plz no division by zero..
                                data = data[0]
                            else:
                                data = data[0] / data[1]
                        # Save tag into output dict
                        objKey['exif'][tag] = str(data)
                objectId = objectId + 1
                progressBar(objectId, total)
                return obj
            elif extension == 'mp4' or extension == 'avi' or extension == 'mov':
                objKey['type'] = 'video'
                objKey['extension'] = extension
                objKey['size'] = path.getsize(folder)
                objKey['path'] = path.abspath(folder)
                objectId = objectId + 1
                progressBar(objectId, total)
                return obj
            else:
                objectId = objectId + 1
                progressBar(objectId, total)
                return {}
    return {}

def progressBar(current, total, barLength = 30):
    percent = float(current) * 100 / total
    arrow   = '▒' * int(percent / 100 * barLength)
    spaces  = ' ' * (barLength - len(arrow))
    print('  ▓%s%s▓ Scan progress: %d%%' % (arrow, spaces, percent), end='\r')


# Script start point
if __name__ == '__main__':
    main()
