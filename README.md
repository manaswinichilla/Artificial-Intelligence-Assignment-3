# Assignment 3
**Part 1- Pikachu**

**Search Abstraction:**

**Initial state**- A board with any number of pichus or pikachus of any of the black or white players in any position

**Search space**- Any board generated by moving the players( white or black ) pichus or pikachus according to below constraints
-> Move a single Pichu, one square forward, left, or right, if that square is empty

-> Move a single Pichu of his or her color to “jump” over a single piece of the opposite color by moving
two squares forward, left, or right, if that square is empty.

-> Move a single Pikachu of his or her color any number of squares forward, left, right, or backwards, to
an empty square, as long as all squares in between are also empty

-> Move a single Pikachu of his or her color to “jump” over a single piece of the opposite color and
landing any number of squares forward, left, right, or backwards, as long as all of the squares between
the Pikachu’s start position and jumped piece are empty and all the squares between the jumped piece
and the ending position are empty.

**Successor**- List of boards from the initial/ current board after making below moves
-> a pichu moves one square forward, left, or right, if that square is empty.

-> a pichu “jumps” over a single piece of the opponent player by moving
two squares forward, left, or right, if that square is empty.

-> a pikachu moves any number of squares forward, left, right, or backwards, to
an empty square, as long as all squares in between are also empty

-> a pikachu “jump” over a single piece of the opponent player and
landing any number of squares forward, left, right, or backwards, as long as all of the squares between
the Pikachu’s start position and jumped piece are empty and all the squares between the jumped piece
and the ending position are empty.

**Goal state**- A board where one of the player captures all of the other player’s pieces first

**Evaluation Function** - We are taking the count of player's and opponent's pichu's and pikachu's.
We take the difference between the player and opponents pichus and pickachu counts. 
I have assigned a weight of 100 for the pikachu difference, as they have more mobility. 
And no weight for the mobility of the birds(pichus).

I tried the different Evaluation functions from the the refrences below but 
found that the basic function was giving me efficiency in terms of time
# https://www.cs.huji.ac.il/~ai/projects/old/English-Draughts.pdf 

**Strategy**

As, each an every board can have multiple successors the branching factor of the search tree can be high. 
So, we have decided to limit the depth of the tree as well as prune the search tree.
For this we have used the alpha beta pruning algorithm with iterative deepening approach.

**Functions:** 

**find_best_move()**

We use this function for finding the next move and yield the board with this next move.
We convert the string of the board in 2d list, which is what i will be using in the rest of teh program.
We give a depth limit parameter which is being incremented by 2. By two as we would need a min and a max layer for deciding next best move.

We call the **"min_max_decision"** function, which calls the get_opponent function, which returns the opponent of the player.
We have set the deafult values for alpha and beta
 alpha_value = -1000000000000
 beta_value =  +1000000000000
Then it gets the successor of the initial board and call the "min_value" 
We provide the depth as 0, which is then incremented by the min_value and max_value functions

**Min_value**

This is the layer which will be played by the opponent.
We check if we have reached the depth limit which we are iterating from min_max_decision. 
Or if we have reached goal state, then we call the evaluation function and return the score.
If we havent recahed the goal or the depth limit then
We call all the successors of the opponent player and then call the max layer for each of these successors
We get a score from the max layer for the alpha value.
 We check if this new score by the max layer is less than the local beta value we have. If it is then we update the local beta value
 We check if this new score is less than the default beta value we have and update the default beta Value.
 We check if it this value by the max layer is greater than the alpha value we have, if it is then we return this value


**Max_value**

This is the layer which will be played by the player.
We check if we have reached the depth limit which we are iterating from min_max_decision. 
Or if we have reached goal state, then we call the evaluation function and return the score.
If we havent recahed the goal or the depth limit then
We call all the successors of the player and then call the min layer for each of these successors
We get a score from the min layer for the beta value.
 We check if this new score by the min layer is greater than the local alpha value we have. 
 If it is then we update the local alpha value
 We check if this new score is greater than the default alpha value we have and update the default alpha Value.
 We check if it this value by the min layer is less than the beta value we have, if it is then we return this value

#
**Part 2 - Sebastian Game**

**Search Abstraction** :

**Initial state-** Random dice roll

**State space-** Dice rolls

**Successor state-** A list of dice rolls for all possible combinations made if the dice has a true value

**Evaluation function-** Dice value list and the expected score

**Maximum layer-** Gives the maximum score over all the successors

**Goal state-** After 13 iterations, all the categories must be assigned.

**Cost-** Cost calculated as per the game rules.

**_Stratergy_** :

This modified version of yahtzee game is implemented using *'expectiminimax'*.

Our implementation follows week 8's discussion session, 'A game of chance'. We have a max_layer function, a expectation function, a cost_function, get_dice_list, get_list_of_categories as helper functions.

After the initial random dice roll, the program picks up the next best roll based on the expected score of all the unvisited categories. This happens once more, if a better dice roll is found. 
So, after 13 iterations, our program covers all the 13 categories, and gives the total-score.

After 100 iterations, we get the lowest and highest total-score seen so far and also the average of all the total-scores.

**Functions:** 

**_max_layer function_** : 

This is the max layer of expectiminimax. It is used to get the maximum score over all of its successors. To figure out the best stratergy, it takes on boolean values for each of the dice values in the list. A 'True' value for a dice indicates that it can be rerollled while a 'False' value means that it doesn't have to be rerolled.

For each such possibility, it fetches the score for that dice value list. It returns the maximum score at the end of the function.

For example, if a dice roll=[False, True, False, False, False] implies that only the 2nd dice value needs to be rerolled.

Now, this maximum_layer function calls the 'expectation' function.

**_expectation function_**:

This function calculates the score over all the successors. This function calls the 'get_dice_list' to get dice value list.

For each dice list, we call the 'cost_function', from which we'll get a scorelist with scores for all the categories that haven't been covered yet.
For each of these categories' scores, we calculate the probability and then get the max score among these. 

We do this for all the posibilities, get the max out of it and return its expected score and the dice value list.


**_get_dice_list_** :

This function gets the dice list values over all the successors. 

For each dice value in the dice list, it checks the boolean value and decides whether to reroll or not.


**_cost_function_** :

We maintain a dictionary, 'scorelist'.
We use this function in the expectation function, to calculate the score for categories that haven't been visited yet and whose conditions are satisfied by the list of dice values.
If the list of dice values doesn't satify a category's conditions, then we give it a value of 0.


**_get_list_of_categories_** :

This function is to return a list of categories that haven't been visited.

**_first_roll_** :

This takes dice and scorecard. To get the first_roll, we call the max_layer by passing dice and the categories that haven't been covered yet.
This will return the new best dice value list.

**_second_roll_** :
This takes dice and scorecard. To get the second_roll, we call the max_layer by passing dice and the categories that haven't been covered yet.
This will return the new best dice value list, if one exists.

**_third_roll_** :

This takes dice and scorecard. It calls the cost_function by passing dice and the list of categories that haven't been covered yet.
This returns the best category that the dice list can be assigned to.



#
**Part 3 -Naive Bayes Classifier**

**Strategy**:

given a message, we need to classify class_one or class_two.

To compute this, we need probabilty of getting the class, and product of probability of each word given a message is class_one/class_two

P(class_one |word1,word2,...wordn)
=P(class_one)*product of(P(word_i| class_one)) for all words in message

Similarly for class_two,

P(class_two|word1,word2,...wordn)=P(class_two(0))*product of(P(word_i| class_two)for all words in message

We can find P(word_i| class_one) and P(word_i|class_two) as follows:
P(word_i| class_one):
=  No_of_word_in_class_one/No_of_class_one + no_of_unique_words

Similarly:
P(word_i| class_two):
=  No_of_word_in_class_two/No_of_class_two + no_of_unique_words

We iterate through the test set objects, for every word in each of the objects we compute P(word|class_one) and P(word|class_two) and multiply these with P(class one) and P(class_two) respectively. Of these two, whichever the probability is higher, the message is classied into that respective category. This is done for all messages in the test set. 

The functions in the program are as follows:

**def load_file(filename):** 
function to load the filename and return a dictionary of objects labels and classes

**def clean_text(text):**
given a text, the function is to return the text with lower case, stop words removed, and any other extra characters removed

**def remove_punctuation(train_data):**
this function calls clean_text for every object in train_data and updates the “cleaned” text in the train_data

**def generate_unique_words(train_data):**
This function is to return a list of unique words in the train_data 

**def p_of_both_classes(train_data, class_one, class_two):**
this returns the probability of getting class one and class two

**def n_of_word_given_class(uniqueword, train_data):**
this returns the number of times word has appeared in messages classified as class one and class two in train_data

**def p_of_word_given_classes(word, train_data, all_words_class_one, all_words_class_two, len_of_unique_words)**:
this function is to return the probability of word given class_one and class_two

**def classify(obj, train_data, p_of_class_one, p_of_class_two, all_words_class_one, all_words_class_two, len_of_unique_words, class_one,
             class_two):**
this function calls the above function with required parameters, given an object, classifies as class_one if probability of class given obj is higher and class_two otherwise.

**def classifier(train_data, test_data):**
this function, iterates through the objects in test_data, with the help of above functions, collects the list of predictions and returns it.

**Citations:**

part 1:

_For Evaluataion Function_

https://www.cs.huji.ac.il/~ai/projects/old/English-Draughts.pdf

http://www.cs.columbia.edu/~devans/TIC/AB.html
_For Alpha-Beta Pruning:_
https://youtu.be/zp3VMe0Jpf8

part 2:

Professor Crandall's solution code explanation for week 8's activity- 'a game of chance'

https://www.dicegamedepot.com/yahtzee-rules/

https://amp.en.google-info.org/1153192/1/expectiminimax.html

part 3:

https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
https://www.kdnuggets.com/2020/07/spam-filter-python-naive-bayes-scratch.html
