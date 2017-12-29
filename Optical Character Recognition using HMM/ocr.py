#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png 
# Training file used during assignment: Tweets.train.txt

# Authors: Apurva Gupta, Surbhi Paithankar, Hasika Mahtta
# (based on skeleton code by D. Crandall, Oct 2017)
#
"""
This program aims at recognizing characters in a given image using the concept of HMM.
We have implemented this using three techniques viz.
a. Simple Naive Bayes Algorithm
b. Variable Elimination (Forward-Backward algorithm)
c. Viterbi Algorithm.

Probabilities:
We calculated following probabilities required for implementation.
1. Initial Probability: 
P(Letter L1 ) = Number of occurences of Letter L1 in training file/ total Number of letters
   Note : If No. of occurences of Letter L1 is zero then P(Letter L1) = 10e-14

2. Transition Probability:
P(L2|L1) : No. of occurences where L2 succeeds L1 in training file/ No. of occurences of L1  
   Note : If No. of occurences of Letter L1 is zero then P(L2|L1) = 10e-14

3. Emission Probability:
We consider every pixel to be an observation O1...n.
So as per Naive bayes:
P(O1...n|Letter) = P(O1|Letter)P(O2|Letter)....P(On|Letter)

In order to calculate P(Oi|Li) we used:
If,a given pixel matches at a particular position:
P(Oi|Li) = 1+1/((14*25)+ no. of black pixels in training letter Li)
else:
P(Oi|Li) = 0+1/((14*25)+ no. black pixels in training letter Li)

Note: Since we are doing calculations at pixel level, the joint probabilities lead to underflow. Therefore we would be using logs for the implementation of simple & viterbi algorithm.
However in variable elimination, since we need to perform summation to eliminate a variable, we cannot use logs. This is because summation of terms in logs implies multiplication and not addition.

Hence we multiply a scaling factor in the emission probability to handle the underflow.
SCALING FACTOR USED:
We used a scaling factor of log(10e308)+log(10e308)+log(10e272). We arrived at this value using the method of trial and error.

METHOD 1:
Simple Naive:

In this we consider every observation to be independent of other. In short, we did not take transition probabilities into account.
Formulae with log:
Argmin P(Letter Li|Observed 14*25 pixels) = -log(P(Observed 14*25 pixels|Letter Li)) + -log( P(Letter Li))

METHOD 2:
Variable Elimination:
In Variable elimination we take all other states into account and eliminate them by performing summation over all possible values.
Lets say We need to find P(Letter Li| Pixel observation O1....n) where n is number of letters in the image
Step 1:
Compute tow_table(alpha) using forward algorithm from first letter upto the desired letter. i.e L1...Li

Step 2:
Compute tow_table(Beta) using backward algorithm from last letter upto the desired letter. i.e Ln....Li

Step 3:
Finally we multiply alpha(L1...Li)*emission(Joint observation O1...n|Letter Li) * beta(Li....n)

METHOD 3:
Viterbi Algorithm:

Step 1:
In this we created a viterbi matrix (I*J) where i = number of letters in test set and j = number of training letters 
vit(i,j) stores viterbi values and a backpointer to the previous state.
Formula :
vit(0,j) = P(Observed 14*25 pixels|Letter Li) * P(Letter Li)
vit(Li,j) = max(vit(Li-1,j) * P(Li|Li-1)) * P(Observed 14*25 pixels|Letter Li)

Step 2:
After creating the viterbi matrix, we begin with the last letter and traverse along the path till the first letter using the backpointer maintained.


ASSUMPTION:
1. Every letter has same font with size 14*25.

OBSERVATION:

1. Simple gives a good performance in guessing any word.
2. We observe that VE and Viterbi performs sometimes better than simple.
3. VE and Viterbi performs very well when the provided training file is very exhaustive enough. For example: When we used bc.train we saw it performing not very well,infact simple looked to perform much better. However if the training file is replaced with tweets.train.txt, we saw a significant improvement in results.
This may be because of the training file better information for building the transition proabability table.

LIMITATION
1. Due to underflow issue, we add some value to scale the emission probabilities, But sometimes it also cause overflow,when very big numbers get multiplied. We observed that after multiplication,values in tou table came out to be +infinity in some cases. Thus, overflow and underflow cause some issue in this regard.Out of 20 test images provided,one of them doesnt work properly because of overflow.
We tried to calculate emssion probability in some other way,to avoid this problem,But we observed that this way of calculating emission probability gives the best result. 

"""


from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
train_text_file = str(sys.argv[2])

#Reads the input training file and splits it at character level.
def read_data(fname):
    data1 = []
    data = []
    file = open(fname, 'r');
    for line in file:
        data += line.split("\n")
    for every in data:
            for each in every:
                data1.append(each)
    return data1

#Function to store any given image in list of list pixel format.
def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '1' if px[x, y] < 1 else '0' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

#Function to create a dictionary to store every character and its corresponding pixel representation.
def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }


##################################
#Prior probability calculation   #
##################################

def prob_letter_calculation( train_text_data ):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"'`:$&;/#^%*+_-)(|\}]{[><~@\r "
    prob_letter = {} # stores probability in logs
    letter_count = {}
    total_letters = 0
    pletter = {} # stores without log

    for eachletter in train_text_data:
        prob_letter[eachletter] = 0
        pletter[eachletter] = 0
        letter_count[eachletter] = 0

    for everyletter in train_text_data:
        prob_letter[everyletter]+=1
        letter_count[everyletter] +=1
        total_letters+=1
    
    for every in prob_letter.keys():
        if prob_letter[every]!=0:
            prob_letter[every]= float(prob_letter[every])/total_letters
        else:
            prob_letter[every] = 0.000000000000001
    
    for every in prob_letter.keys():
        pletter[every] = prob_letter[every]
        prob_letter[every] = -math.log(prob_letter[every])
 
    return prob_letter,pletter,letter_count

####################################
#Transition Probability Calculation#
####################################

def letter_transition(train_text_data,letter_count,prob_letter):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"'`:$&;/#^%*+_-)(|\}]{[><~@ "
    transition = {} # in log
    prob_transition = {} #without log

    for everyletter in prob_letter.keys():
        transition[everyletter] = {}
        prob_transition [everyletter] = {}
        for nextletter in prob_letter.keys():
            transition[everyletter][nextletter] = {}
            transition[everyletter][nextletter] = 0
            prob_transition[everyletter][nextletter] = 0

    for i in range(0,len(train_text_data)):
        if i+1<len(train_text_data):
            transition[train_text_data[i+1]][train_text_data[i]]+=1
            
    for every in transition.keys():
        for each in transition[every]:
            if letter_count[each]!=0:
                transition[every][each] = float(transition[every][each])/ letter_count[each] if (transition[every][each])!=0 else 0.000000000000001
            else:
                transition[every][each]=0.000000000000001
   
    for each in transition.keys():
        for every in transition[each]:
            prob_transition[each][every] = transition[each][every]
            transition[each][every]=-math.log(transition[each][every])
    return transition,prob_transition



# Function calls for training the program.
TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
print "Training in progress"
train_tdata = read_data(train_text_file)
prob_letter,pletter,letter_count = prob_letter_calculation( train_tdata )

for everyletter in TRAIN_LETTERS:
    if everyletter not in prob_letter.keys():
        prob_letter[everyletter] =  0.000000000000001
        letter_count[everyletter] = 1
        pletter[everyletter] = 1
        
prob_transition,transition  = letter_transition(train_tdata,letter_count,prob_letter)

print "Training done!"

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)


#Construction of emission probabilities
emission_1 = [[0 for x in range(0,14)]for y in range(0,25)]
emission_0 = [[0 for x in range(0,14)]for y in range(0,25)]
emission_dir = [[0 for x in range(0,14)]for y in range(0,25)]

for i in range(0,len(emission_1)):
    for j in range (0,len(emission_1[i])):
        emission_1[i][j]={}
        for everyletter in TRAIN_LETTERS:
            emission_1[i][j][everyletter] = 0

for i in range(0,len(emission_0)):
    for j in range (0,len(emission_0[i])):
        emission_0[i][j]={}
        for everyletter in TRAIN_LETTERS:
            emission_0[i][j][everyletter] = 0

#Calculate blackpixels in every training letter.
blackpixels = {}
for everyletter in TRAIN_LETTERS:
    blackpixels[everyletter] = 0

for everyletter in TRAIN_LETTERS:
        for i in range(0,25):
            for j in range(0,14):
                if train_letters[everyletter][i][j]=='0':
                    blackpixels[everyletter] +=1

for everyletter in TRAIN_LETTERS:
        for i in range(0,25):
            for j in range(0,14):
                if train_letters[everyletter][i][j]=='1':
                    emission_1[i][j][everyletter] = -math.log(float((1.0 + 1)/((14*25)+blackpixels[everyletter]))) 
                    emission_0[i][j][everyletter] = -math.log(float((0.0 + 1)/((14*25)+blackpixels[everyletter])))
                else:
                    emission_0[i][j][everyletter] = -math.log(float((1.0 + 1)/((14*25)+blackpixels[everyletter])))
                    emission_1[i][j][everyletter] = -math.log(float((0.0 + 1)/((14*25)+blackpixels[everyletter])))


obval = [0 for x in range(0,len(test_letters))]
emission = [0 for x in range(0,len(test_letters))]

for i in range(0,len(test_letters)):
    obval[i]={}
    emission[i]={}

#########################################
##NAIVE bayes implementation            #
#########################################

answer = ""
for k in range(0,len(test_letters)):
    for everysymbol in TRAIN_LETTERS:
        obval[k][everysymbol] = 0

    for i in range(0,25):
        for j in range(0,14):
            for everysymbol in TRAIN_LETTERS:
                if test_letters[k][i][j]=='1':
                    obval[k][everysymbol] +=(emission_1[i][j][everysymbol]) 
                else:
                    obval[k][everysymbol] +=(emission_0[i][j][everysymbol])


    min =9999999999
    rightletter = ""
    for everyletter in obval[k].keys():
        obval[k][everyletter] += (prob_letter[everyletter])
        if obval[k][everyletter]<min:
            min = obval[k][everyletter]
            rightletter = everyletter

    answer +=rightletter

print "Simple: ",answer


##Multiplying emission probabilities with scaling factor to get probabilities in non-logarithmic form.
for i in range(0,len(test_letters)):
    for every in TRAIN_LETTERS:
        emission[i][every]= math.exp(math.log(10e307)+math.log(10e307)+math.log(10e272)+ -obval[i][every])

##################################################
#Variable elimination implementation             #
##################################################
def hmm_ve(TRAIN_LETTERS, test_letters,worddir,transition,prob_letter):

        tou_table={}
        tags = []
        answer = ""

        max = 0.000000000
        tou_table["s1"] ={}

        #Finding letter for the first character in the test set.
        for eachtag in TRAIN_LETTERS:
            try:
                tou_s1 = prob_letter[eachtag] * (worddir[0][eachtag])
                tou_log = (tou_s1)
                if tou_log>max:
                    max = tou_log
                    final_tag = eachtag
                tou_table["s1"][eachtag] = tou_s1
            except:
                tou_s1 = (prob_letter[eachtag]) * ( 0.00000000000000001)
                tou_log = (tou_s1)
                if tou_log>max:
                    max = tou_log
                    final_tag = eachtag
                tou_table["s1"][eachtag] = tou_s1
        tags.append(final_tag)

        #Below code finds the most probable character for any letter from second position till second last.
        #We compute tow_table_forwards, emission probability for letterr i and tow_table_backward
        #Finally we find the argmax of product for the above three terms.

        for k in range(2,len(test_letters)): 
            i = 2
            for x in range(1,len(test_letters)):
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
                for eachtag in TRAIN_LETTERS:
                    
                    total = 0.0000000000
                    for everytag in TRAIN_LETTERS:
                        temp =  (transition[eachtag][everytag]) * (tou_table[variable][everytag])
                        total = total + temp
                    tou_table[variable1][eachtag] = total
                     #We do not multiply emission probability to the tow table when we have reached the position of the letter whose character is to be guessed using forward algorithm.
                    if q-1!=1:
                        try:
                            temp1 =  (worddir[wordcount][eachtag]) * (tou_table[variable1][eachtag])
                            tou_table[variable1][eachtag] = temp1
                        except:
                            temp1 = (0.00000000000000001)  * ( tou_table[variable1][eachtag])
                            tou_table[variable1][eachtag] = temp1
                wordcount = wordcount + 1    
                q = q -1
 
            #backward algo that runs from the last character upto the specific letter to be guessed.

            wordcount = len(test_letters) 
            if k==wordcount-1:
                variable = "s" + str(len(test_letters)-1) + "b"
            else:
                variable = "s" + str(len(test_letters)-1)
            for eachtag in TRAIN_LETTERS:
                total = 0.000000000000
                for everytag in TRAIN_LETTERS:
                    try:
                        temp =  (transition[everytag][eachtag]) * ( worddir[wordcount-1][everytag])
                        total = total  + temp
                    except:
                        temp =  (transition[everytag][eachtag])* (0.00000000000000001)
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
                #Here we multiply Tow_forward * emission prob * Tow_backward

                for eachtag in TRAIN_LETTERS:
                    total = 0.00000000000000
                    for everytag in TRAIN_LETTERS:
                        try:
                            temp =  (transition[everytag][eachtag]) * (worddir[wordcount-1][everytag])  * (tou_table[variable][everytag])
                            total = total + temp
                        except:
                            temp =  (transition[everytag][eachtag]) * (0.00000000000000001)  * (tou_table[variable][everytag])
                            total = total + temp
                    tou_table[variable1][eachtag] = total
                wordcount = wordcount-1
            
            max = 0.0000000
            variable = "s"+ str(k)+"a"
            variable1= "s" + str(k)+"b"
            

            max = 0.00000000000000000
            for eachtag in TRAIN_LETTERS:
                try:
                    total = (tou_table[variable][eachtag]) * ( tou_table[variable1][eachtag]) * ( worddir[k-1][eachtag])
                    
                    total_log = total
                    if total_log>max:
                        max = total_log
                        final_tag = eachtag
                except:
 
                    total = (tou_table[variable][eachtag]) * ( tou_table[variable1][eachtag]) * (  0.00000000000000001)
                    total_log = total
                    if total_log>max:
                        max = total_log
                        final_tag = eachtag
            
            tags.append(final_tag)

        #Calculates probability to find last letter in the image.
        max = -999999999.0
        tou_table1= {}
        i = 0
        for each in TRAIN_LETTERS:
            variable = "s"+str(i+1)
            tou_table1[variable] = {}
            i = i + 1
        for eachtag in TRAIN_LETTERS:
            try:
                tou_s1 = prob_letter[eachtag] * worddir[0][eachtag]
                tou_table1["s1"][eachtag] = tou_s1
            except:
                tou_s1 = prob_letter[eachtag] *  0.00000000000000001
                tou_table1["s1"][eachtag] = tou_s1
        
        i = 1
        temp = 0.00000000000

        max = 0.00000000000
        
        wordcount = 1
        max = 0.000000000000
        while wordcount<len(test_letters):
            variable1 = "s"+str(wordcount)
            variable2 = "s"+str(wordcount+1)
            max = 0.00000000000000
            for eachtag in TRAIN_LETTERS:
                total = 0.00000000000
                for everytag in TRAIN_LETTERS:
                    temp = transition[eachtag][everytag] * tou_table1[variable1][everytag]
                    total = total + temp
                try:
                    total1 = total * worddir[wordcount][eachtag]
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
        for every in tags:
            answer += every
        return answer


######################################
#VITERBI ALGORITHM IMPLEMENTATION    #
######################################

def viterbi(TRAIN_LETTERS,test_letters,transition,obval):
    answer = ""
    #Construct viterbi matrix
    vit = [[0 for i in range(0,len(TRAIN_LETTERS))]for j in range(0,len(test_letters))]

    maxarr=[]
    first_letter= test_letters[0]
    #Find viterbi value for first letter
    for i in range(0,len(TRAIN_LETTERS)):
        vit[0][i]= [(obval[0][TRAIN_LETTERS[i]] +  (prob_letter[everyletter])),0]

    #Filling up of viterbi matrix for all other letters
    for j in range(1,len(test_letters)):
        for k in range(0,len(TRAIN_LETTERS)):
            emission = obval[j][TRAIN_LETTERS[k]]
            minval ,mintag = 9999999,""

            for l in range(0,len(TRAIN_LETTERS)):
                val = vit[j-1][l][0] + transition[TRAIN_LETTERS[k]][TRAIN_LETTERS[l]]
                if val < minval:
                    minval = val
                    mintag = TRAIN_LETTERS[l]
        
            vit[j][k] = [(minval+emission),mintag]

    #Backtracking to find the correct sequence

    tagarr = []
    for i in range(len(test_letters)-1,0,-1):
        min = 999999999
        tag = ""
        for j in range(0,len(TRAIN_LETTERS)):
            if vit[i][j][0]<min:
                min = vit[i][j][0]
                mintag = vit[i][j][1]
                value = j
        if i== len(test_letters)-1:
            tagarr.append(TRAIN_LETTERS[value])
        tagarr.append(mintag)

    #Below case handles special case when there is just one letter.

    if len(test_letters)==1:
            min = 9999999999
            for i in range(0,len(TRAIN_LETTERS)):
                if vit[0][i][0]<min:
                    min = vit[0][i][0]
                    mintag = TRAIN_LETTERS[i]
            tagarr.append(mintag)

    tagarr.reverse()
    for every in tagarr:
        answer+=every

    return answer

print "HMM VE:" ,hmm_ve(TRAIN_LETTERS, test_letters,emission,transition,pletter)
print "HMM MAP:",viterbi(TRAIN_LETTERS,test_letters,prob_transition,obval)
