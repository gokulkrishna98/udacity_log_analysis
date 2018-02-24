#!/usr/bin/python
import psycopg2
import operator


def populararticles():
    """function to print the top 3 articles !!!"""
    # connecting to database
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    '''
    selecting path and getting the final file and counting it,
    grouping by final file and
    making sure the view was successfull and ordering it in
    descending order;
    '''
    c.execute("""select articles.title,articlecount.count from articlecount
                inner join articles on upper(articles.title)
                like concat('%',upper(pathtitle),'%') limit 3;""")
    name = c.fetchall()

    for i in name:
        printstring = "%s - %ld" % (i[0], i[1])
        print(printstring)

    db.close()
    return


def popularauthors():
    """function to order authors by popularity"""
    # connencting to database .....
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    sqlcommand = """select name,sum(count) as scount from authorcount,authors
                     where authors.id = authorcount.author
                     group by name
                     order by scount desc;"""

    c.execute(sqlcommand)
    authordetails = c.fetchall()

    for i in authordetails:
        details = "%s - %s" % (i[0], i[1])
        print(details)

    return


def errorcount():
    """function to display date with more than 1.1% error"""
    # connecting to database
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    # selecting date from time and counting article views with no error and
    # grouping and ordering by dates

    c.execute("""select to_char(time::timestamp::date,'Mon dd,yyyy') as dates,
                count((select status where status = '200 OK')) as success,
                count((select status where status != '200 OK')) as error
                from log group by dates order
                by dates;""")
    # getting it to an object
    viewdata = c.fetchall()
    # selecting date from time and counting article views with error and
    # grouping and ordering by dates
    for i in viewdata:
        # calculating error percentage for each date
        a = float(i[2])
        b = float(i[1])
        errorpercent = (a / (a + b)) * 100

        # displaying date with more than 1.1% error percentage
        if errorpercent > 1.1:
            print("%s - %f" % (i[0], errorpercent))


def main():
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


if __name__ == "__main__":
    main()
