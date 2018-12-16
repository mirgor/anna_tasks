import csv
import sys
from itertools import islice
import pandas as pd

#for i in range(100+1):
#    sys.stdout.write(('='*i)+(''*(100-i))+("\r [ %d"%i+"% ] "))
#    sys.stdout.flush()
# comment

def read_ratings1():
    print("Input the minimal rating, please: ")
    rating = input()
    print("Input the minimal number of votes(from 100000): ")
    votes = input()
    with open('title.ratings1.tsv', 'r') as f:
        next(f) # skip headings
        reader = csv.reader(f, delimiter='\t')
        num = 0
        film_code_set = set()
        for line in reader:
            if float(line[1]) > int(rating):
                if int(line[2]) > int(votes):
                    film_code_set.add(line[0])
                    num += 1
        print(film_code_set)
        print(num)
        return [num, film_code_set]


def read_principals1(num, film_code_set):
    # print(num)
    with open('title.principals1.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        n = 0
        set_with_actors = set()
        for line in reader:
            if line[0] in film_code_set:
                if line[3] == "actor" or line[3] == "actress":
                    # show progress
                    sys.stdout.write(('.'*(n//10))+("\r Num of actors: [ %d"%n+" ] "))
                    sys.stdout.flush()
                    set_with_actors.add(line[2])
                    n += 1
    lst_with_actors = list(set_with_actors)
    print("\n Num of actors:", n)
    print(set_with_actors)
    return [n, set_with_actors, lst_with_actors]


def make_actors_dict(n, set_with_actors, lst_with_actors):
    with open('title.principals1.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        actor_films_dict = dict()
        temp_lst = []
        for line in reader:
            if line[2] in set_with_actors:
                temp_lst.append(line)
        for i in range(n):
            temp_lst2 = []
            for j in range(len(temp_lst)):
                if temp_lst[j][2] == lst_with_actors[i]:
                    temp_lst2.append(temp_lst[j][0])
            actor_films_dict[lst_with_actors[i]] = temp_lst2
    print(actor_films_dict)
    return actor_films_dict

#================ true code started from here =============================
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

# let full info about movie by film_code
def get_films_info(film_code_lst, start_line = 0):
    n = 0
    count = 0
    film_info = dict()
    film_raiting = dict()
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
                film_info[line[0]]['genres'] = line[8] if line[5] != '\\N' else 0
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

# --------------------------
# main()
# --------------------------
#actors_dict_fin()
#get_all_films_with_actor('nm0606487')


all_film_raiting = dict()

all_film_codes_by_actor = list()
all_film_info_by_actor = dict()

#all_film_codes_by_actor = get_film_codes_by_actor ('nm0606487')
actor_code = 'nm0000138'
all_film_codes_by_actor = get_film_codes_by_actor (actor_code)
#print(get_film_info('tt0021885'))
all_film_info_by_actor = get_films_info(all_film_codes_by_actor)

print(all_film_info_by_actor)
actor_dinamo_data = get_df_year_film(all_film_info_by_actor)
actorinfo = actor_info(actor_code)
actor_dinamo_data.to_csv(actorinfo['id'] + "-" + actorinfo['primaryName'].replace(" ", "_") + ".tsv", sep='\t', encoding='utf-8')