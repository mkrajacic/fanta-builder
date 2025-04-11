# FantasySongContest

This is a fantasy game project tailored towards singing competitions. Users can create teams and allocate singers as the members of the team.
The user must select a member as the captain of the team. There is a set of occurrences. If an occurrence happens to a singer that is a member of the team, that team will have points added or deducted, depending on the type of the occurrence.
For example, if "Singer A" does "Thing A", the team which has "Singer A" as one of their members will have 20 points added to their result, because "Thing A" was specified to be a bonus which adds 20 points. Similarly, if "Thing A" was specified to be a penalty, the team would have 20 points deducted instead. If "Singer A" was set as the team captain, the points for the occurrence would be doubled, meaning the team would receive or lose 40 points.

Teams can have a limited number of assigned members. Users can create a limited number of teams. Each singer has a cost associated to them. The sum of all the costs of the assigned members cannot exceed a specified number. The aforementioned limits can be customised with settings specified in the *Custom settings* section

## Tech Stack

**Client:** HTMX, Alpine.js, Bootstrap 5.3

**Server:** Django

**Database:** MariaDB

**Icons:** MingCute Icon

## Examples
#### Add team
![add_team](https://github.com/user-attachments/assets/96e4cff8-1dae-4e79-bba0-cd2d61a79811)

#### Add members to the team and select the captain
![add_team_members](https://github.com/user-attachments/assets/dd10c102-e69e-4c37-a2ca-421326bbad41)

#### Update captain
![update_captain](https://github.com/user-attachments/assets/23742395-f95e-4240-8d37-97b231702a2c)

#### Singer results
![singer_results](https://github.com/user-attachments/assets/04e7f27e-d19b-4d82-b165-9c21f86a4181)

#### Leaderboards
![leaderboards](https://github.com/user-attachments/assets/b15c71e9-fa7c-4660-8dce-f262848531a7)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DATABASE_NAME`

`DATABASE_USER`

`DATABASE_PASSWORD`

`DATABASE_HOST`


## Run the project (Windows PowerShell instructions)

Clone the project

```bash
  git clone https://github.com/mkrajacic/fantasy-song-contest.git
```

Go to the project directory

```bash
  cd fantasy-song-contest
```

(Optional) Create python virtual environment and activate it

```bash
  python -m venv .\venv
  .\venv\Scripts\activate
```

Make django migrations and migrate

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

## Django apps

This project has the following django apps:

- users
    - authentication
    - user profile CRUD
- teams
    - team CRUD
    - modify lineup
    - change captain
    - display singers
- rules
    - display rules
    - display occurrences (bonuses and penalties)
- results
    - display results for singers
    - display team leaderboards

## Custom settings

The following settings impact the app functionalities:

`MAXIMUM_TEAMS_PER_USER`

`MEMBERS_PER_TEAM`

`MAXIMUM_USABLE_POINTS`

`TEAMS_READONLY` - determines if the team information and member lineups are changeable. If False, the display of teams will show detailed results for each team from the user

## Management commands
The app comes with two management commands for generating the results for the singers and teams.

The command makescores takes the id of an occurrence, the id of an event and the id (or multiple ids) of the singers

```bash
  python manage.py makescores occurrence_id event_id singer_id
```

After running makescores which assigns the occurrences to the event and singer(s), run makeresults to generate the results

```bash
  python manage.py makeresults
```
