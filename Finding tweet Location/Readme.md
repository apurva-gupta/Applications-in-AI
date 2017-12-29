This program aims at finding that where was the tweet sent based on the content of tweet.

Description of Files
1. tweets.train - It contains tweets and correspodning cities where they were sent.
2. tweets.test1 - It contains test file with correct city name labels and test tweets.
3. geolocate.py - It contains the code written in python to implement bayesian classfier for finding city names in test file and calculate accuracy on test set.

It is a classic implementation of Naive Bayes law in document classification using bag of words approach.

To Run Program:
./geolocate.py training-file testing-file output-file

Format of Training-file and Test-file : <city name> <tweet>
The program trains on training file, predicts city names for test tweets in test file and write result in output-file in format : <predicted city> <actual city> <tweet>
The dataset consists of tweets from 12 different american cities.

DATA PREPROCESSING
1. Converted whole bag of words to lower case
2. Removed punctuations and stop words

RESULTS
