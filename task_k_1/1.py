import csv
import sys
from itertools import islice

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

def year_film(actor_code, year, actor_films_dict):
    count_movies = 0
    summary_rating = 0.0
    summary_votes = 0.0
    avg_rating = 0.0

    temp_lst = actor_films_dict[actor_code]
    print(temp_lst) #['tt0104748', 'tt0114323', 'tt0117592',...]
    basics_lst = []
    rating_lst = []
    with open('title.basics1.tsv', 'r', encoding='utf-8') as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            if line[0] in temp_lst:
                basics_lst.append(line)
    # print('basics_lst:', basics_lst)

    with open('title.ratings1.tsv', 'r', encoding='utf-8') as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            if line[0] in temp_lst:
                rating_lst.append(line)

    for i in range(len(basics_lst)):
        if int(basics_lst[i][4]) == int(year):
            if basics_lst[i][5] == "\\N":
                summary_rating += float(rating_lst[i][1])
                count_movies += 1
                summary_votes += float(rating_lst[i][2])

        elif basics_lst[i][5] != "\\N":
            if int(basics_lst[i][5]) == int(year):
                summary_rating += float(rating_lst[i][1])
                count_movies += 1
                summary_votes += float(rating_lst[i][2])

    if count_movies == 0:
        avg_rating = 0
    else:
        avg_rating = summary_rating / count_movies

    # print('rating_lst:', rating_lst)
    # print('temp_lst:', temp_lst)
    # print('count_movies = ', count_movies)
    # print('summary_rating = ', summary_rating)
    # print('summary_votes = ', summary_votes)
    # print("avg_rating = ", avg_rating)

    return [count_movies, summary_rating, summary_votes, avg_rating]

    # for j in range(len(basics_lst)):
    #     if basics_lst[j][5] == year:
    #         count_movies += 1
    #         summary_rating += basics_lst[j][]

    # print(basics_lst)


def all_about_actor(actor_code):
    main_dict = dict()
    actor_info_lst = actor_info(actor_code)
    actor_films_dict = actors_dict_fin()
    if actor_info_lst[2] == 'null':
        actor_age = 2018 - int(actor_info_lst[1])
    else:
        actor_age = int(actor_info_lst[2]) - int(actor_info_lst[1])
    print(actor_info_lst, actor_age)
    lst_of_movies = []
    for i in range(int(actor_info_lst[1]), int(actor_info_lst[1]) + actor_age + 1):
        # print(i)
        lst_of_movies.append(year_film(actor_code, i, actor_films_dict))
        # print(year_film(actor_code, i))
    main_dict['actor_code'] = actor_code
    main_dict['actor_name'] = actor_info_lst[0]
    main_dict['birth_year'] = actor_info_lst[1]
    main_dict['death_year'] = actor_info_lst[2]
    main_dict['data'] = lst_of_movies

    print(main_dict)
    return main_dict

#-> {actor_code: "nn...." , 
#    actor_name: "Taylor Glen", 
#    birth_year: 2000, 
#    death_year: null, 
#    data: [
#       [рік, count movies, summary raiting, summary votes, avg rating],
#       [рік, count movies, summary raiting, summary votes, avg rating]
#   ]}


def actors_dict_fin():
    temp_lst = read_ratings1()
    num = temp_lst[0]
    film_code_set = temp_lst[1]
    temp_lst2 = read_principals1(num, film_code_set)
    n, set_with_actors, lst_with_actors = int(temp_lst2[0]), temp_lst2[1], temp_lst2[2]
    actors_dict = make_actors_dict(n, set_with_actors, lst_with_actors)
    return actors_dict

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
#print(get_film_raiting('tt0000041'))
#print(set_dict_all_film_raiting())
#year_film('nm0606487', 2013)

# actor_info('nm0666739')
# all_about_actor('nm0666739')

