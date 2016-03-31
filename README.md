# uw-tree
## Inspiration
I feel it is hard to keep track of all the course I need to take to get a certain degree and don't want to spend time go though all the Major and minor list to add a new major or minor in 8 study terms.

## What it does
This application plans the coursesby term for you to get your major and it can suggest courses if you are not sure which course to take.

## How I built it
Use MongoDB as database, Python Flask as rest services, Angular JS as frontend
Data comes from uwaterloo open API (https://api.uwaterloo.ca/) and University of Waterloo websites
Login system using Twitter account 

## Challenges I ran into
Filter and extract valid infomation from the data from the uwaterloo API (Different professors use different rules when writing prereq of a course, it is super hard to parse the prereq)
Nobody provides course data for Major, Minor and options, so we need to crawl them ourselves from the school website (http://ugradcalendar.uwaterloo.ca/) and parse them.
How to design the course recommandation system

## Accomplishments that I'm proud of
Finish the parser for the course prereqs using rule based tree and regex. The accuracy is not bad. :)

## What I learned
Full-stack web development skills
Web crawler development skills
Communicate with MongoDB with Document-Object Mapper (like the ORM for relational database)

## What's next for uw-tree
Frontend development, refine backend logic
