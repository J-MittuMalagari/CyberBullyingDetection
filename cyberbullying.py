import string
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from cyberbullying.sentimentanalyzer import getCommentSentiment

def emojiremoval(item):

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  # other emoticons
                               u"\U0001F923"  # rolf emoji
                               u"\U000024C2-\U0001F251" "]+", flags=re.UNICODE)
    return "".join(emoji_pattern.sub(r'', item)) + "\n"

def normalizing(item):

    # tokenize the sentences
    tokens = word_tokenize(item)

    # convert to lower case
    tokens = [w.lower() for w in tokens]

    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]

    # remove stopwords from each sentence
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]

    return " ".join(tokens) + "\n"

def isBullyingPost(comment):

    comment = str(emojiremoval(comment))
    comment = str(normalizing(comment))
    sentiment = getCommentSentiment(comment)

    tokens = word_tokenize(comment)

    tokenlist = []

    for i in tokens:
        if len(i) >= 3 and i.isalpha():
            tokenlist.append(i)

    i = 0

    badwords = []

    filenames = [
        'D:\\major_project_code\\CyberbullyingDetection\\CyberbullyingDetection\\dataset\\Hurtful.txt',
        'D:\\major_project_code\\CyberbullyingDetection\\CyberbullyingDetection\\dataset\\Obscene.txt',
        'D:\\major_project_code\\CyberbullyingDetection\\CyberbullyingDetection\\dataset\\Insults.txt',
        'D:\\major_project_code\\CyberbullyingDetection\\CyberbullyingDetection\\dataset\\Racist.txt']

    while i != 4:
        with open(filenames[i]) as infile:
            for line in infile:
                line = line[:-1]
                line.strip()
                badwords.append(line)
            i += 1
    flag = 0

    for t in tokenlist:
        for i in badwords:
            if i == t:
                flag = 1
    if flag == 1:
        return True
    else:
        return False
