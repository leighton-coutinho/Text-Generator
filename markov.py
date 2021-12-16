#Leighton Coutinho Student ID:261016919
import random

def get_grams(text, k):
    ''' (str,num) --> dict
    This function will return dictionary of k grams
    based on markovs model, here k will be the second
    parameter and it will be judged using the string given
    >>> get_grams('gagggagaggcgagaaa', 2)
    {'ga': {'g': 4, 'a': 1}, 'ag': {'g': 2, 'a': 2}, 'gg': {'g': 1, 'a': 1, 'c': 1},
    'gc': {'g': 1}, 'cg': {'a': 1}, 'aa': {'a': 1}}
    >>> get_grams("She sells sea shells by the sea shore.", 1)
    {'S': {'h': 1}, 'h': {'e': 3, 'o': 1}, 'e': {' ': 2, 'l': 2, 'a': 2, '.': 1},
    ' ': {'s': 5, 'b': 1, 't': 1}, 's': {'e': 3, ' ': 2, 'h': 2}, 'l': {'l': 2, 's': 2},
    'a': {' ': 2}, 'b': {'y': 1}, 'y': {' ': 1}, 't': {'h': 1}, 'o': {'r': 1}, 'r': {'e': 1}}
    '''
    gramsdict = {}
    
    for i in range(len(text)-k):
        key = text[i:k+i]
        if key not in gramsdict:
            gramsdict[key] = {}

        mytext = text[i:k+i+1]
        if mytext[:k] == key:
            if mytext[-1] in gramsdict[key]:
                gramsdict[key][mytext[-1]] += 1
            else:
                gramsdict[key][mytext[-1]] = 1
        
           
    return gramsdict

def combine_grams(grams1, grams2):
    '''(dict,dict) --> dict
    This function will take two dictionaries of k grams.
    It will then add the occurences of each part and
    essentially combine the grams together
    >>> combine_grams({'a': {'b': 3, 'c': 9}, 'b': {'a': 10}},
    {'b': {'a': 5, 'c': 5}, 'c': {'d': 4}})
    {'a': {'b': 3, 'c': 9}, 'b': {'a': 15, 'c': 5}, 'c': {'d': 4}}
    >>> combine_grams({'a': {'b': 3, 'c': 9}}, {'c': {'d': 4}})
    {'a': {'b': 3, 'c': 9}, 'c': {'d': 4}}
    >>> combine_grams({'a': {'b': 3, 'c': 9}, 'b':12},{'b':5, 'c': {'d': 4}})
    {'a': {'b': 3, 'c': 9}, 'b': 17, 'c': {'d': 4}}
    >>> combine_grams({'a': {'b': 3, 'c': 9}, 'b': 12},{'b': {b:5,a:10} , 'c': {'d': 4}})
    {'a': {'b': 3, 'c': 9}, 'b': {b: 17, a:10}, 'c': {'d': 4}}
    '''
    combinedgrams = {}
    #first look at grams1
    for key in grams1:
        if key in grams2:
            # if key value is a dictionary then we look into the dictionary and add values
            if type(grams1[key]) == dict:
                mydict = {}
                for innerkey in grams1[key]:
                    if innerkey in grams2[key]:
                        added = grams1[key][innerkey] + grams2[key][innerkey]
                        mydict[innerkey] = added
                    else:
                        mydict[innerkey] = grams1[key][innerkey]
                # look at grams2 inner dictionary and add inner keys that were not in grams1
                for innerkey in grams2[key]:
                    if innerkey not in grams1[key]:
                        mydict[innerkey] = grams2[key][innerkey]
                combinedgrams[key] = mydict
            #if key value is an integer then we just add the integers
            else:
                combinedgrams[key] = grams1[key]+grams2[key]
        else:
            combinedgrams[key] = grams1[key]
    # look at grams2 and add keys that were not in grams1
    for key in grams2:
        if key not in grams1:
            combinedgrams[key] = grams2[key]
            
    return combinedgrams



def get_grams_from_files(filenames, k):
    ''' (list,num) --> dict
    This function takes a list with strings corresponding to filenames
    it will then read these files and create a k grams dictionary
    for each file. It will then return a dictionary with the combined
    k gram dictionary
    >>> grams = get_grams_from_files(['raven.txt'], 4)
    >>> len(grams)
    3023
    >>> grams['drea']
    {'r': 1, 'm': 4}
    '''
    gramslist = []
    for file in filenames:
        text = ''
        fobj = open(file, "r", encoding='utf-8')
        for line in fobj:
            text += line
        fobj.close()
        gramsdict = get_grams(text, k)
        gramslist.append(gramsdict)
    count = 0
    while True:
        if len(gramslist) == 1:
            return gramslist[0]
        combinedlist = combine_grams(gramslist[0], gramslist[1])
        gramslist.pop(0)
        gramslist.pop(0)
        gramslist.insert(0,combinedlist)

        
def generate_next_char(grams, cur_gram):
    ''' (dict,str) --> list,list
    This function will take a k grams dictionary and a string
    corresponding to the current k gram, it will then return
    the prediction of the next character using the probabilities
    (Instead of probability here we use random.choice)
    >>> random.seed(9001)
    >>> generate_next_char({'a': {'b': 3, 'c': 9}, 'c': {'d': 4}}, 'a')
    'b'
    >>> generate_next_char({'a': {'b': 3, 'c': 9}, 'c': {'d': 4}}, 'a')
    'c'
    >>> random.seed(1337)
    >>> grams = get_grams_from_files(['raven.txt'], 4)
    >>> generate_next_char(grams, 'drea')
    'm'
    '''
    items = []
    weighting = []
    total = 0
    if cur_gram not in grams:
        raise AssertionError("Given gram is not in the dictionary")
    for key in grams:
        if len(key) != len(cur_gram):
            raise AssertionError("Given gram has different number of character than keys in dictionary")
    
    items = list(grams[cur_gram].keys())
    for key in grams[cur_gram]:
        total += grams[cur_gram][key]
    for i in items:
        weighting.append(grams[cur_gram][i]/total)
  
    return random.choices(items, weighting)[0]


def generate_text(grams, start_gram, k, n):
    '''(dict,str,num,num) --> str
    This function generates a text of length n using k
    characters for the start_gram. It will generate the rest
    of the characters using the gram dictionary and will
    return the text
    >>> random.seed(1330)
    >>> grams = get_grams_from_files(['raven.txt'], 5)
    >>> generate_text(grams, "Once upon", 5, 200)
    Once upon the tempest tossed this desert land enchanted—tell me—tell me, I implore—
    Quoth the Raven, thou,” I cried, “thy God we both adore—
    Tell the floor.
    ’Tis soul with my head at ease
    '''
    text = start_gram[:k]
    count = 0
    while count < n-k:
        cur_gram = text[-k:]
        newchar = generate_next_char(grams, cur_gram)
        text += newchar
        count +=1
    for i in range(1,len(text)):
        if text[-i] == ' ' or text[-i] == '\n':
            text = text[:-i]
            break 
    
    return text



def repair_text(corrupted_text, error_char, grams, k):
    '''(str,str,dict,num) --> str
    This function will take a corrupted text with certain error characters,
    it will then remove the error characters and replace them with
    characters generated through the k grams dict
    >>> random.seed(1330)
    >>> grams = get_grams_from_files(['raven.txt', 'beowulf.txt'], 5)
    >>> repair_text('it was th~ bes~ of tim~s, i~ was ~he wo~st of~times', '~', grams, 5)
    it was the best of times, in was Bhe wolst of times
    '''
    correct_text = corrupted_text
    updated_grams = {}
    for key in grams:
        updated_grams[key] = grams[key]
    for i in range(len(corrupted_text)):
        if correct_text[i] == error_char:
            cur_gram = correct_text[i-k:i]
            newchar = generate_next_char(updated_grams, cur_gram)
            correct_text = correct_text[:i] + newchar + correct_text[i+1:]
            updated_grams[cur_gram][newchar] += 1
    
    return correct_text
            



