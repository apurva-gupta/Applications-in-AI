Optical Character Recognition

This program aims at recognizing characters in a given image using the concept of HMM.

We have implemented this using three techniques viz.
a. Simple Naive Bayes Algorithm
b. Variable Elimination (Forward-Backward algorithm)
c. Viterbi Algorithm

To Run Program:
./ocr.py train-image-file.png train-text.txt test-image-file.png

It predicts the text in image file:test-image-file.png using all three techniques.

Description of files:
1. ocr.py :- It contains code written in python
2. courier-train.png :- It is traning file which contains all the alphabets,numbers and special symbols.
3. test-0-0.png to test-19-0.png :- These are all the test images
4. tweets.train :- this training file is used to calculate transition probabilities
5. test-strings :- It contains all the text of images test-0-0.png to test-19-0.png
