# Log Analysis Project
A Python program that generates a report from a news website's database.

## Aspects analyzed
1. **What are the most popular three articles of all time?** Which articles have been accessed the most?
2. **Who are the most popular article authors of all time?** That is, when you sum up all of the articles each author has written, which authors get the most page views?
3. **On which days did more than 1% of requests lead to errors?**  On which days, if any, have the errors amounted to more than 1% of total requests?

## Running the program
Follow the steps below to run the program and generate the report:
#### Set up
1. Install [Vagrant](https://www.vagrantup.com/downloads.html)
1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
1. Download the Vagrant setup files from [Udacity's Github](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f73b_vagrantfile/vagrantfile)
1. Download the database: [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
1. Place the newsdata.sql file in the same directory as your vagrant file
1. Place [these files](www.github.com/pperone) in the same directory

#### Run
1. Open a terminal and cd to the vagrant directory
1. Run ``` vagrant up ``` to build the VM for the first time
1. Run ``` vagrant ssh ``` to connect
1. Enter ``` psql -d news -f newsdata.sql ```
1. Run ``` python Report.py ```

## Expected Output:

<pre>
LOG ANALYSIS - NEWS SITE
-------------------------------------------------------------


1. What are the most popular three articles of all time?
"Candidate is jerk, alleges rival" - 338647 views
"Bears love berries, alleges bear" - 253801 views
"Bad things gone, say good people" - 170098 views


2. Who are the most popular article authors of all time?
Ursula La Multa - 507594 views
Rudolf von Treppenwitz - 423457 views
Anonymous Contributor - 170098 views
Markoff Chaney - 84557 views


3. On which days did more than 1% of requests lead to errors?
July 17, 2016 - 2.3% errors
</pre>

## SQL Views
Two views were created. The goal was to simplify the final queries, and avoid repetition, since they were used in more than one query. They were the following:
#### trimmedpaths
It creates a table containing the paths without the leading "/article/":
<pre>
create view trimmedpaths as SELECT right(path, length(path) - 9), hits FROM (select path, count(\*) as hits from log where status like '200 OK' group by path) pathhits;
</pre>
#### authorsviews
It creates a table containing all authors and their respective article views:
<pre>
create view authorsviews as select name, hits from (select name, title from authors, articles where authors.id = articles.author) as authorarticles, (select title, hits from (select title, slug from articles) as titleslug, trimmedpaths where titleslug.slug = trimmedpaths.right) as titlesviews where authorarticles.title = titlesviews.title;
</pre>
