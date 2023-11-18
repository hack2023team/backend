import zipfile
import pandas as pd
import random

# in progress

def getRecomendations(m_number, m_tags, m_ingredients, m_disliked_ingredients, m_p_min_tags, m_p_max_ingredients):
    # number of recomendations
    number = m_number
    # tags to compare with
    tags = m_tags
    # matrix with lists of ingredients, for each liked meal one list
    ingredients = m_ingredients
    # list of disliked ingredients
    disliked_ingredients = m_disliked_ingredients
    # the minimum percentage of tags of a dataset entry that should have to be part of tags, to consider for reccomendation
    p_min_tags = m_p_min_tags
    # the maximum percentage of ingridients of a dataset entry that intersect with a combination of ingridients
    p_max_ingredients = m_p_max_ingredients # read the dataset using the compression zip


    # search through dataset in a random way
    #for i in random.shuffle(range(len(df))):
        # check if percentage of tags is reached
       # p_tags = list(set(tags) & set(df.loc[i]))







    return

def createRecepyBase():

    # load 1000 rows of csv (restricted due to demonstration purposes)
    df = pd.read_csv('RAW_recipes.csv', nrows=1000)
    print(list(df.columns))
    print(df.dtypes)

    #TODO create hashmap
    # create numpy matrix: rows-recipies, cols-ingredients
    return

if __name__ == "__main__":
    testnumber = 2
    if testnumber == 1:
        getRecomendations(
            m_number=10,
            m_tags=["indian", "healthy", "carbs", "chinese", "pork"],
            m_ingredients=[
                ["rice", "pumpkin", "potato", "soy sauce", "salt", "pepper", "pepperoni", "cilantro"],
                ["noodles", "tomatoes", "garlic", "olive oil", "salt", "pepper", "parmigano"],
                ["paprika","rice", "minced meat", "onions"]],
            m_disliked_ingredients=["pork belly", "peanuts"],
            m_p_min_tags=0.7,
            m_p_max_ingredients=0.7
        )
    elif testnumber == 2:
        createRecepyBase()

