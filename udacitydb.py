#!/usr/bin/python
import psycopg2
import operator

# function to print the top 3 articles


def populararticles():
    # connecting to database
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    '''
    selecting path and getting the final file and counting it,
    grouping by final file and
    making sure the view was successfull and ordering it in
    descending order;
    '''
    c.execute("""select split_part(path,'/',3), count(*)
                as count from log where status like '200 OK'
                group by path
                order by count desc;""")
    name = c.fetchall()

    # replacing - witn <space> and checking it in titles article
    # to get the title name of articles
    for i in range(1, 4):

        articlepath = name[i][0].replace("-", " ")
        end = len(articlepath)
        s = "select title from articles where title like '%"
        + articlepath[1:end] + "%'"
        c.execute(s)
        new = c.fetchall()

        # printing title and its view count
        print('%s - %d' % (new[0][0], name[i][1]))

    db.close()
    return


# function to order authors by popularity
def popularauthors():

    # connencting to database .....
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # finding relation between authors and articles
    c.execute(""" select articles.author, articles.title from articles,authors
             where articles.author=authors.id""")
    authortitledata = c.fetchall()

    # getting the count of articles
    c.execute("""select split_part(path,'/',3), count(*) as count
                 from log where status like '200 OK'
                group by path
                orderby count desc;""")
    titlecountdata = c.fetchall()

    # flag to avoid first field which is empty
    flag = 0

    # calculation in python

    # index represents author id
    articlesvotes = [0, 0, 0, 0, 0]
    # dictionary for author vote details
    authorvotedetails = {}
    authorname = []
    for i in titlecountdata:
        # avoiding first titlecountdata which is empty
        if flag == 0:
            flag = 1
            continue
        else:
            # comparing articlepath with titles to get author id
            articlepath = i[0].split('-', 3)[2].replace("'", "")
            s = " select author from articles where"+
            +" replace(upper(title),'''','') like upper('%"
            + articlepath + "%')"
            c.execute(sqlcommand)
            authorid = c.fetchall()

            # counting views for author and if error pass it
            try:
                articlesvotes[authorid[0][0]] += i[1]
            except:
                pass
            else:
                pass

    # selecting author name using author id
    for i in range(1, 5):
        sqlcommand = "select name from authors where id = %d" % (i)
        c.execute(sqlcommand)
        authornameraw = c.fetchall()
        # list of author names
        authorname.append(authornameraw[0][0])

    # making dictionary with author name and views
    for i in authorname:
        sqlcommand = "select id from authors where name = '" + i + "'"
        c.execute(sqlcommand)
        authorid = c.fetchall()
        authorvotedetails[i] = articlesvotes[authorid[0][0]]

    # sorting the dictionary by values (i.e. views)
    #pls make exception for pep8 guide
    sortedauthordetails = sorted(authorvotedetails.items(),
                                key=operator.itemgetter(1),
                                reverse=True)

    # printing the details
    for i in sortedauthordetails:
        finalstr = "%s - %s" % (i[0], i[1])
        print(finalstr)
    db.close()
    return


# function to display date with more than 1.1% error
def errorcount():

    # connecting to database
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    '''
    selecting date from time and counting article views with no error and
    grouping and ordering by dates
    '''
    c.execute("""select to_char(time::timestamp::date,'Mon dd,yyyy') as dates,count(*)
                as count from log where status='200 OK' group by dates order
                by dates;""")
    # getting it to an object
    successviewdata = c.fetchall()

    c.execute("""select time::timestamp::date as dates, count(*)
                as count from log where status !='200 OK' group by dates order
                by dates;""")
    errorviewdata = c.fetchall()
    '''
    selecting date from time and counting article views with error and
    grouping and ordering by dates
    '''
    count = 0
    for i in successviewdata:
        # calculating error percentage for each date
        errorpercent = (float(errorviewdata[count][1]) / float(i[1])) * 100

        # displaying date with more than 1.1% error percentage
        if errorpercent > 1.1:
            print("%s - %f" % (i[0], errorpercent))

        count = count+1

# calling respective functions
print("****Top 3 popular articles****")
print("------------------------------\n")
populararticles()
print("\n****Popular authors & their viewcount****")
print("-------------------------------------------\n")
popularauthors()
print("\n")
print("\n****Days with more than 1 percent error****")
print("wait.......\n")
errorcount()
