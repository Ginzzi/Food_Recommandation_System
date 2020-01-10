from problem_data import * 




def show_nbr_ratings():
    """
        Show the number of occurences in the data for all of the ratings
    """
    nbrs = [0,0,0,0,0]
    for rating in dataframe_ratings:
        if rating == 1:
            nbrs[0] += 1
        elif rating == 2:
            nbrs[1] += 1
        elif rating == 3:
            nbrs[2] += 1
        elif rating == 4:
            nbrs[3] += 1
        elif rating == 5:
            nbrs[4] += 1
    print(nbrs)
    return nbrs




def equilibrate_data_for_ratings():
    nbrs = show_nbr_ratings()
    while nbrs[2] > 700 and nbrs[3] > 700 and nbrs[4] > 700:
        for i, line in enumerate(dataframe.values):
            if line[1] == 3 and nbrs[2] > 700:
                dataframe.drop(i)
                nbrs[2] -= 1
                print(nbrs)
            elif line[1] == 4 and nbrs[3] > 700:
                dataframe.drop(i)
                nbrs[3] -= 1
                print(nbrs)
            elif line[1] == 5 and nbrs[4] > 700:
                dataframe.drop(i)
                nbrs[4] -= 1
                print(nbrs)
    return dataframe


def sigmoid(x):
    return 1/(1 + np.exp(-x))

def sigmoid_prime(x):
    ones = np.ones((x.shape[0], 1))
    return product(sigmoid(x), ones-sigmoid(x))


def product(z, mat):
    result = []
    for i, row in enumerate(z):
        result.append(mat[i] * row)
    return mat

def softmax(z):
    p = []
    for i in range(len(z)):
        p.append(np.exp(z[i])/(sum(np.exp(z))))
    return p

def condition_on_y(y):
    for i, yi in enumerate(y):
        if yi < 1e-40 or math.isnan(yi):
            y[i] = 1e-40
    return y


def create_apriori_data(dataframe):
    data = []
    for i in range(len(dataframe)):
        data.append(list_of_ingredients_in_recipe_index(i))

def list_of_ingredients_in_recipe(title_recipe):
    """ 
    Returns a list containing all of the "ingredients" in a
    specific recipe
    """
    list_of_ingredients = []
    dataline = dataframe[dataframe['title'].str.match(title_recipe)]
    for elem in dataline:
        for value in dataline[elem]:
            if isinstance(value, str):
                pass
            elif isinstance(value, float):
                if value == 1.0:
                    list_of_ingredients.append(elem)
    return list_of_ingredients



def list_of_ingredients_in_recipe_index(index_recipe):
    """ 
    Returns a list containing all of the "ingredients" in a
    specific recipe
    """
    list_of_ingredients = []
    dataline = dataframe.iloc[[index_recipe]]
    for elem in dataline:
        for value in dataline[elem]:
            if isinstance(value, str):
                pass
            elif isinstance(value, float):
                if value == 1.0:
                    list_of_ingredients.append(elem)
    return list_of_ingredients


def total_list_of_ingredients():
    """ 
    We print all of the "ingredients" present in the dataset
    We delete title, rating, calories, protein, fat and sodium columns
    """
    result = list(dataframe.columns.copy())
    result.remove('title')
    result.remove('good_rating')
    result.remove('bad_rating')
    result.remove('calories')
    result.remove('protein')
    result.remove('fat')
    result.remove('sodium')
    
    return result

list_of_ingredients = total_list_of_ingredients()


def is_ingredient_in_recipe(ingredient, title_recipe):
    """
    Return True if the ingredient is in the recipe
           False otherwise
    """
    ingredients_in_recipe = list_of_ingredients_in_recipe(title_recipe)
    return ingredient in ingredients_in_recipe


def get_rating_for_recipe(title_recipe):
    return list(dataframe[dataframe['title'].str.match(title_recipe)]['rating'])[0]

def get_all_fat():
    """
        Returns a list containing all the fat in the several recipes
    """
    fat = []
    for line in dataframe.values:
        if not np.isnan(line[5]):
            fat.append(line[5])
    return fat

def is_fat_in_intervals(fat, intervals):
    result = False
    for interval in intervals:
        if fat >= interval[0] and fat <= interval[1]:
            result = True
            break
    return result

def which_interval_is_fat_in(fat, intervals):
    result = -1
    for i, interval in enumerate(intervals):
         if fat >= interval[0] and fat <= interval[1]:
            result = i
            break
    return result

def get_fat_for_recipe(index_recipe):
    """
        Returns the fat number for a specific recipe
    """
    return dataframe.values[index_recipe][5]

def get_dictionnary_recipes_and_ratings():
    """
    Returns a dictionnary
    Keys -> recipes
    Values -> ratings
    """
    d = {}
    recipes = dataframe['title']
    ratings = dataframe['rating']
    for i, value in enumerate(recipes):
        d.update({value : ratings[i]})
    return d

def get_dictionnary_lists_of_ingredients_and_ratings(dataframe):
    """
    Returns a dictionnary that contains as:
        keys -> title of a recipe
        value -> tuple containing :
            1) A list of binary presence of all the ingredients in the df for the recipe
            2) The rating of the recipe
    """
    d = {}
    for recipe in dataframe[:3].values:
        title_of_recipe = recipe[0]
        rating_of_recipe = recipe[1]
        #print(recipe[0])
        list_of_ingredients_for_recipe = []
        for ingredient_value in recipe[7:]:
            #print(ingredient_value)
            if ingredient_value == 1.0:
                list_of_ingredients_for_recipe.append(1)
            else:
                list_of_ingredients_for_recipe.append(0)
        d.update({title_of_recipe : (list_of_ingredients_for_recipe, rating_of_recipe)})



def get_ingredients_and_ratings_for_index(dataframe, index):
    """
    Returns a tuple that contains as:
        First element :  title of the recipe 
        Second element : A list of binary presence of all the ingredients in the df for the recipe
        Third element :  The rating of the recipe
    """
    d = {}
    recipe = dataframe.values[index]
    title_of_recipe = recipe[0]
    rating_of_recipe = recipe[1]
    #print(recipe[0])
    list_of_ingredients_for_recipe = []
    for ingredient_value in recipe[6:]:
        #print(ingredient_value)
        if ingredient_value == 1.0:
            list_of_ingredients_for_recipe.append(1)
        else:
            list_of_ingredients_for_recipe.append(0)
    return (title_of_recipe, list_of_ingredients_for_recipe, rating_of_recipe)



def get_ingredients_and_fat_for_index(dataframe, index):
    """
    Returns a tuple that contains as:
        First element :  title of the recipe 
        Second element : A list of binary presence of all the ingredients in the df for the recipe
        Third element :  The rating of the recipe
    """
    d = {}
    recipe = dataframe.values[index]
    title_of_recipe = recipe[0]
    fat_of_recipe = recipe[5]
    #print(recipe[0])
    list_of_ingredients_for_recipe = []
    for ingredient_value in recipe[6:]:
        #print(ingredient_value)
        if ingredient_value == 1.0:
            list_of_ingredients_for_recipe.append(1)
        else:
            list_of_ingredients_for_recipe.append(0)
    return (title_of_recipe, list_of_ingredients_for_recipe, fat_of_recipe)





data = pd.read_csv("recipes_no_explication_with_ratings_and_nutrition_modified.csv")
dataframe = pd.DataFrame(data)
#dataframe_ratings = list(dataframe['good_rating'])
#dataframe = equilibrate_data_for_ratings()
dataframe_ratings = list(dataframe['good_rating'])
show_nbr_ratings()
datalines = dataframe.values



max_dataframe_ratings = max(dataframe_ratings)
min_dataframe_ratings = min(dataframe_ratings)
variance_dataframe_ratings = np.var(dataframe_ratings)
mean_dataframe_ratings = np.mean(dataframe_ratings)


    
