import csv
import sys
from itertools import islice
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def actor_info(actor_code):
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
    print(actor_info_dict) #['John Denver', '1943', '1997']
    return actor_info_dict

def set_dict_all_film_raiting(): 
    with open('title.ratings1.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            all_film_raiting[line[0]] = {'averageRating':float(line[1]), 'numVotes':int(line[2])}
    if len(all_film_raiting.keys()) > 0:
        return len(all_film_raiting.keys())
    else:
        return 0

# let raiting by film_code as {float('averageRating'), int('numVotes')}
def get_film_raiting(film_code, from_file = 0, start_line = 0):
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
                n+=1
                if int(film_code[2:]) < int(line[0][2:]):
                    break 
    else:
        if len(all_film_raiting.keys()) <= 0:
            set_dict_all_film_raiting() 
        if film_code in all_film_raiting:
            film_raiting = all_film_raiting[film_code]
    print("get_film_raiting log :", film_raiting)
    return film_raiting


def set_all_films_info(): 
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
                    count+=1
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
    print("get_films_info log :", film_info)            
                       
    if len(film_info.keys()) <= 0:
        return 0
    else:
        #    print("get_film_info log " , film_info, n)
        return film_info
        
def get_film_codes_by_actor(actor_code):
    with open('title.principals1.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        temp_lst = []
        n = 0
        for line in reader:
            if line[2] == actor_code and (line[3] == 'actor' or line[3] == 'actress'):
                # show progress
                sys.stdout.write(('.'*(n//10))+("\r Num films: [ %d"%n+" ] "))
                sys.stdout.flush()
                temp_lst.append(line[0])
                n+=1
        print("\n Num of films with actor:", n)
        print(temp_lst)
    if len(temp_lst) > 0:
        return temp_lst
    else:
        return 0

def get_df_year_film(all_film_info_by_actor_dict):
    strYear = ''
    valYear = 0
    result = dict()    
    
    for key, val in all_film_info_by_actor_dict.items():
        strYear = val['startYear']
        valYear = int(strYear)
        print(strYear, valYear, val['averageRating'],val['numVotes'])
        
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
        
#    [startYear, count_movies, summary_rating, summary_votes, avg_rating]
    return pd.DataFrame(df_year_film)


def get_data_by_author(actor_code):
    #work with actor
    #actor_code = 'nm0000138'
    actorinfo = actor_info(actor_code)
    
    all_film_codes_by_actor = list()
    all_film_info_by_actor = dict()
    all_film_codes_by_actor = get_film_codes_by_actor (actor_code)
    
    all_film_info_by_actor = get_films_info(all_film_codes_by_actor)
    
    actor_dinamo_data = get_df_year_film(all_film_info_by_actor)
    
    #read actor_dinamo_data from file
    #actor_dinamo_data = pd.read_csv(actorinfo['id'] + "-" + actorinfo['primaryName'].replace(" ", "_") + ".tsv", sep='\t', encoding='utf-8')
    
    #set age values in actor_dinamo_data
    for ind in actor_dinamo_data.index:
        actor_dinamo_data['age_actor'][ind] = actor_dinamo_data['year'][ind] - int(actorinfo['birthYear'])
        print (actor_dinamo_data['year'][ind], actor_dinamo_data['age_actor'][ind])    
    actor_dinamo_data = actor_dinamo_data.sort_values(by=['year']) 
    actor_dinamo_data.to_csv(actorinfo['id'] + "-" + actorinfo['primaryName'].replace(" ", "_") + ".tsv", sep='\t', encoding='utf-8')
    plot_actors_dinamo(actor_dinamo_data, actorinfo)
    
    
def plot_actors_dinamo(actor_dinamo_data, actorinfo):
    # Data for plotting

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


# --------------------------
# main()
# --------------------------

#create common data-cache
all_film_raiting = dict()
all_films_info = dict()

autors_list = ['nm0000255', 'nm0000242', 'nm0000354', 
               'nm0000142', 'nm0000158', 'nm0000163', 
               'nm0000195', 'nm0000047', 'nm0000098', 
               'nm0000139', 'nm0000170', 'nm0000182', 
               'nm0000193', 'nm0000213', 'nm0000136', 
               'nm0000235', 'nm0000226', 'nm0000138']

i = 0
while i < len(autors_list):
    get_data_by_author(autors_list[i])
    i += 1
