# encountering a byte error because sql dumps are in latin1
#import sys
#reload(sys)
#sys.setdefaultencoding('latin-1')

'''

IMPORTANT: Requires several nltk packages.
Install by running
import nltk
nltk.download()

Need porter stemmer, and the stopwords corpus
'''
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords

def clean_punctuation(text):
    #fixed_slashes = text.replace('/',' ')
    fixed_slashes = text
    custom_punc = '!"#$%&\'()*,.:;<=>?@[\]^_`{|}-~'
    translate_table = str.maketrans(
        custom_punc, ''.join([' ' for i in range(0, len(custom_punc))]))
    try:
        desc = fixed_slashes.lower().translate(translate_table)
        return desc
    except TypeError:
        print('TypeError: Translate function does not accept unicode.')

def remove_stop(text):
    desc_tokens = nltk.word_tokenize(text)
    no_stopwords = [word for word in desc_tokens if not word in stopwords.words('english')]
    no_stopwords = [word for word in no_stopwords if not word in ['+', '-']] # remove singletons
    return no_stopwords

def stem(tokens):
    stemmed = []
    for item in tokens:
        stemmed.append(PorterStemmer().stem(item))
    return stemmed

def stringify(tokens):
    s = ''
    for token in tokens:
        s += token
        s += ' '
    return s.rstrip() # remove the last space

def clean_tokens(text):
    return stem(remove_stop(clean_punctuation(text)))

if __name__ == '__main__':
    '''
    sample usage
    '''
    t = "Rehabilitation/Reconstruction/Removal of Gravel on Bulacan, Road. North km+1993-km+384"
    print(t)

    st = clean_tokens(t)
    print(st)

    print(stringify(st))
