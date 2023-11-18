import pandas as pd
from ast import literal_eval
import numpy as np

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
    np.save("data/i_matrix.npy", i_matrix)
    np.save("data/t_matrix.npy", t_matrix)
    np.save("data/i_dict.npy", ingredient_dictionary)
    np.save("data/t_dict.npy", tag_dictionary)
    return dataframe, i_matrix, t_matrix, ingredient_dictionary, tag_dictionary


if __name__ == "__main__":
    testnumber = 1
    if testnumber == 1:
        intitialize_recipies()
    elif testnumber == 2:
        createRecipyBase()
    elif testnumber == 3:
        dataframe, ingredient_dictionary, number_ingredients, tag_dictionary, tag_number = createRecipyBase()
        i_matrix = createMatrix(dataframe, "ingredients_keys", number_ingredients)
        t_matrix = createMatrix(dataframe, "tags_keys", tag_number)


