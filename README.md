# 291MiniProject2

CMPUT291 - Fall 2015

Mini-Project 2


Due : November 24th at 5pm 


Clarifications:

You are responsible for monitoring the course discussion forum in eclass and this section of the project specification for more details or clarifications. No clarification will be posted after 5pm on November 23rd.

Nov 6, 2015: There is a typo in the description of the file scores.txt. Scores and review ids are separated by a comma (and not a colon). The provided data files are correct. 
Nov 18, 2015: Here is a marking rubric for the project.
Introduction

The goal of this project is to teach the concept of working with data in the physical layer. This is done by building an information retrieval system, using the Berkeley DB library for operating on files and indices. Your job in this project is to write programs that keep data in files and maintain indices that provide basic searches over data. 80% of the project mark would be assigned to your implementation which would be assessed in a demo session, and is further broken down to three phases with 10% of the mark allocated for Phase 1, 5% of the mark for Phase 2, and 65% for Phase 3. Another 15% of the mark will be assigned for the documentation and quality of your source code and for your design document. 5% of the mark is assigned for your project task break-down and your group coordination.

Group work policy

You will be doing this project with one or two other partners from the 291 class. Your group information from mini-project 1 is copied to mini-project 2 groups page on the assumption that you would be working in the same group. If you decide to change groups, please notify the instructor. It is assumed that all group members contribute somewhat equally to the project, hence they would receive the same mark. In case of difficulties within a group and when a partner is not lifting his/her weight, make sure to document all your contributions. If there is a break-up, each group member will get credit only for his/her portion of the work completed (losing the mark for any work either not completed or completed by the partner). For the same reason, a break-up should be your last resort.

Task

You are given a data file, which you will use to construct your indices. Here is a small data file with only 10 records and here is one with 1000 records. The data includes product reviews on Amazon; each review record consists of a product id, a product title, a product price, userid and profile name of the reviewer, helpfulness of the review, review score, review timestamp, summary and full text of the review, Your job is to create indices, following Phases 1 and 2, and use those indices to process the queries in Phases 3.

Phase 1: Preparing Data Files

Write a program that reads reviews from standard input and construct the following four files. Before constructing these files, escape every double quote " in the input by replacing it with &quot; and escape every backslash (\) by replacing it with double backslash (\\). Backslash is escaped since Berkeley DB does not like it in the input; double quote is also escaped so the symbol can be used to encode the character strings.

reviews.txt: This file has one row for each review record. The fields are ordered as given in the input, and the consecutive fields are separated by a comma. The fields product title, profile name (of the reviewer), review summary and review text are placed inside quotations to avoid a possible mixup in the separator character, for example when a comma appears inside a text field. The first field is the record number (or record id) which is assigned sequentially to input records with the first record assigned id 1. Here is this file for our sample file with 10 records.

pterms.txt: This file includes terms of length 3 or more characters extracted from product titles; a term is a consecutive sequence of alphanumeric and underscore '_' characters, i.e [0-9a-zA-Z_] or the character class \w in Perl or Python. The format of the file is as follows: for every term T in a product title of a review with id I, there is a row in this file of the form T',I where T' is the lowercase form of T. That means, terms must be converted to all lowercase before writing them in this file. Here is the respective file for our sample file with 10 records.

rterms.txt: This file includes terms of length 3 or more characters extracted from the fields review summary and review text. The file format and the way a term is defined is the as given above for the filepterms.txt. Here is the respective file for our sample file with 10 records.

scores.txt: This file includes one line for each review record in the form of sc:I where sc is the review score and I is the review id. Here is the respective file for our sample file with 10 records.

These files can also be found at directory ~drafiei/291/pub on the lab machines. In the same directory, you would also find larger size files (such as 1k and 10k records) that you may want to use in the testings of your programs.

Phase 2: Building Indexes

Sort all the files built in Phase 1 (except the file reviews.txt which is sorted) using the Linux sort command; pass the right option to the sort command to keep only the unique rows (see the man page for sort). You can keep the sorted data under the same file names or pass sorted records to stdout so they can be piped to your loading program (as described next). Suppose the sorted files are named as before (to simplify our presentation here). Given the sorted files reviews.txt, pterms.txt, prterms.txt and scores.txt, create the following four indexes: (1) a hash index on reviews.txt with review id as key and the full review record as data, (2) a B+-tree index on pterms.txt with terms as keys and review ids as data, (3) a B+-tree index on rterms.txt with terms as keys and review ids as data, (4) a B+-tree index on scores.txt with scores as keys and review ids as data. You should note that the keys in all 4 cases are the character strings before the first comma and the data is everything that comes after the comma. Use the db_load command to build your indexes. db_load by default expects keys in one line and data in the next line. Here is a simple Perl script that converts input records into the format db_load expects. Your program for Phase 2 would produces four indexes which should be named rw.idx, pt.idx, rt.idx, and sc.idx respectively corresponding to indexes 1, 2, 3, and 4, as discussed above.

In addition to db_load, you may also find db_dump with option p useful as you are building and testing the correctness of your indexes.

Phase 3: Data Retrieval

Given the index files rw.idx, pt.idx, rt.idx and sc.idx created in Phase 2 respectively on review ids, product title terms, review terms, and scores, write a program that processes queries as follows. Each query returns the full record of the matching review, with review id given first, followed by the rest of the fields formatted for output display, in some readable format. Here are some examples of queries:

p:camera
r:great
camera
cam%
r:great cam%
rscore > 4
camera rscore < 3
pprice < 60 camera
camera rdate > 2007/06/20
camera rdate > 2007/06/20 pprice > 20 pprice < 60
The first query returns all records that have the term camera in the product title. The second query return all records that have the term great in the review summary or text. The third query returns all records that have the term camera in one of the fields product title, review summary or review text. The fourth query returns all records that have a term starting with cam in one of the fields product title, review summary or review text. The fifth query returns all records that have the term great in the review summary or text and a term starting with cam in one of the fields product title, review summary or review text. The sixth query returns all records with a review score greater than 4. The 7th query is the same as the third query except it returns only those records with a review score less than 3. The 8th query is the same as the third query except the query only returns those records where price is present and has a value less than 60. Note that there is no index on the price field; this field is checked after retrieving the candidate records using conditions on which indexes are available (e.g. terms). The 9th query returns the records that have the term camera in one of the fields product title, review summary or review text, and the review date is after 2007/06/20. Since there is no index on the review date, this condition is checked after checking the conditions on terms. Also the review date stored in file reviews.txt is in the form of a timestamp, and the date give in the query must be converted to a timestamp before a comparison (e.g. check out the date object in the datetime package for Python). Finally the last query returns the same set of results as in the 9th query except the product price must be greater than 20 and less than 60.

More formally, each query defines some conditions that must be satisfied by one or more of the following fields: product title, product price (referred to as pprice in queries), review score (referred to as rscore in queries), review date (referred to as rdate in queries), review summary and review text. A condition on terms from product title, review summary and review text can be either an exact match or a partial match; for simplicity, partial matches are restricted to prefix matches only (i.e. the wild card % can only appear at the end of a term). All matches are case-insensitive, hence the queries "Camera", "camera", "cAmera" would retrieve the same results; for the same reason the extracted terms in previous phases are all stored in lowercase. Matches on review scores, review dates and product price are range conditions denoted by rscore > and rscore < for review scores, rdate > and rdate < for review dates and pprice > and pprice < for product price. There is zero or more spaces between any of the terms rscore, rdate, andpprice and the symbols < and >. There is also zero or more spaces between any of the symbols < and > and the number or the date that follows it. Hence, rscore<20, rscore< 20, rscore <20, and rscore     <    20 are all valid and would return the same matches. Queries can use two range predicates on the same field as is the cases in Query 10. Matches on terms can be exact (as in queries 1-3) or partial (as in query 4). A query can have multiple conditions (as in queries 5, 7, 8, 9 and 10) in which case the result must match all those conditions (i.e. the and semantics), and there is one or more spaces between the conditions. The keywords rscore, pprice and rdate are reserved for searches (as described above) and would not be used for any other purposes. The dates are formatted as yyyy/mm/dd in queries but they are stored as timestamps in the data file; this means dates in the input queries must be converted to timestamp before a search can be performed. You can assume every query has at least one condition on an indexed column, meaning the conditions on rscore, pprice and rdate can only be used if a condition on review/product terms or review scores is also present.

Testing

At demo time, your code will be tested under a TA account. You will be given the name of a data file, and will be asked (1) to prepare reviews.txt, pterms.txt, rterms.txt, scores.txt, (2) build Berkeley DB indexes rw.idx, pt.idx, rt.idx and sc.idx, and (3) provide a query interface, which will allow us to test your system for Phase 3. We typically follow a 5 minutes rule, meaning that you are expected to prepare the data and build your indices in Phases 1 and 2 in less than 5 minutes; if not, we may have to use our own indexes, in which case you would lose the marks for Phases 1 and 2.

The demo will be run using the source code submitted and nothing else. Make sure your submission includes every file that is needed. There will be a limited time for each demo. Every group will book a time slot convenient to all group members to demo their projects. At demo time, all group members must be present. The TA will be asking you to perform various tasks and show how your application is handling each task. A mark will be assigned to your demo on the spot after the testing.

Important note: You can make no assumption on the number of review records (and the size of any of the files and indexes that are built from the input file). We will be using a relatively large file for testing and you don't want your program to break down in our tests, resulting in a poor mark! That said, you can make very few assumptions (such as the inverted list of a term can fit in main memory) and clearly state them in your report. You can also assume that the length of a review text cannot exceed 33000 characters (or bytes).

Instructions for Submissions

Your submission includes (1) the source code for phases 1, 2 and 3 and any makefile or script that you may need to compile your code, and (2) a short report. Your source code must include at least three programs, i.e. one for each phase. Your program for Phase 3 would implement a simple query interface in your favorite programming language (e.g. Python, C or C++, Java). For phases 1 and 2, you can have more than one program (for example, in Python, C, C++, java or Perl) and can make use of any Unix command and scripting language (e.g. Perl, bash) that runs under Linux on lab machines, as long as you clearly document in your report how and in what sequence the programs or commands should run. The source code is submitted as follows:

Create a single gzipped tar file with all your source code and additional files you may need for your demo. Name the file prj2code.tgz.
Submit your project tarfile in the project submission site by the due date at the top of this page.
Your report must be type-written and submitted in hardcopy at the designated drop boxes located on the first floor of CSC building, across from the room 1-45 before the due date. Your report cannot exceed 3 pages in length plus one additional cover page. Your project report is due on Friday November 27th, at 10am, and no late submission is allowed for the project report. All project members are expected to submit their code online but only one copy of the project report will be submitted.

The report should include (a) a general overview of your system with a small user guide, (b) a description of your algorithm for evaluating queries, in particular evaluating queries with multiple conditions and wild cards and range searches and an analysis of the efficiency of your algorithm, (c) your testing strategy, and (d) your group work break-down strategy. The general overview of the system gives a high level introduction and may include a diagram showing the flow of data between different components; this can be useful for both users and developers of your application.  The user guide should have instructions for running your code for phases 1, 2 and 3. The testing strategy discusses your general strategy for testing, with the scenarios being tested and the coverage of your test cases. The group work strategy must list the break-down of the work items among partners, both the time spent (an estimate) and the progress made by each partner, and your method of coordination to keep the project on track. The design document should also include any assumption you have made or any possible limitations your code may have.
