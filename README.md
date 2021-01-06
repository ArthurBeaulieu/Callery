# Callery

![](https://badgen.net/badge/version/0.0.1/blue)
[![License](https://img.shields.io/github/license/ArthurBeaulieu/Callery.svg)](https://github.com/ArthurBeaulieu/Callery/blob/master/LICENSE.md)

Local website to review your photos!

Use the python script to generate a `JSON` which will contain all the required information to properly browse your photo library, then drop it in the provided `index.html` file to enjoy your pictures!

# Get started

Install `python` (version 3) and `Pillow`, then run the `build.py -t` script, with your library root path, then drop the created `JSON` in the `index.html` file to browse it!

- Use the `-t`/`--thumbs` flag in `build.py` to generate thumbnails, to fasten the browsing.
- Use the `-m`/`--minify` flag to make the `JSON` output file lighter.

Both `_thumbnails` folder and `MyLibrary.json` file will be created at the root of the provided path.

# Screenshots

Sorry, this website only works on a local machine for security reasons (otherwise the web might be broken), so you will need to clone this repository to test it against your photo library! Here are some screenshots to still have a look on it ;)

<p>
  <img src="/screenshots/browser.png" width="960" alt="callery-browser"/>
  <br><br>
  <img src="/screenshots/viewer.png" width="960" alt="callery-viewer"/>
</p>
