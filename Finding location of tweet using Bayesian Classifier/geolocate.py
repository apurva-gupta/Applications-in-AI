#!/usr/bin/env python
#Team members: Surbhi Paithankar, Apurva Gupta, Sai Shruthi
#Program Title: Tweet Classification - Estimate where a Twitter "tweet" was sent, based only on the content of the tweet itself.
# Description : The program is a classic implementation of Naive Bayes Law in document classification where we use bag of words for predicating the location. Each word is considered to be independent to other in the tweet.
# The formalae used was : P(C|W)= min(-lnP(C)+sum(-lnP(Wi|C) for all i denoting all words)).
# P(Wi|C) incorporates Laplace Add-one smoothing i.e P(Wi|C) = (no. of times Word Wi appears in a Class C + 1) / (Vocab Size + No. of words in class C)

#The program also displays top 5 words associated with each city. It is done by fetching 5 words have top 5 P(Wi|C) values for each city.

#DESIGN DECISIONS:
# As a part of data cleansing, we convert all words to lower cases. Also we remove all the punctuations & stop words from the test & train file as they add a very little value to the calculations. 

#Citation:
#Refered : https://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html

import math
import sys
import string
import re

trainfile = sys.argv[1]
testfile = sys.argv[2]
with open(trainfile,"r") as myfile:
  data= myfile.read()
with open(testfile,"r") as mytestfile:
  testdata = mytestfile.read()
data = data.split("\n")
testdata = testdata.split("\n")
trainlist1=[]
testlist1=[]
trainlist=[]
testlist = []

#Function to remove non-alphanumeric characters from a given tweet.
def getwords(tweet):
  return [word.lower() for word  in re.split(r"[\W_]",tweet) if word!= '']


for every in data:
  trainlist1.append(every.split(" ",1))

for every in testdata:
  testlist1.append(every.split(" ",1))

testlist1 = [x for x in testlist1 if x!=[''] and x!=[]]
trainlist1 = [x for x in trainlist1 if x!=[''] and x!=[]]

for each in trainlist1: 
    if len(each)==2:
      trainlist.append(getwords(each[1]))

for each in testlist1:
    if len(each)==2:
      testlist.append(getwords(each[1]))

#List of stop words
stop_words = set(['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my','and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once'])


# Remove words from trainset that are present in stop list.
i = 0
while i<len(trainlist):
  j = 0
  for every in trainlist[i]:
    if every not in stop_words:
      trainlist[i][j] = every
      j = j + 1
  del trainlist[i][j:]
  i = i +1

# Remove words from testset that are present in stop list.
i = 0
while i<len(testlist):
  j = 0
  for every in testlist[i]:
    if every not in stop_words:
      testlist[i][j] = every
      j = j + 1
  del testlist[i][j:]
  i = i +1


#City directory Construction. Eg: City1: word1,word2,...,wordn
citydir = {}
i=0
for each in trainlist1:
  if len(each)==2:
    if each[0] not in citydir.keys():
      citydir[each[0]]= trainlist[i]
    else:
      citydir[each[0]]+=trainlist[i]
    i=i+1

#Word directory Construction. Eg: {Word1: {city1: Count1, City2: Count2,....,Cityn: Countn}}
worddir = {}
for everyline in trainlist:
  for everyword in everyline:
    worddir[everyword] = {}


for everyline in testlist:
  for everyword in everyline:
   if everyword not in worddir.keys():
    worddir[everyword] = {}

for everyword in worddir.keys():
  for everycity in citydir.keys():
    worddir[everyword][everycity]=0

for everycity in citydir.keys():
  for everyword in citydir[everycity]:
    worddir[everyword][everycity]+=1

# Directory that stores the P(C) for each city. P(C)= No. of tweets from a city/ Total number of tweets
no_of_tweet_dir={}
x = 0
i = 0
while i<len(trainlist1):
  each = trainlist1[i][0]
  if each not in no_of_tweet_dir:
    no_of_tweet_dir[each] = 1
  else:
    no_of_tweet_dir[each] += 1
  i = i+1

x = 0
i = 0
n = len(trainlist)
for each in no_of_tweet_dir.keys():
  x = no_of_tweet_dir[each]
  no_of_tweet_dir[each] = -math.log(float(float(x)/float(n)))


#Vocabulary size calculation
vocab = len(worddir)

#Conditional probability directory Construction. Eg: {Word1: {city1: Conditional prob1, City2: cond_prob2,....,Cityn: Cond_probn}}

cond_prob = {}
for everyword in worddir.keys():
  cond_prob[everyword]={}
  for everycity in citydir.keys():
      cond_prob[everyword][everycity]={}

for everyword in worddir.keys():
  for everycity in citydir.keys():
    if worddir[everyword][everycity]==0:
      prob = -math.log(float((0+1)/float((vocab+len(citydir[everycity])))))
    else:
      prob = -math.log(float((worddir[everyword][everycity]+1)/float((vocab+len(citydir[everycity])))))
    cond_prob[everyword][everycity] = prob


# Below code find the P(C|W). As we have taken negative log, we will find the city have minimum cost value for -ln(P(C))+-ln(P(W|C))
value = 00.00000
max = 999999999999999
city_list=[]

i=0
while i<len(testlist):
  value = 00.00000
  max = 999999999999
  for everycity in citydir.keys():
    value = 00.0000
    for everyword in testlist[i]:
        value = value+cond_prob[everyword][everycity]
    total_value = value + (no_of_tweet_dir[everycity])
    if total_value<max:
      max = total_value
      city = everycity
  city_list.append(city)
  i = i+1


# We write the predicted city,actualcity, tweet to the specified output file.
op_file = open(str(sys.argv[3]),"wa")
i = 0
elem3=""
while i<len(testlist):
  elem1 = city_list[i]
  elem2 = testlist1[i][0]
  elem3 = testlist[i][1:]
  L = str(elem1) + " " + str(elem2)+ " "+str(elem3)
  op_file.write(L+"\n")
  i = i+1


#Below we find the top 5 words associated with each city and display on the output console.
arr=[]
words={}
for eachcity in citydir.keys():
  arr=[]
  i=0
  words[eachcity]=[]
  while i<5:
    value1=[99999999999999999,0]
    for eachword in citydir[eachcity]:
     if eachword not in words[eachcity] and cond_prob[eachword][eachcity]<value1[0]:
         value1=[cond_prob[eachword][eachcity],eachword]
    words[eachcity].append(value1[1])
    i=i+1

for each in words.keys():
  str=""
  print "\nTop 5 words associated with ",each,":"
  for word in words[each]:
    str= str+" "+word
  print str
      
