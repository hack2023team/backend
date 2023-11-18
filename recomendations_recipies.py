import pandas as pd
import numpy as np
from dataframe_initialization import createMatrix, createRecipyBase
from ast import literal_eval
import  random


# in progress
def getRecepy(df, id):
    return df.iloc[id, :].tolist()

def exampleDislikes():
    return ["peanuts", "apple", "duck"]
def storedIdsTuples(stored_ids, stored, dislikes_ingredients, df):

    return
def getRecepyIDs(stored_ids=[1,2,3,4,5], dislikes_ingredients=[]):
    df = pd.read_csv("data/prepared_recipes.csv")
    df["tags_keys"] = df["tags_keys"].apply(literal_eval)
    df["ingredients_keys"] = df["ingredients_keys"].apply(literal_eval)
    stored=df.loc[stored_ids]
    tags = stored['tags_keys'].explode().unique()
    i_matrix = np.load("data/i_matrix.npy", allow_pickle=True)
    t_matrix = np.load("data/t_matrix.npy", allow_pickle=True)
    result = getRecomendations(
        df,
        200,
        tags,
        stored["ingredients_keys"],
        dislikes_ingredients,
        m_p_min_tags=0.1,
        m_p_max_ingredients=0.90,
        m_p_min_ingredients=0.2,
        i_matrix=i_matrix,
        t_matrix=t_matrix
        )
    recepy_ids = result
    store_index = stored_ids
    for index in range(len(stored_ids)):
        rand = random.randint(0, index*4)
        recepy_ids = np.insert(recepy_ids, rand, stored_ids[index])
        store_index[index] = rand
    recepy_ids = [(i,i) for i in recepy_ids]
    return recepy_ids
# to get the clostest match, put m_p_max ingridients on 1.0 and use m_number=1
def getRecomendations(
        df, m_number, m_tags, m_ingredients, m_disliked_ingredients, m_p_min_tags, m_p_max_ingredients, m_p_min_ingredients,i_matrix,
        t_matrix):


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
        p_max_ingredients = m_p_max_ingredients  # read the dataset using the compression zip

        #get indexes of rows that contain disliked ingrediens
        row_indices = np.where(np.any(i_matrix[:, m_disliked_ingredients] == 1, axis=1))[0]
        indices_to_delete = list(row_indices)

        # create mask of wanted ingredients
        i_mask = np.zeros((len(m_ingredients), i_matrix.shape[1]), np.int8)
        for i, row in enumerate(m_ingredients):
            i_mask[i, row] = 1

        # create mask of wanted tags
        t_mask = np.zeros((1, t_matrix.shape[1]), np.int8)
        for i in m_tags:
            t_mask[0, i] = 1

        # result with one row for every recipy
        result = np.zeros((i_matrix.shape[0], len(m_ingredients) + 3))
        # 1st row sum of all ones per recipy
        result[:, 0] = np.sum(i_matrix, axis=1)  # sum rows together
        # 4th to nth row partition of common ones
        for i in range(len(m_ingredients)):
            copy_matrix = np.logical_and(i_matrix, i_mask[i])
            result[:, i + 3] = np.sum(copy_matrix, axis=1)
            result[:, i + 3] = result[:, i + 3] * 1.0 / result[:, 0]

        # 2nd row
        result[:, 1] = np.sum(t_matrix, axis=1)
        # 3rd row partition of common tags
        copy_matrix = np.logical_and(t_matrix, t_mask[0])
        result[:, 2] = np.sum(copy_matrix, axis=1)
        result[:, 2] = result[:, 2] * 1.0 / result[:, 1]

        # keep partition describing rows and create id
        result = result[:,1:]
        b = np.arange(result.shape[0]).reshape((-1, 1))
        result[:, 0] = b[:,0]
        # 1st: id 2nd:tag percentage, rest: ingredient percentages
        # filter data
        mask = np.ones(result.shape[0], dtype=bool)
        mask[indices_to_delete] = False

        # Filter the array to keep only rows not in the list
        result = result[mask] #todo check if it works
        result[:, 1] = result[:, 1]*3 + np.sum(result[:, 2:], axis=1)
        sorted_indices = np.argsort(result[:,1])
        result = result[sorted_indices]
        if result.shape[0] >= m_number:
            result = result[: m_number, : 1]
        else:
            result = result[:, : 1]
        return result



if __name__ == "__main__":
    testnumber = 4
    if testnumber == 1:
        getRecomendations(
            m_number=10,
            m_tags=[20, 1, 23, 3, 35, 48],
            m_ingredients=[[1], [2]],  # [[1,5,40,42,30,100], [1,3,2], [50, 101, 2, 3, 23,41, 12]],
            m_disliked_ingredients=[20, 201],
            m_p_min_tags=0.7,
            m_p_max_ingredients=0.7
        )
        '''
                    m_ingredients=[
                        ["rice", "pumpkin", "potato", "soy sauce", "salt", "pepper", "pepperoni", "cilantro"],
                        ["noodles", "tomatoes", "garlic", "olive oil", "salt", "pepper", "parmigano"],
                        ["paprika","rice", "minced meat", "onions"]],
                    m_disliked_ingredients=["pork belly", "peanuts"],
                    m_tags=["indian", "healthy", "carbs", "chinese", "pork"],
                    '''
    elif testnumber == 2:
        createRecipyBase()
    elif testnumber == 3:
        dataframe, ingredient_dictionary, nu
        mber_ingredients, tag_dictionary, tag_number = createRecipyBase()
        i_matrix = createMatrix(dataframe, "ingredients_keys", number_ingredients)
        t_matrix = createMatrix(dataframe, "tags_keys", tag_number)


        rev_tag_dictionary = {item: key for key, item in tag_dictionary.items()}
        rev_ing_dictionary = {item: key for key, item in ingredient_dictionary.items()}
        t1 = ['60-minutes-or-less', 'time-to-make', 'course', 'main-ingredient', 'cuisine', 'preparation', 'occasion', 'north-american', 'side-dishes', 'vegetables', 'mexican', 'easy', 'fall', 'holiday-event', 'vegetarian', 'winter', 'dietary', 'christmas', 'seasonal', 'squash']
        t2 = ['30-minutes-or-less', 'time-to-make', 'course', 'main-ingredient', 'cuisine', 'preparation', 'occasion', 'north-american', 'breakfast', 'main-dish', 'pork', 'american', 'oven', 'easy', 'kid-friendly', 'pizza', 'dietary', 'northeastern-united-states', 'meat', 'equipment']
        t3 = ['time-to-make', 'course', 'preparation', 'main-dish', 'chili', 'crock-pot-slow-cooker', 'dietary', 'equipment', '4-hours-or-less']
        t4 = ['60-minutes-or-less', 'time-to-make', 'course', 'main-ingredient', 'preparation', 'occasion', 'side-dishes', 'eggs-dairy', 'potatoes', 'vegetables', 'oven', 'easy', 'dinner-party', 'holiday-event', 'easter', 'cheese', 'stove-top', 'dietary', 'christmas', 'new-years', 'thanksgiving', 'independence-day', 'st-patricks-day', 'valentines-day', 'inexpensive', 'brunch', 'superbowl', 'equipment', 'presentation', 'served-hot']
        t = list(set(t1+t2+t3+t4))
        i1 = ['winter squash', 'mexican seasoning', 'mixed spice', 'honey', 'butter', 'olive oil', 'salt']
        i2 = ['prepared pizza crust', 'sausage patty', 'eggs', 'milk', 'salt and pepper', 'cheese']
        i3 = ['ground beef', 'yellow onions', 'diced tomatoes', 'tomato paste', 'tomato soup', 'rotel tomatoes', 'kidney beans', 'water', 'chili powder', 'ground cumin', 'salt', 'lettuce', 'cheddar cheese']
        i4 = ['spreadable cheese with garlic and herbs', 'new potatoes', 'shallots', 'parsley', 'tarragon', 'olive oil', 'red wine vinegar', 'salt', 'pepper', 'red bell pepper', 'yellow bell pepper']
        i1 = [rev_ing_dictionary[key] for key in i1]
        i2 = [rev_ing_dictionary[key] for key in i2]
        i3 = [rev_ing_dictionary[key] for key in i3]
        i4 = [rev_ing_dictionary[key] for key in i4]
        i = [i1,i2,i3,i4]
        t = [rev_tag_dictionary[key] for key in t]


        reccomendations = getRecomendations(
            m_number=10,
            m_tags= t, #[20, 1, 23, 3, 35, 48, 60, 12, 2,4,32,43,53,32,200,34,300,349,343,23,24,25,26],
            m_ingredients= i, #[[20, 1, 23, 3, 35, 48, 60, 12, 2,4,32,43,53,32,200,34,300,349,343,23,24,25,26, 1, 5, 40, 42, 30, 100], [1, 3, 2, 20, 1, 23, 3, 35, 48, 60, 12, 2,4,32,43,53,32,200,34,309,349,343,23,24,25,26], [37,71, 28, 291, 281, 21, 24, 32,33, 34, 35, 36, 37, 51, 55, 52 ,3,50, 101, 2, 3, 23, 41, 12]],
            m_disliked_ingredients=[20, 201],
            m_p_min_tags=0.5,
            m_p_max_ingredients=0.85,
            m_p_min_ingredients=0.3,
            df=dataframe,
            i_matrix=i_matrix,
            t_matrix=t_matrix
        )
    elif testnumber == 4:
        df_ids = getRecepyIDs()
