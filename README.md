# pyqt-splitted-graphicsview
QGraphicsView which shows clipped left image and clipped right image at the same place based on movable vertical line.

This widget is suitable for displaying images before and after processing.

The QGraphicsScene in this view is resized based on the size of the image that was added, according to the specific purpose of this script.

## Requirements
* PyQt5 >= 5.14

## Class & Method Overview
* SplittedImageView - class in the imageView.py
  * setFilenameToLeft(filename) - set the image file on the left
  * setFilenameToRight(filename) - set the image file on the right
  * removeItemOnTheLeft() - remove the image on the left if it exists
  * removeItemOnTheRight() - remove the image on the right if it exists
 
## Example Code
Refer to the main.py to understand how to use it.

## How to Use
![image](https://github.com/yjg30737/pyqt-splitted-graphicsview/assets/55078043/42363867-02a0-4a46-a8a1-f4ef8343727c)

Set the image files for each part (left and right) and observe what happens when you move the vertical line left and right.

https://github.com/yjg30737/pyqt-splitted-graphicsview/assets/55078043/0da48979-85e3-4e68-95e4-57395ee7393a

Left part is a (1).png, right part is a (2).png. These files are in the repo, so you can use them to test this script, right away.
