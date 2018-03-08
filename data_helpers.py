import numpy as np
import re
import itertools
from collections import Counter
import numpy as np
from numpy import array

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    '''positive_examples = list(open(positive_data_file, "r").readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(negative_data_file, "r").readlines())
    negative_examples = [s.strip() for s in negative_examples]'''

    tempString = ""
    tempList = []
    positive_examples = []
    negative_examples = []
    x_text = []
    
    #A = np.array([1,2,3,4,5,6])
    '''a = [1,2,3,4]
    b = [5,6,7,8]
    tempList.append(a)
    tempList.append(b)
    
    A = np.array(tempList)
    print (A[0])
    B = np.reshape(A, (2, 4))
    print(B[0][0])
    #B = np.reshape(A, (-1, 4))
    #print(B[0])'''


    with open("./data/rt-polaritydata/malicious.pos", "r") as f:
        for line in f:
            if line != "\n":
                tempString += line
            else:
                tempString = tempString[:-1] #remove \n
                tempString = tempString.replace(" ", "")    #size 20000
                for x in tempString:
                    tempList.append(int(x))
                positive_examples.append(tempList[:])
                x_text.append(tempList[:]) #append copy of list instead of reference
                tempList[:] = []
                tempString = ""

    tempList[:] = []
    tempString = ""

    with open("./data/rt-polaritydata/non_malicious.neg", "r") as f:
        for line in f:
            if line != "\n":
                tempString += line
            else:
                tempString = tempString[:-1] #remove \n
                tempString = tempString.replace(" ", "")
                for x in tempString:
                    tempList.append(int(x))
                negative_examples.append(tempList[:])
                x_text.append(tempList[:])
                tempList[:] = []
                tempString = ""

    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
