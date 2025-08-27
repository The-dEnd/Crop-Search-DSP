This document covers current implementation of ML algorithm. It is intended for developers, with a technical background and a basic knowledge of ML. It does not cover the models training themselves, or the implementation coices, but instead focuses on the usage of trained models within the application.

The algorithm is split in two distinct parts:
1) YOLOv5 identification of die patterns with bounding boxes.
2) Within identified bounding boxes, Resnet18 identification of the exact die.

Should the need to change the ML model arise, two possibilities exist:
A) either improving/replacing the models, while keeping current implementation and design choice
B) or completely refactor the detection algorithm, should better algorithms arise in the future.



For case B, feel free to reimplement a new algorithm from scratch, and call it in the display.py file at the #HereInsertMLAlgo flags.
For case A, you can replace the models within the "models/" folder with newer models, and adapt the optimal picture size the algorithms were trained with, by editing the variables resize_yolo and resize_resnet.
resize_yolo defines the picture size that is requested to run the YOLO bounding boxes mapping.
For each found bounding box, resize_resnet defines the size to which the bounding box is reesized before running Resnet.

