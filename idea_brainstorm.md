# Brainstrom IDEA

## Key information

We are developing a web app providing a news feed that are personalised.
Target audiance will be Korean who lives in the UK.

The web all will
- retrive the UK news from web
- categorise the news using LLM
- Add the article in the database along with the category
  - Category is mixed between hard-coded list and free form that LLM will use
- LLM wil fetch article that are relavent to user. For example:
  - tube strike will affect certain region residence
  - property law change will update certain group of people
  - Visa change will affect almost all Korean
- User will input their information so they can get personalised feed
  - Postcode, age, occupation (Hard-list)
  - Interest (Free-form text)
- The feed will be visualised as cards
  - Front card will have: Title representing the article, Action/Impact of the news in personalised format
  - Back card will have: summarised article, link to the source 
- The name of the app is "What now?" because it shows user what affect them and what they will need to do based on the articles.

## Specifications

- FastAPI backend
- VueJS frontend
- SQLite db

## Behavioural rule

- git should be actively used throughout the development
- ask user whether to commit if you think it's needed
- leverage worktree whenever needed
- do not work on main branch
- create a branch and push per task


## Important note

This is 3 hours Hackatone project; therefore, we focus on delivering MVP.

