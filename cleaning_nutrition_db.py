import numpy as np





with open('recipes_no_explication_with_ratings_and_nutrition.csv', 'r', encoding='utf8') as recipes_with_ratings_and_nutrition_data_file:
    names_of_recipes_with_ratings_and_nutrition_data_lines = recipes_with_ratings_and_nutrition_data_file.readlines()
    del names_of_recipes_with_ratings_and_nutrition_data_lines[0]
    


def cleaning_commas_issues_in_titles(data_lines):
    with open('recipes_no_explication_with_ratings_and_nutrition_modified.csv', 'a+', encoding='utf8') as recipes_with_ratings_and_nutrition_data_file:
        for line_index in range(len(data_lines)):
            values_of_line = data_lines[line_index].split(',')
            try:
                should_be_float_value = float(values_of_line[1])
                recipes_with_ratings_and_nutrition_data_file.write(data_lines[line_index])
            except ValueError:
                print("BIIIIIIIIIIIIIIIIIIIIIIIIIIG ERROR")
                del data_lines[line_index]
        
        


        

        
def cleaning_grammar_words_in_title(data_lines):
    with open('recipes_no_explication_with_ratings_and_nutrition_modified.csv', 'w', encoding='utf8') as recipes_with_ratings_and_nutrition_data_file:
        for line in data_lines:
            values_of_line = line.split(',')
            title = values_of_line[0]

            with_bool = 'with' in title or 'With' in title
            and_bool = 'and' in title or 'And' in title
            or_bool = 'or' in title or 'Or' in title
            in_bool = 'in' in title or 'In' in title
            
            if with_bool:
                if 'with' in title:
                    title.replace('with', '')
                if 'With' in title:
                    title.replace('With', '')

            if and_bool:
                if 'and' in title:
                    title.replace('and', '')
                if 'And' in title:
                    title.replace('And', '') 

            if or_bool:
                if 'or' in title:
                    title.replace('or', '')
                if 'Or' in title:
                    title.replace('Or', '')           

            if in_bool:
                if 'in' in title:
                    title.replace('in', '')
                if 'In' in title:
                    title.replace('In', '')

    recipes_with_ratings_and_nutrition_data_file.writelines(data_lines)


def printing_data_lines(data_lines):
    for line in data_lines:
        print(line)



if __name__ == '__main__':
    cleaning_commas_issues_in_titles(names_of_recipes_with_ratings_and_nutrition_data_lines)
    cleaning_grammar_words_in_title(names_of_recipes_with_ratings_and_nutrition_data_lines)

#printing_data_lines(names_of_recipes_with_ratings_and_nutrition_data_lines)