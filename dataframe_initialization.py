import pandas as pd
from ast import literal_eval
import numpy as np
from recomendations_recepies import getRecomendations

def createMatrix(df, key_column_name, number_matrix_columns):
    matrix = np.zeros((len(df), number_matrix_columns + 1), np.int8)
    for i, row in enumerate(df[key_column_name]):
        for value in row:
            matrix[i, value] = 1
    return matrix


def createKeyColumn(df, column_name):
    # get all ingredients, create keys for them and store keys of all ingredients of one recipy in a new column
    df[column_name] = df[column_name].apply(literal_eval)
    all_values = list(set(df[column_name].explode().tolist()))  # list(set([row for row in df]))
    value_dictionary = {idx + 1: item for idx, item in enumerate(all_values)}
    rev_value_dictionary = {item: key for key, item in value_dictionary.items()}

    def _get_keys(values):
        return [rev_value_dictionary[val] for val in values]

    df[f"{column_name}_keys"] = df[column_name].apply(_get_keys)
    number_values = len(all_values)
    return df, all_values, value_dictionary, number_values


def createRecipyBase():
    # load 1000 rows of csv (restricted due to demonstration purposes)
    df = pd.read_csv('data\RAW_recipes.csv', nrows=1000)

    # get all ingredients, create keys for them and store keys of all ingredients of one recipy in a new column
    df, all_ingredients, ingredient_dictionary, ingredient_number = createKeyColumn(df, "ingredients")
    # do the same for tags
    df, all_tags, tag_dictionary, tag_number = createKeyColumn(df, "tags")

    '''
    print(df["ingredients_keys"].head())
    print(ingredient_dictionary)
    print(all_ingredients)
    print(list(df.columns))
    print(df.dtypes)
    print(max(df.id))
    print(min(df.id))
    '''

    return df, ingredient_dictionary, ingredient_number, tag_dictionary, tag_number


# creates matrices, returns dicitonaries and adds key numbers to df
def intitialize_recipies():
    dataframe, ingredient_dictionary, number_ingredients, tag_dictionary, tag_number = createRecipyBase()
    i_matrix = createMatrix(dataframe, "ingredients_keys", number_ingredients)
    t_matrix = createMatrix(dataframe, "tags_keys", tag_number)

    dataframe.to_csv("data\prepared_recipies.csv")
    return dataframe, i_matrix, t_matrix, ingredient_dictionary, tag_dictionary


if __name__ == "__main__":
    testnumber = 3
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
        dataframe, ingredient_dictionary, number_ingredients, tag_dictionary, tag_number = createRecipyBase()
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
        print("a")
