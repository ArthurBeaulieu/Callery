# Callery

![](https://badgen.net/badge/version/0.1.0/blue)
[![License](https://img.shields.io/github/license/ArthurBeaulieu/Callery.svg)](https://github.com/ArthurBeaulieu/Callery/blob/master/LICENSE.md)
![Dep](https://badgen.net/badge/dependancies/none/green)

Local website to review your photos! Download the `index.html` file and put it anywhere you want.

Use the python script to generate a `JSON` which will contain all the required information to properly browse your photo library, then drop it in the provided `index.html` file to enjoy your pictures!

Both Js and CSS are embeded in HTML file so you can put this HTML file anywhere you want.

# Get started

Install the dependencies : `pip3 install --user -r requirements.txt`.
Then run the `build.py -t <path>` script, with your library root path, then drop the created `JSON` in the `index.html` file to browse it!

- Use the `-t`/`--thumbs` flag in `build.py` to generate thumbnails, to fasten the browsing.
- Use the `-m`/`--minify` flag to make the `JSON` output file lighter.
- Use the `-o <path>`/`--output <path>` argument to specify an output path for both JSON and thumbnails if required.

Both `_thumbnails` folder and `_CalleryData.json` file will be created at the root of the provided path (or into the given output path).

# Screenshots

Sorry, this website only works on a local machine for security reasons (otherwise the web might be broken), so you will need to clone this repository to test it against your photo library! Here are some screenshots to still have a look on it ;)

<p>
  <img src="/screenshots/browser.png" width="960" alt="callery-browser"/>
  <br><br>
  <img src="/screenshots/viewer.png" width="960" alt="callery-viewer"/>
</p>
