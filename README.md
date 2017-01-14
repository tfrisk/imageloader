# Image Loader

Load all images from given url.

## Usage

```
usage: imageloader.py [-h] -u URL [-D DIR] [-d]

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  URL to read
  -D DIR, --dir DIR  Write images to specific directory
  -d, --debug        Display debug messages
```

Python version 2.7 or later is required (works with python 3).

Option `-D DIR` is optional, the default location is `./saved-images`.

## Limitations

Images with <picture> element containers are not supported as they
are much harder to assemble together than traditional <img> elements.

Embedded base64 encoded images are not supported.

Excepts given url is reachable with status code 200. Redirected urls
are not tested and may not work.

Images are saved with their original names which could be messy.

Image directory structure is not preserved, all images are saved in one
directory flat.

Generated download log ("filelist.txt") is not sorted.

## License

Copyright (c) 2017 Teemu Frisk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
