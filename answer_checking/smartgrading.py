import numpy as np
import string
from sentence_transformers import SentenceTransformer, util

# Calculate the Levenshtein distance between two strings, and return true if they differ by either 1 character or at most 15% of their characters
def typo_check(answer, input):
    distances = np.zeros((len(answer) + 1, len(input) + 1))

    for i in range(len(answer) + 1):
        distances[i][0] = i
    for i in range(len(input) + 1):
        distances[0][i] = i

    a = 0
    b = 0
    c = 0
    
    for i in range(1, len(answer) + 1):
        for j in range(1, len(input) + 1):
            if (answer[i-1] == input[j-1]):
                distances[i][j] = distances[i - 1][j - 1]
            else:
                a = distances[i][j - 1]
                b = distances[i - 1][j]
                c = distances[i - 1][j - 1]
                
                if (a <= b and a <= c):
                    distances[i][j] = a + 1
                elif (b <= a and b <= c):
                    distances[i][j] = b + 1
                else:
                    distances[i][j] = c + 1

    return distances[len(answer)][len(input)] == 1 or distances[len(answer)][len(input)] <= 0.15 * len(answer)

# Remove the words 'a' 'an' and 'the' from a text input
def remove_articles(input):
    input = input.split(' ')
    output = []

    for i in input:
        if i not in ['a', 'an', 'the']:
            output.append(i)

    return ' '.join(output)

# Preprocesses text input, removing capitalization, punctuation, and articles
def clean(input):
    return remove_articles(input.translate(str.maketrans('','', string.punctuation)).lower())

# Calculates the cosine similarity between two sentences, the user input and true answer, which are embedded using the pretrained 'all-MiniLM-L6-v2' model
def similarity(input, answer):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    input_embedding = model.encode(input, convert_to_tensor=True)
    answer_embedding = model.encode(answer, convert_to_tensor=True)

    return util.cos_sim(input_embedding, answer_embedding).item()

# Checks if the answer is acceptable
def check(input, answer):
    # Arbitrary choice of threshold hyperparameter, fine-tuning needed on user data
    threshold = 0.5

    input_c = clean(input)
    answer_c = clean(answer)
    
    if typo_check(answer_c, input_c):
        return True
    # If the typo check fails, use the model to calculate similarity
    else:
        # Return true if the similarity score is above the threshold
        return similarity(input, answer) > threshold
