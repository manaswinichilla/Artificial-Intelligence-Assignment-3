# classify.py : Classify text objects into two categories
#
# admysore-hdeshpa-machilla
#
# Based on skeleton code by D. Crandall, March 2021
#


import sys
import re

#function to load the filename and return a dictionary of objects labels and classes
def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ', 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            objects.append(parsed[1] if len(parsed) > 1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# Given a text, the function is to return the text with lower case, stop words removed, and any other extra characters removed
def clean_text(text):
    stop_words = {'all', 'whys', 'being', 'over', 'isnt', 'through', 'yourselves', 'hell', 'its', 'before', 'wed',
                  'with', 'had', 'should', 'to', 'lets', 'under', 'ours', 'has', 'ought', 'do', 'them', 'his', 'very',
                  'cannot', 'they', 'werent', 'not', 'during', 'yourself', 'him', 'nor', 'wont', 'did', 'theyre',
                  'this', 'she', 'each', 'havent', 'where', 'shed', 'because', 'doing', 'theirs', 'some', 'whens', 'up',
                  'are', 'further', 'ourselves', 'out', 'what', 'for', 'heres', 'while', 'does', 'above', 'between',
                  'youll', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'both', 'about', 'would', 'wouldnt',
                  'didnt', 'ill', 'against', 'arent', 'youve', 'theres', 'or', 'thats', 'weve', 'own', 'whats', 'dont',
                  'into', 'youd', 'whom', 'down', 'doesnt', 'theyd', 'couldnt', 'your', 'from', 'her', 'hes', 'there',
                  'only', 'been', 'whos', 'hed', 'few', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'on',
                  'but', 'you', 'hadnt', 'shant', 'mustnt', 'herself', 'than', 'those', 'he', 'me', 'myself', 'theyve',
                  'these', 'cant', 'below', 'of', 'my', 'could', 'shes', 'and', 'ive', 'then', 'wasnt', 'is', 'am',
                  'it', 'an', 'as', 'itself', 'im', 'at', 'have', 'in', 'id', 'if', 'again', 'hasnt', 'theyll', 'no',
                  'that', 'when', 'same', 'any', 'how', 'other', 'which', 'shell', 'shouldnt', 'our', 'after', 'most',
                  'such', 'why', 'wheres', 'a', 'hows', 'off', 'i', 'youre', 'well', 'yours', 'their', 'so', 'the',
                  'having', 'once', ''}
    text=text.lower()
    words=text.split()
    resultwords  = [word for word in words if word not in stop_words]
    text = ' '.join(resultwords)
    only_chars = '[^a-zA-Z\s]+'
    text = re.sub(only_chars, '', text)
    text = re.sub(' +', ' ', text)
    text = text.replace('\r', '')
    text = text.replace('\n', '')
    text = text.replace('\w', '')
    return text.strip().lower()

# This function calls clean_text for every object in train_data and updates the “cleaned” text in the train_data
def remove_punctuation(train_data):
    for index in range(len(train_data['objects'])):
        train_data['objects'][index]=clean_text(train_data['objects'][index])
    return train_data

# This function is to return a list of unique words in the train_data
def generate_unique_words(train_data):
    unique_words=[]
    num=0
    for obj in train_data['objects']:
        for word in obj.split():
            if(word not in unique_words):
                unique_words.append(word)
    return unique_words

# This returns the probability of getting class one and class two
def p_of_both_classes(train_data, class_one, class_two):
    count_label = {class_one: 0, class_two: 0}
    index = 0
    all_words_class_one = 0
    all_words_class_two = 0
    for label in train_data['labels']:
        if (label == class_one):
            count_label[class_one] += 1
            all_words_class_one += 1
        else:
            count_label[class_two] += 1
            all_words_class_two += 1
        index += 1
    p_of_class_one = count_label[class_one] / len(train_data['labels'])
    p_of_class_two = count_label[class_two] / len(train_data['labels'])

    return [p_of_class_one, p_of_class_two, all_words_class_one, all_words_class_two]

# This returns the number of times word has appeared in messages classified as class one and class two in train_data
def n_of_word_given_class(uniqueword, train_data):
    class_one = train_data['classes'][0]
    total_word_in_class_one=0
    total_word_in_class_two=0
    index=0
    for label in train_data['labels']:
        if str(label)==str(class_one):
            for word in train_data['objects'][index].split():
                if word==uniqueword:
                    total_word_in_class_one+=1
        else:
            for word in train_data['objects'][index].split():
                if word == uniqueword:
                    total_word_in_class_two += 1
        index+=1

    return [total_word_in_class_one,total_word_in_class_two]

# This function is to return the probability of word given class_one and class_two
def p_of_word_given_classes(word, train_data, all_words_class_one, all_words_class_two, len_of_unique_words):
    n_word = n_of_word_given_class(word, train_data)
    p_of_word_given_class_one = (n_word[0] + 1) / (all_words_class_one + len_of_unique_words)
    p_of_word_given_class_two = (n_word[1] + 1) / (all_words_class_two + len_of_unique_words)

    return [p_of_word_given_class_one, p_of_word_given_class_two]

# This function calls the above function with required parameters, given an object, classifies as class_one
# if probability of class given obj is higher and class_two otherwise.
def classify(obj, train_data, p_of_class_one, p_of_class_two, all_words_class_one, all_words_class_two, len_of_unique_words, class_one,
             class_two):
    obj = re.sub('\W', ' ', obj)
    obj = obj.split()

    p_of_class_one_given_obj = p_of_class_one
    p_of_class_two_given_obj = p_of_class_two

    for word in obj:
        p_of_word_given_class = p_of_word_given_classes(word, train_data, all_words_class_one, all_words_class_two, len_of_unique_words)
        p_of_class_one_given_obj *= p_of_word_given_class[0]
        p_of_class_two_given_obj *= p_of_word_given_class[1]

    if p_of_class_two_given_obj > p_of_class_one_given_obj:
        return class_two
    elif p_of_class_one_given_obj > p_of_class_two_given_obj:
        return class_one

# This function, iterates through the objects in test_data, with the help of above functions, collects the list of
# predictions and returns it.
def classifier(train_data, test_data):
    train_data = remove_punctuation(train_data)
    test_data = remove_punctuation(test_data)
    unique_words = generate_unique_words(train_data)
    class_one = test_data['classes'][0]
    class_two = test_data['classes'][1]
    p_of_classes = p_of_both_classes(train_data, class_one, class_two)
    p_of_class_one = p_of_classes[0]
    p_of_class_two = p_of_classes[1]
    all_words_class_one = p_of_classes[2]
    all_words_class_two = p_of_classes[3]
    predicted=[]
    for obj in test_data['objects']:
        prediction=classify(obj, train_data, p_of_class_one, p_of_class_two, all_words_class_one, all_words_class_two, len(unique_words), class_one, class_two)
        predicted.append(prediction)
    return predicted

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if (train_data["classes"] != test_data["classes"] or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([(results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"]))])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))