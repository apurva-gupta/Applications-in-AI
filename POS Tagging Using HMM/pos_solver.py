###################################
# CS B551 Fall 2017, Assignment #3
#
# Apurva Gupta(guptaapu), Surbhi Paithankar (spaithan),  Hasika Mahatta(hmahtta)
#
# (Based on skeleton code by D. Crandall)
#
#
####
"""
Title: To find POS tags of every word of a given sentence using hidden Markov model.

We have implemented this using three techniques viz.
a. Simple Naive Bayes Algorithm
b. Variable Elimination (Forward-Backward algorithm)
c. Viterbi Algorithm.

a. Simple Naive Bayes Algorithm

Formula used:
ARGMAX P(POSTAG|WORD Wi) = P(WORD Wi|POSTAG) * P(POSTAG)
where P(POSTAG) is the prior probability for any pos tag
and P(WORD WI|POSTAG) is the emission probability for a word given POSTAG.

For this implemention we use simple bayes net, where every word is independent of other word.

b. Variable Elimination

In Variable elimination we take all other states into account and eliminate them by performing summation over all possible values.
Lets say We need to find P(POSTAG PTi| WORD Wi)
Step 1:
Compute tow_table(alpha) using forward algorithm from first word upto the desired word. i.e PT1...PTi
Step 2:
Compute tow_table(Beta) using backward algorithm from last letter upto the desired letter. i.e PTn....PTi
Step 3:
Finally we multiply alpha(PT1...i)*emission(PTi|Word Wi) * beta(PTi....n)

c. Viterbi Algorithm
Formula used:
Step 1:
In this we created a viterbi matrix (I*J) where i = number of words in sentence and j = number of POS tags.
vit(i,j) stores viterbi values and a backpointer to the previous state.
Formula :
vit(W0,j) = P(Word W0|POSTAG) * P(POSTAG)
vit(Wi,j) = max(vit(Wi-1,j) * P(POSTAG|Prev POSTAG)) * P(Word Wi|POSTAG)

Step 2:
After creating the viterbi matrix, we begin with the last letter and traverse along the path till the first letter using the backpointer maintained.


PROBABILITY CALCULATIONS:

1. Initial Probability: 
P(postag PT) = Number of occurences of the postag PT in training file/ total Number of postags
   Note : If No. of occurences of POSTAG PT is zero then P(Letter L1) = 10e-14

2. Transition Probability:
P(POSTAG P2|POSTAG P1) : No. of occurences where P2 succeeds P1 in training file/ No. of occurences of P1  
   Note : If No. of occurences of POSTAG P1 is zero then P(L2|L1) = 10e-14

3. Emission Probability:
P(Word Wi| POSTAG Pi) : No. of occurences where Word Wi has POSTAG Pi in training set/ No. of occurences of POSTAG Pi.

 
POSTERIOR PROBABILITY:
    # Calculate the log of the posterior probability of a given sentence with a given part-of-speech labeling
    #The posterior probability is the probability where we need to calculate the probability for each word in the sentence given the corresponding tag for t
hat sentence.
    #That is posterior probability = P(S1......Sn|W1.......Wn).
    #Applying naive bayes and bayes law, we will get this probability equal to P(W1|S1)........P(Wn|Sn)*P(S1)P(S2/S2).......P(Sn|Sn-1)/P(W1...Wn)
    #(ignoring denominator)
    #For example -
    #Sentence- The house is big
    #label-    Det noun  pron adj
    #In the above bayes net, we can calculate the posterior probability as follows:
    #P(The/Det)*P(Det)*P(house/noun)*P(noun)*P(noun/Det)*P(is/pron)*P(pron)*P(pron/noun)*P(big/adj)*P(adj)*P(adj/pron)



OBSERVATION:
1. Viterbi & Variable elimination performs much better than simple.
2. Viterbi & VE give almost equal results.
3. We observed that for some really long sentences(like 519th sentence in bc.test set) the issue of underflow takes place.This leads into wrong predication.In order to handle this, we have performed scaling up by multiplying 10e5 while computing the tow table. This inturn increased the word accuracy from 94.48% to 95.32% in HMM VE.  

RESULTS:
Scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct:
   0. Ground truth:      100.00%              100.00%
     1. Simplified:       93.92%               47.45%
         2. HMM VE:       95.32%               56.05%
        3. HMM MAP:       95.31%               55.30%


"""

####

import random
import math
from decimal import *

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

#Posterior probability calculation
    def posterior(self, sentence, label):
        total = 0.00
        
        for i in range(0,len(label)):
            if i!=len(label)-1:
                try:
                    total_prob = math.log(self.tagprob[label[i]]) + math.log(self.worddir[sentence[i]][label[i]]) +math.log(self.transition[label[i+1]][label[i]])
                except:
                    total_prob = math.log(self.tagprob[label[i]]) + math.log(0.000000000000001) + math.log(self.transition[label[i+1]][label[i]])
                total= total + total_prob
            
        return total

    # Do the training!
    #Here, we are training the data by calculating the following and have stored them in the dictionaries.
    #Note: '<S>' and '<ST>' indicates the start and end of the sentence respectively which is required while calculating the transition probabilities.
    #tagprob('tag'): This dictionary stores the probability of the each tag in the training data.
    #tagcount: This dictionary stores the count of each tag as per the  training data.
    #transition[next_tag][everytag]: This dictionary stores the transitiona probabilities of each tag occurance after each tag.
    #totaltags: This counts total numnber of tags in the training data in all.

    #First we initialize the dictionary for storing the probabilities as mentioned above.
    def train(self, data):
        self.count = 0
        self.previous_tag = "<S>"
        self.transition = {}
        self.tagcount = {}
        self.tagprob = {}
        self.totaltags = 0
        self.all_tags = ['adv', 'noun', 'adp', 'pron', '<S>', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj','<ST>']
        for everytag in self.all_tags:
            self.transition[everytag]={}
            self.tagcount[everytag] = 0
            for next_tag in self.all_tags:
                self.transition[everytag][next_tag] = {}
                self.transition[everytag][next_tag] = 0

        #Counts the total number of tags in the data and the count of each tag in it.
        for i in range(0,len(data)):
            for eachtag in data[i][1]:
                if eachtag!='<S>' and eachtag!='<ST>':
                    self.tagcount[eachtag]+=1
                    self.totaltags +=1
        self.tagcount['<S>'] = len(data)
        
        #tagprob that is the probability of each tag in the data can be calculated as follows:
        #Probability(eachtag)= total number of occurences of each tag/ total number of tags 
        for eachtag in self.tagcount.keys():
            self.tagprob[eachtag]=float(self.tagcount[eachtag])/float(self.totaltags)
       
        #Calculation of transition probabilities.
        #In this we are counting occurence of each tag after each tag and storing them in the dictionary.
        #For example - probability of noun occuring after of the 12 tags: P(noun/verb),P(noun/det),P(noun/det),P(noun/pron)......
        for i in range(0,len(data)):
            self.transition[data[i][1][0]]['<S>'] +=1
            for j in range(0,len(data[i][1])):
                if j+1 < len(data[i][1]):
                    self.transition[data[i][1][j+1]][data[i][1][j]] +=1
                else:
                    self.transition['<ST>'][data[i][1][j]] +=1

        for every in self.transition.keys():
            for prev in self.transition[every]:
                if self.tagcount[prev]!=0:
                    self.transition[every][prev]/=float(self.tagcount[prev])
        
        for every in self.transition.keys():
            for prev in self.transition[every]:
                if self.transition[every][prev]==0:
                    self.transition[every][prev]=0.00000000000000001


        #Calculation of Emmission probability
        #Emmission probability is the probability of each word given each of the tags.
        #This can be calculated by counting the number of occurances of each word as a particular tag in the training data.
        #this implies that we count the number of occurances of a word say 'the' as 'noun' , 'the' as 'verb' , 'the' as each of the tags
        #and store them in the emmission dictionary self.worddir[eachword][everytag]. 
        #This dictionary will give the emmision probability directly for  any word when required . For example - 
        #self.worddir[the][det],self.worddir[the][noun],self.worddir[the][det],....... and for all the words and each of the tags.

        self.worddir={}
        l=i=j=k = 0               
        while i <len(data):
            l=j =0
            while l<len(data[i][0]):
                w = data[i][0][j]
                self.worddir[w]={}
                j = j+1
                l = l+1
            i = i+1
        for eachword in self.worddir.keys():
            for everytag in self.all_tags:
                self.worddir[eachword][everytag] = 0 

        l=i=j=k = 0
        while i<len(data):
            l=j=k = 0
            while l<len(data[i][0]):
                word = data[i][0][j]
                tag = data[i][1][k]
                count = self.worddir[word][tag]
                self.worddir[word][tag] =  count + 1
                l = l + 1
                j = j + 1
                k = k + 1
            i = i + 1

        for eachword in self.worddir.keys():
            for eachtag in self.worddir[eachword]:
                if self.tagcount[eachtag]!=0:
                    self.worddir[eachword][eachtag]/=float(self.tagcount[eachtag])

        for eachword in self.worddir.keys():
            for eachtag in self.worddir[eachword]:
                if self.worddir[eachword][eachtag]==0:
                    self.worddir[eachword][eachtag] = 0.00000000000000001

    # Functions for each algorithm.
    #Prediction of tags for each of the words using simplifies bayes Net method
    #Calculation of probability using simplified Bayes net as shown in Figure1(b) in the question.
    #This can be calculate by applying bayes net .
    #P(S1...Sn/W)=emmission probability(word/S1....Sn)* Probability[eachtag]
    #that is P(S1....Sn/word)=P(Word/S1......Sn)*P(S1........Sn)
    #P(Word/S1....Sn) can be retrieved from the emmission probability dictionary.
    #P(S1..........Sn) can be retrieved from the tagprob dictionary.
    #We will choose the maximum count value of each of the tags that occur for a particular word and return that particular tag for that particular word
    def simplified(self, sentence):
        tags = []
        
        for eachword in sentence:
                max = 0.000000000000000000000000000000000000000
                for eachtag in self.all_tags:
                    try:
                        value = self.worddir[eachword][eachtag] * self.tagprob[eachtag]
                         
                        if value>max:
                            max = value
                            final_tag = eachtag
                    except:
                        value = 0.00000000000000001 * self.tagprob[eachtag]
                        
                        if value> max:
                             max = value
                             final_tag = eachtag
                tags.append(final_tag)       
        return  tags


    #Prediction of sequence of tags using Variable Elimiation algorithm.
    def hmm_ve(self, sentence):

        tag_list = ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']
        tou_table={}
        final_tag = "noun"

        min = 99999999
        tags = []

        #Code block to find pos tag using simple naive bayes if the sentence has length =1
        if len(sentence)==1:
            max = 0.0000000000000
            for eachtag in tag_list:
                value = self.worddir[sentence[0]][eachtag] * self.tagprob[eachtag] * self.transition[eachtag]["<S>"]
                if value>max:
                    max = value
                    final_tag = eachtag
            return [ final_tag ] 

        # We find the pos tag for the first word here
        max = 0.000000000
        tou_table["s1"] ={}
        for eachtag in tag_list:
            try:
                tou_s1 = (self.tagprob[eachtag]) * ( self.worddir[sentence[0]][eachtag]) * 10e5
                tou_log = (tou_s1)
                if tou_log>max:
                    max = tou_log
                    final_tag = eachtag
                tou_table["s1"][eachtag] = tou_s1
            except:
                tou_s1 = (self.tagprob[eachtag]) * ( 0.00000000000000001) * 10e5
                tou_log = (tou_s1)
                if tou_log>max:
                    max = tou_log
                    final_tag = eachtag
                tou_table["s1"][eachtag] = tou_s1
        tags.append(final_tag)
        
        #Below code block finds the pos tag for any word(apart from first & last) in given sentence.
        #We compute tow_table_forwards, emission probability for word i and tow_table_backward
        #Finally we find the argmax of product for the above three terms.
        for k in range(2,len(sentence)): 
            i = 2
            for x in range(1,len(sentence)):
                if i!=k:
                    variable = "s"+str(i)
                    tou_table[variable] = {}
                else:
                    variable = "s"+str(i)+str("a")
                    variable1 = "s"+str(i)+str("b")
                    tou_table[variable] = {}
                    tou_table[variable1] = {}
                i = i +1

            i = 1
            p = k
            q = k
            r = k
            wordcount = 1
            while q-1!=0:
                variable  = "s" + str(i)
                if i==p-1:
                    variable1 = "s"+str(i+1)+"a" 
                    
                else:
                    variable1 = "s" + str(i+1)
                i = i +1
                for eachtag in tag_list:
                    
                    total = 0.0000000000

                    for everytag in tag_list:
                        temp =  (self.transition[eachtag][everytag]) * (tou_table[variable][everytag]) *10e5
                        total = total + temp
                    tou_table[variable1][eachtag] = total

                    #We multiply emission probability to the tow table only when we have reached to the position of the word whose POS is to be found.
                    if q-1!=1:
                        try:
                            temp1 =  (self.worddir[sentence[wordcount]][eachtag]) * (tou_table[variable1][eachtag])
                            tou_table[variable1][eachtag] = temp1
                        except:
                            temp1 = (0.00000000000000001)  * ( tou_table[variable1][eachtag])
                            tou_table[variable1][eachtag] = temp1
                wordcount = wordcount + 1    
                q = q -1
 
            #backward algo that runs from the last word upto the word whose POSTAG is to be found.
            wordcount = len(sentence) 
            if k==wordcount-1:
                variable = "s" + str(len(sentence)-1) + "b"
            else:
                variable = "s" + str(len(sentence)-1)
            for eachtag in tag_list:
                total = 0.000000000000
                for everytag in tag_list:
                    try:
                        temp =  (self.transition[everytag][eachtag]) * ( self.worddir[sentence[wordcount-1]][everytag]) * 10e5
                        total = total  + temp
                    except:
                        temp =  (self.transition[everytag][eachtag])* (0.00000000000000001)*10e5
                        total = total  + temp
                        
                tou_table[variable][eachtag] = total
            
            wordcount = wordcount -1 
            
            i = wordcount 
            p = k 
            while wordcount-p!=0:
                variable = "s"+str(i)
                if i-1==p:
                    variable1 = "s"+str(i-1)+"b"
                else:
                    variable1 = "s"+str(i-1)
            
                i = i -1
                for eachtag in tag_list:
                    total = 0.00000000000000
                    for everytag in tag_list:
                        try:
                            temp =  (self.transition[everytag][eachtag]) * (self.worddir[sentence[wordcount-1]][everytag])  * (tou_table[variable][everytag]) * 10e5
                            total = total + temp
                        except:
                            temp =  (self.transition[everytag][eachtag]) * (0.00000000000000001)  * (tou_table[variable][everytag]) * 10e5
                            total = total + temp
                    tou_table[variable1][eachtag] = total
                wordcount = wordcount-1
            
            max = 0.0000000
            variable = "s"+ str(k)+"a"
            variable1= "s" + str(k)+"b"
            

            max = 0.00000000000000000
            #Here we multiply Tow_forward * emission prob * Tow_backward
            for eachtag in tag_list:
                try:
                    total = (tou_table[variable][eachtag]) * ( tou_table[variable1][eachtag]) * ( self.worddir[sentence[k-1]][eachtag])
                    
                    total_log = total
                    if total_log>max:
                        max = total_log
                        final_tag = eachtag
                except:
 
                    total = (tou_table[variable][eachtag]) * ( tou_table[variable1][eachtag]) * (  0.00000000000000001)
                    total_log = total
#                    print total,eachtag
                    if total_log>max:
                        max = total_log
                        final_tag = eachtag
            
            tags.append(final_tag)
        
        #Calculates probability to find POS for last word in a sentence
        max = -999999999.0
        tou_table1= {}
        i = 0
        for each in sentence:
            variable = "s"+str(i+1)
            tou_table1[variable] = {}
            i = i + 1
        for eachtag in tag_list:
            try:
                tou_s1 = self.tagprob[eachtag] * self.worddir[sentence[0]][eachtag]
                tou_table1["s1"][eachtag] = tou_s1
            except:
                tou_s1 = self.tagprob[eachtag] *  0.00000000000000001
                tou_table1["s1"][eachtag] = tou_s1
        
        i = 1
        temp = 0.00000000000

        max = 0.00000000000
        
        wordcount = 1
        max = 0.000000000000
        while wordcount<len(sentence):
            variable1 = "s"+str(wordcount)
            variable2 = "s"+str(wordcount+1)
            max = 0.00000000000000
            for eachtag in tag_list:
                total = 0.00000000000
                for everytag in tag_list:
                    temp = self.transition[eachtag][everytag] * tou_table1[variable1][everytag]
                    total = total + temp
                try:
                    total1 = total * self.worddir[sentence[wordcount]][eachtag]
                    log_total = (total1)
                except:
                    total1 = total * 0.00000000000000001
                    log_total = (total1)
                if log_total>max:
                    max = log_total
                    final_tag = eachtag
                
                tou_table1[variable2][eachtag] = log_total
    
            wordcount = wordcount+1
        tags.append(final_tag)

        return tags

#Viterbi Implpementation
    def hmm_viterbi(self, sentence):
        #Construct viterbi matrix
        vit = [[0 for x in range(0,len(self.all_tags))] for y in range(0,len(sentence))]
        maxarr = []
        self.first_word = sentence[0]
        #Find viterbi value for first word
        for i in range(0,len(self.all_tags)):
            try:
                vit[0][i]=[float(self.worddir[self.first_word][self.all_tags[i]]) * float(self.transition[self.all_tags[i]]['<S>']),0]
            except:
                vit[0][i]=[0.000000000001*float(self.transition[self.all_tags[i]]['<S>']),0]
            
        #Filling up of viterbi matrix for all other words
        for j in range(1,len(sentence)):
            for k in range(0,len(self.all_tags)):
                try:
                    emission = self.worddir[sentence[j]][self.all_tags[k]]
                except:
                    emission = 0.00001 * self.tagprob[self.all_tags[k]]
                    
                maxval,maxtag = -999999,""
                for l in range(0,len(self.all_tags)):
                    val = float(vit[j-1][l][0])*self.transition[self.all_tags[k]][self.all_tags[l]]
                    if val>maxval:
                        maxval = val
                        maxtag = self.all_tags[l]
                vit[j][k]= [emission*maxval,maxtag]

        #Backtracking to find the correct sequence
        tagarr =[]
        for i in range(len(sentence)-1,0,-1):
            val = -99999999
            tag = ""
            for j in range(0,len(self.all_tags)):
                if vit[i][j][0]>val:
                    val = vit[i][j][0]
                    tag = vit[i][j][1]
                    value = j
            if i == len(sentence)-1:
                tagarr.append(self.all_tags[value])
            tagarr.append(tag)
            
        #Below case handles special case when length of sentence is 1.
        if len(sentence)==1:
            val = -999999
            for i in range(0,len(self.all_tags)):
                if vit[0][i][0]>val:
                    val = vit[0][i][0]
                    maxtag = self.all_tags[i]
            tagarr.append(maxtag)
    
        tagarr.reverse()
        return tagarr
            


    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM VE":
            return self.hmm_ve(sentence)
        elif algo == "HMM MAP":
            return self.hmm_viterbi(sentence)
        else:
            print "Unknown algo!"


