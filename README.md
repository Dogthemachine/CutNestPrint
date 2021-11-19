![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/CNP_logo-100.png)
# Cut Nest Print
## Automatic solution for compact placement of images for printing. Made on Python, based on Django3. 
### Allows two databases .sqlite3 to fast import data from the [website](https://catcult.club/). Holds all items of clothes devides by topics (fashions).
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-17%20%D0%B2%2012.45.19.png)
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-17%20%D0%B2%2012.28.03.png)
### Each product maintains its own set of cuts- .tiff files, divided by size.
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-17%20%D0%B2%2018.10.14.png)
When the products are selected for nesting, the contours of each cut are created and saved in .svg files. Uses the OpenCV computer vision library to build outlines of cuts (see helpers.py). 
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-18%20%D0%B2%2013.19.23.png)
Then the files are passed to [Deepnest](https://github.com/Jack000/Deepnest) automatically by uploading to specific folder, where the nesting is done. The output is a .json file that contains the coordinates of the positions of each part.
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-17%20%D0%B2%2012.29.50.png)
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-17%20%D0%B2%2012.34.28.png)
By "Finish apportionment" button .tiff background is created, and each detail is laid out on it through a contour mask of itself, according to the coordinates obtained from .json
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-17%20%D0%B2%2012.38.50.png)
The finished file with the apportionment is compressed, uploaded into the Dropbox and sent to production by email using the "Send by mail" button.
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-17%20%D0%B2%2012.39.55%20copy.png)
By clicking the "Confirm order" button, the information about the order is saved in the database.
![This is an image](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-11-17%20%D0%B2%2012.42.17.png)
Using Bootstrap4 for styling.
