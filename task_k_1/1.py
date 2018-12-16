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


def actor_info(actor_code):
    actor_info_lst = []
    with open('names.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            if line[0] == actor_code:
                # print(line)
                actor_info_lst.append(line[1])
                actor_info_lst.append(line[2])
                if line[3] == "\\N":
                    actor_info_lst.append("null")
                else:
                    actor_info_lst.append(line[3])
                break
    print(actor_info_lst) #['John Denver', '1943', '1997']
    return actor_info_lst

#================ true code started from here =============================

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
def get_film_raiting(film_code, from_file = 0):
    if from_file == 1:
        n = 0
        film_raiting = dict()

        with open('title.ratings1.tsv', 'r', encoding="utf-8") as f:
            next(f)
            reader = csv.reader(f, delimiter='\t')
            for line in reader:
                if line[0] == film_code:
                    film_raiting['averageRating'] = float(line[1])
                    film_raiting['numVotes'] = int(line[2])
                    break
                # show progress
                sys.stdout.write("\r Searching film: [ %d"%n+" ] ")
                sys.stdout.flush()
                n+=1
    
    else:
        if len(all_film_raiting.keys()) <= 0:
            set_dict_all_film_raiting() 
            
        film_raiting = all_film_raiting[film_code]
    print("get_film_raiting log :", film_raiting)
    return film_raiting

# let full info about movie by film_code
def get_film_info(film_code):
    n = 0
    start_line = int(film_code[2:]) - 1000 #todo optimize  -value
    if start_line < 0 :
        start_line = 0   
    film_info = dict()
    
    with open('title.basics1.tsv', 'r', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(islice(f, start_line, None), delimiter='\t')
        for line in reader:
            #print("log film_info:", line[0], start_line)
            if line[0] == film_code:
                film_info[film_code] = dict()
                film_info[film_code]['startYear'] = int(line[5])
                film_info[film_code]['primaryTitle'] = line[2]
                film_info[film_code]['originalTitle'] = line[3]
                film_info[film_code]['genres'] = line[8]
                film_raiting = get_film_raiting(film_code)
                film_info[film_code]['averageRating'] = film_raiting['averageRating']
                film_info[film_code]['numVotes'] = film_raiting['numVotes']
                break
            # show progress
            sys.stdout.write("\r Searching film " + film_code + ": [ %d"%n + " " + line[0] +" ] ")
            sys.stdout.flush()
            n+=1
            if int(line[0][2:]) > int(film_code[2:]):
                break
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
all_film_codes_by_actor = get_film_codes_by_actor ('nm0000022')
#print(get_film_info('tt0021885'))
for elem in all_film_codes_by_actor:
    temp_dct = get_film_info(elem)
    if temp_dct != 0:
        print(temp_dct)
        all_film_info_by_actor[elem] = temp_dct[elem]
print(all_film_info_by_actor)
actor_dinamo_data = get_df_year_film(all_film_info_by_actor)