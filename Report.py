#!/usr/bin/python

import psycopg2

database = "news"
db = psycopg2.connect(database=database)
c = db.cursor()

c.execute(
          "create view trimmedpaths as SELECT right(path, length(path) - 9), "
          "hits FROM (select path, count(*) as hits from log where status "
          "like'200 OK' group by path) pathhits")
c.execute("create view authorsviews as select name, hits from (select name, "
          "title from authors, articles where authors.id = articles.author) "
          "as authorarticles, (select title, hits from (select title, slug "
          "from articles) as titleslug, trimmedpaths where titleslug.slug = "
          "trimmedpaths.right) as titlesviews where authorarticles.title = "
          "titlesviews.title")
c.execute("select title, hits from (select title, slug from articles) as "
          "titleslug, trimmedpaths where titleslug.slug = trimmedpaths.right "
          "order by hits desc limit 3")

result = c.fetchall()

print("\n")
print("LOG ANALYSIS - NEWS SITE")
print("-------------------------------------------------------------")
print("\n")
print("1. What are the most popular three articles of all time?")
for row in result:
    print("\"" + row[0] + "\"" + " - " + str(row[1]) + " views")
print("\n")

c.execute(
          "select name, sum(hits) from authorsviews group by name order by sum "
          "desc")

result = c.fetchall()

print("2. Who are the most popular article authors of all time?")
for row in result:
    print(row[0] + " - " + str(row[1]) + " views")
print("\n")

c.execute(
          "select dateok.date, (cast(datefail.count as float) / dateok.count) "
          "as rate from (select date(time), count(*) from log where status "
          "like '200 OK' group by date) as dateok, (select date(time), "
          "count(*) from log where status not like '200 OK' group by date) as "
          "datefail where dateok.date = datefail.date and cast(datefail.count "
          "as float) / dateok.count >= 0.01")

result = c.fetchall()

print("3. On which days did more than 1% of requests lead to errors?")
for row in result:
    date = row[0].strftime('%B %d, %Y')
    errors = str(round(row[1] * 100, 1))
    print(date + " - " + errors + "% errors")
print("\n")

db.close()
