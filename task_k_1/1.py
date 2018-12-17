import csv
import sys
from itertools import islice
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def ask_user_for_actorslist():
    '''

    Scan users input(code or codes of actors separated with coma) and return a list of actor codes.

    :return: e.g. ['nm0000255', 'nm0000242']

    '''

    lst = input("Enter the codes of actors separated by coma & space, please.\nFor example:  nm0000255, nm0000242\n:")
    if lst != '': 
        lst = lst.split(", ")
    else:
        lst = []
    return lst

def actor_info(actor_code):
    '''

    Gets actor code and return the dictionary with keys: id, primaryName, birthDay, deathYear.

    :param actor_code: 'nm0004266'
    :return: {'id': 'nm0004266', 'primaryName': 'Anne Hathaway', 'birthYear': '1982', 'deathYear': 'null'}

    '''
    actor_info_dict = dict()
    with open('names.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            if line[0] == actor_code:
                actor_info_dict['id'] = actor_code
                actor_info_dict['primaryName'] = line[1] if line[1] != "\\N" else "null"
                actor_info_dict['birthYear'] = line[2] if line[2] != "\\N" else "null"
                actor_info_dict['deathYear'] = line[3] if line[3] != "\\N" else "null"
                break
    return actor_info_dict

def set_dict_all_film_raiting():
    '''
    Read title.ratings1.tsv and add values for each film-code to the dictionary.
    Uses to create common data-cache-dict. Writes the dictionary(keys = film-code)
    of dictionaries(keys = 'averageRating', 'numVotes') to the global variable 'all_film_raiting'.

    :return: 0 or int
    '''
    with open('title.ratings1.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            all_film_raiting[line[0]] = {'averageRating':float(line[1]), 'numVotes':int(line[2])}
    if len(all_film_raiting.keys()) > 0:
        return len(all_film_raiting.keys())
    else:
        return 0


def get_film_raiting(film_code, from_file = 0, start_line = 0):
    '''

    Gets the film code and return the dict of film rating with keys: 'averageRating', 'numVotes'.
    Shows to stdout the progress of film-searching at the moment.

    :param film_code: 'tt0026740'
    :return: {'averageRating': 4.3, 'numVotes': 483}

    '''
    film_raiting = dict()
    if from_file == 1:
        n = 0
    
        with open('title.ratings1.tsv', 'r', encoding="utf-8") as f:
            next(f)
            reader = csv.reader(islice(f, start_line, None), delimiter='\t')
            for line in reader:
                if line[0] == film_code:
                    film_raiting['averageRating'] = float(line[1])
                    film_raiting['numVotes'] = int(line[2])
                    break
                # show progress
                sys.stdout.write("\r Searching film `" + film_code + "`: [ " + line[0] +" ] ")
                sys.stdout.flush()
                n += 1
                if int(film_code[2:]) < int(line[0][2:]):
                    break 
    else:
        if len(all_film_raiting.keys()) <= 0:
            set_dict_all_film_raiting() 
        if film_code in all_film_raiting:
            film_raiting = all_film_raiting[film_code]
    return film_raiting


def set_all_films_info():
    '''

    Read title.basics1.tsv and add values for each film-code to the dictionary.
    Uses to create common data-cache-dict. Writes the dictionary(keys = film-code)
    of dictionaries(keys = 'startYear', 'primaryTitle', 'originalTitle') to the global variable 'all_films_info'.

    :return: 0 or int
    '''

    with open('title.basics1.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            all_films_info[line[0]] = {'startYear':int(line[5]) if line[5] != '\\N' else 0, 
                            'primaryTitle':line[2] if line[2] != '\\N' else 'none',
                            'originalTitle':line[3] if line[3] != '\\N' else 'none'}
            
    if len(all_films_info.keys()) > 0:
        return len(all_films_info.keys())
    else:
        return 0


# let full info about movie by film_code
def get_films_info(film_code_lst, from_file = 0, start_line = 0):
    '''

    Gets film_code_list and return the dictionary(keys = film codes)
    of dictionaries(keys = 'startYear', 'primaryTitle', 'originalTitle', 'averageRating', 'numVotes').
    Shows to stdout the progress of film-searching at the moment.

    :param film_code_lst: ['tt0212662', 'tt0247638']
    :param from_file:
    :param start_line:
    :return: {'tt0212662': {'startYear': 1999, 'primaryTitle': 'Get Real',
             'originalTitle': 'Get Real', 'averageRating': 7.2, 'numVotes': 483},
             'tt0247638': {'startYear': 2001, 'primaryTitle': 'The Princess Diaries',
             'originalTitle': 'The Princess Diaries', 'averageRating': 6.3, 'numVotes': 112474}}

    '''

    n = 0
    count = 0
    film_info = dict()
    film_raiting = dict()
    if from_file == 1:
        with open('title.basics1.tsv', 'r', encoding="utf-8") as f:
            next(f)
            reader = csv.reader(islice(f, start_line, None), delimiter='\t')
            for line in reader:
                if line[0] in film_code_lst:
                    count += 1
                    film_info[line[0]] = dict()
                    film_info[line[0]]['startYear'] = int(line[5]) if line[5] != '\\N' else 0
                    film_info[line[0]]['primaryTitle'] = line[2] if line[2] != '\\N' else 'none'
                    film_info[line[0]]['originalTitle'] = line[3] if line[3] != '\\N' else 'none'
                    film_raiting = get_film_raiting(line[0])
                    if len(film_raiting.keys()) > 0:
                        film_info[line[0]]['averageRating'] = film_raiting['averageRating']
                        film_info[line[0]]['numVotes'] = film_raiting['numVotes']
                    else:
                        del film_info[line[0]]
                        continue
                    if len(film_info.keys()) < count:
                        break
                # show progress
                sys.stdout.write("\r Searching film #" + str(count) + ": [ %d"%n + " " + line[0] +" ] ")
                sys.stdout.flush()
                n+=1
    else:
        if len(all_films_info.keys()) <= 0:
            set_all_films_info() 
        i = 0
        while i < len(film_code_lst):
            film_code = film_code_lst[i]
            i += 1
            film_info[film_code] = dict()
            film_info[film_code]['startYear'] = all_films_info[film_code]['startYear']
            film_info[film_code]['primaryTitle'] = all_films_info[film_code]['primaryTitle']
            film_info[film_code]['originalTitle'] = all_films_info[film_code]['originalTitle']
            film_raiting = get_film_raiting(film_code)
            if len(film_raiting.keys()) > 0:
                film_info[film_code]['averageRating'] = film_raiting['averageRating']
                film_info[film_code]['numVotes'] = film_raiting['numVotes']
            else:
                del film_info[film_code]
                continue
            if len(film_info.keys()) < count:
                break
    if len(film_info.keys()) <= 0:
        return 0
    else:
        return film_info
        
def get_film_codes_by_actor(actor_code):
    '''

    Gets the actor_code and return the list of films with this actor.

    :param actor_code: 'nm0000117'
    :return:['tt0103384', 'tt0109220', 'tt0113699', 'tt0115820', 'tt0115963'...]

    '''
    actorinfo = actor_info(actor_code)

    with open('title.principals1.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        temp_lst = []
        n = 0
        for line in reader:
            if line[2] == actor_code and (line[3] == 'actor' or line[3] == 'actress'):
                # show progress
                sys.stdout.write("\r " + actorinfo['primaryName'] + " [ " + actorinfo['id'] + " ] Num films:  %d"%n)
                sys.stdout.flush()
                temp_lst.append(line[0])
                n+=1
    sys.stdout.write("\r \r\n")
    if len(temp_lst) > 0:
        return temp_lst
    else:
        return 0

def get_df_year_film(all_film_info_by_actor_dict):
    '''
    Gets the dictionary of all_film_info_by_actor and return the Pandas DataFrame.

    :param all_film_info_by_actor_dict: {'tt0212662': {'startYear': 1999, 'primaryTitle': 'Get Real',
                                        'originalTitle': 'Get Real', 'averageRating': 7.2, 'numVotes': 483}

    :return: e.g.       age_actor	avg_rating	count_movies	summary_rating	summary_votes	year
                    0	18	5.2	1	5.2	28	1952
                    1	19	5.6	4	22.4	347	1953
                    2	20	6.0857142857142845	7	42.6	3639	1954
                    ...

    '''

    strYear = ''
    valYear = 0
    result = dict()    
    
    for key, val in all_film_info_by_actor_dict.items():
        strYear = val['startYear']
        valYear = int(strYear)
        
        if strYear in result:
            result[strYear]['summary_rating'] += val['averageRating']
            result[strYear]['summary_votes'] += val['numVotes']
            result[strYear]['count_movies'] += 1
        else:
            result[strYear] = dict()
            result[strYear]['year'] = valYear
            result[strYear]['summary_rating'] = val['averageRating']
            result[strYear]['summary_votes'] = val['numVotes']
            result[strYear]['count_movies'] = 1
            result[strYear]['avg_rating'] = 0
            result[strYear]['age_actor'] = 0
    
    df_year_film = dict()
    df_year_film['year'] = []
    df_year_film['summary_rating'] = []
    df_year_film['summary_votes'] = []
    df_year_film['count_movies'] = []
    df_year_film['avg_rating'] = []
    df_year_film['age_actor'] = []
    
    for key, val in result.items():
        val['avg_rating'] =  float(val['summary_rating']) /  int(val['count_movies'])
        df_year_film['year'].append(val['year'])
        df_year_film['summary_rating'].append(val['summary_rating'])
        df_year_film['summary_votes'].append(val['summary_votes'])
        df_year_film['count_movies'].append(val['count_movies'])
        df_year_film['avg_rating'].append(val['avg_rating'])
        df_year_film['age_actor'].append(val['age_actor'])

    return pd.DataFrame(df_year_film)


def get_data_by_author(actor_code):
    '''

    Gets actor_code, gives it to other functions.
    Connect all functions and run them to represent the result of program.

    :param actor_code: 'nm0000138'

    '''

    actorinfo = actor_info(actor_code)
    
    all_film_codes_by_actor = list()
    all_film_info_by_actor = dict()
    all_film_codes_by_actor = get_film_codes_by_actor (actor_code)
    
    all_film_info_by_actor = get_films_info(all_film_codes_by_actor)
    
    actor_dinamo_data = get_df_year_film(all_film_info_by_actor)

    #set age values in actor_dinamo_data
    for ind in actor_dinamo_data.index:
        actor_dinamo_data['age_actor'][ind] = actor_dinamo_data['year'][ind] - int(actorinfo['birthYear'])
#        print (actor_dinamo_data['year'][ind], actor_dinamo_data['age_actor'][ind])    
    actor_dinamo_data = actor_dinamo_data.sort_values(by=['year']) 
    actor_dinamo_data.to_csv(actorinfo['id'] + "-" + actorinfo['primaryName'].replace(" ", "_") + ".tsv", sep='\t', encoding='utf-8')
    
    plot_actors_dinamo(actor_dinamo_data, actorinfo)
    plot_actors_dinamo_age(actor_dinamo_data, actorinfo)
    plot_actors_dinamo_votes(actor_dinamo_data, actorinfo)
    
def plot_actors_dinamo(actor_dinamo_data, actorinfo):
    '''
    Gets actor_dinamo_data (DataFrame) and actorinfo (dict) from previous functions.
    Makes data for plotting avg_rating & count_movies by movies year. Shows the plot.
    :param actor_dinamo_data:
    :param actorinfo:
    :return: plot

    '''

    x = actor_dinamo_data['year']
    y = actor_dinamo_data['avg_rating']
    y2 = actor_dinamo_data['count_movies']
    
    fig, ax = plt.subplots()
    fig.set_size_inches(11.5, 4.5)
    ax.plot(x, y, color='r', linewidth = 2, alpha = 0.7, antialiased = True)
    ax1 = ax.twinx()
    ax1.bar(x, y2, color='b', alpha = 0.5)
    ax.set(xlabel = 'year', ylabel = 'average rating', title = actorinfo['primaryName'])
    ax1.set_ylabel('count movies')
    ax.grid()
    
    fig.savefig(actorinfo['id'] + "-" + actorinfo['primaryName'].replace(" ", "_") + ".png", dpi=150)
    plt.show()

def plot_actors_dinamo_age(actor_dinamo_data, actorinfo):
    '''

    Gets actor_dinamo_data (DataFrame) and actorinfo (dict) from previous functions.
    Makes data for plotting avg_rating & count_movies by age_actor. Shows the plot.

    :param actor_dinamo_data:
    :param actorinfo:
    :return: plot

    '''

    x = actor_dinamo_data['age_actor']
    y = actor_dinamo_data['avg_rating']
    y2 = actor_dinamo_data['count_movies']
    
    fig, ax = plt.subplots()
    fig.set_size_inches(11.5, 4.5)
    ax.plot(x, y, color='r', linewidth = 2, alpha = 0.7, antialiased = True)
    ax1 = ax.twinx()
    ax1.bar(x, y2, color='g', alpha = 0.5)
    ax.set(xlabel = 'actors age', ylabel = 'average rating', title = actorinfo['primaryName'])
    ax1.set_ylabel('count movies')
    ax.grid()
    
    fig.savefig(actorinfo['id'] + "-" + actorinfo['primaryName'].replace(" ", "_") + "_age.png", dpi=150)
    plt.show()

def plot_actors_dinamo_votes(actor_dinamo_data, actorinfo):
    '''
    Gets actor_dinamo_data (DataFrame) and actorinfo (dict) from previous functions.
    Makes data for plotting avg_rating & count_movies by summary_votes. Shows the plot.

    :param actor_dinamo_data:
    :param actorinfo:
    :return: plot
    '''

    x = actor_dinamo_data['year']
    y = actor_dinamo_data['avg_rating']
    y2 = actor_dinamo_data['summary_votes']

    fig, ax = plt.subplots()
    fig.set_size_inches(11.5, 4.5)
    ax.plot(x, y, color='r', linewidth=2, alpha=0.7, antialiased=True)
    ax1 = ax.twinx()
    ax1.bar(x, y2, color='y', alpha=0.5)
    ax.set(xlabel='year', ylabel='average rating', title=actorinfo['primaryName'])
    ax1.set_ylabel('summary votes')
    ax.grid()

    fig.savefig(actorinfo['id'] + "-" + actorinfo['primaryName'].replace(" ", "_") + "_votes.png", dpi=150)
    plt.show()


# --------------------------
# main()
# --------------------------

# set action
# 0 - make all actions    
# 1 - setup list of specified actors
# 2 - create common data-cache-dicts for title.ratings1.tsv and title.principals1.tsv  
# 3 - make data-files & plots for specified actors
# 4 - read data-files of specified actors and make heatmaps age-actor-avg_rating
    
action_lst = [1, 3]

# show progress
if 0 in action_lst or 1 in action_lst: 
    autors_list = ask_user_for_actorslist()
    if len(autors_list) == 0:
        print("\r You didn`t write any input. Then program will run with demonstrating list of actors.")
        autors_list = ['nm0000255', 'nm0000242']
#        autors_list = ['nm0000255', 'nm0000242', 'nm0000354', 
#                   'nm0000142', 'nm0000158', 'nm0000163', 
#                   'nm0000195', 'nm0000047', 'nm0000098', 
#                   'nm0000139', 'nm0000170', 'nm0000182', 
#                   'nm0000193', 'nm0000213', 'nm0000136', 
#                   'nm0000235', 'nm0000226', 'nm0000138',
#                   'nm0424060', 'nm0004266']

if 0 in action_lst or 2 in action_lst: 
    #create common data-cache-dicts 
    print("\r The programm is running сaching of data now. You can drink a cup of coffe or tea. Keep calm and wait a bit, please...\n")
    all_film_raiting = dict()
    all_films_info = dict()
    set_dict_all_film_raiting()
    set_all_films_info()
    print("\r Thanks for waiting! Caching of files successfully finished.")

if 0 in action_lst or 3 in action_lst: 
    sys.stdout.flush()
    sys.stdout.write("\r The programm is running now. You can drink a cup of coffe or tea. Keep calm and wait a bit, please...\n")
    i = 0
    while i < len(autors_list):
        actorinfo = actor_info(autors_list[i])
        if len(actorinfo.keys()) > 0:
            if actorinfo['birthYear'] != "null":
                get_data_by_author(autors_list[i])
            else:
                print("\r %s haven`t birthYear data. So we passed this actor." % (actorinfo['primaryName'] + " [ " + actorinfo['id'] + " ]\n"))
        i += 1
    print("Thanks for your waiting! Check your current folder, please. There you can find 3 types of plot to make your analysis based on exact data.")
    