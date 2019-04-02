# CoverCarousel
A script to display book covers on large TVs (jumbotrons) using Alma and ContentCafe.

![Alt Text](https://github.com/MrJeremyHobbs/CoverCarousel/blob/master/images/CoverCarousel-Logo.gif)

## How it Works
Create a physical items set in Alma of any criterea (New books, books on a certain subject, etc.). This can be either an itemized (static) list or a Logical (dynamic) list that updates in real time.

CoverCarousel reads the set and grabs the ISBN for each item and searches ContentCafe for a HQ image to display.

CoverCarousel downloads cover to local machine and an ongoing slideshow player loads the images.

Use Windows Task Scheduler to set the loader script to run once a day in the early morning, right before opening.

## Installation
CoverCarousel is Windows-only (as of now).

### Slideshow Viewer
CC makes use of FSViewer, an image slideshow app. Download the portable version here: https://www.faststone.org/FSIVDownload.htm

Place within the FSViewer64 folder.

If you download a newer version, change folder names and relative paths accordingly in the carousel_loader.ahk file.

### Loader Script
To run the loader script, you will need to download AutoHotKey here: https://www.autohotkey.com/

