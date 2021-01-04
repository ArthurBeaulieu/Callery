# Callery

Local website to review your photos!

Install python 3 and Pillow, then run the `build.py` script, with your library root path, then drop the created JSON in the `index.html` file to browse it!

- Use the `-t`/`--thumbs` flag in `build.py` to generate thumbnails, to fasten the browsing.
- Use the `-m`/`--minify` flag to make the JSON output file lighter.

Both `_thumbnails` folder and `MyLibrary.json` file will be created at the root of the provided path.
