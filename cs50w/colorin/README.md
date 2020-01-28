# Final Project

Web Programming with Python and JavaScript

My final project is "Colorin", a membership website profiled to bookmarking online study materials. The bookmarks are added by the members, and are accessible by themes and platforms (websites hosting digital content). 


## Project structure

Colorin is a Django 3.0 project based on Python 3.8, and it includes two applications:
- "Members" - covering simple member activities
- "Staff" - covering activities specific to staff members

Programming approach: I'm using Django's ORM and server-side templating, combined with Ajax calls and plain JavaScript. My aim is to replace gradually the server-side templates with client-side code.

### Business Logic

Newcomers need to sign up and complete their profiles in order to be able to access their dashboards.

The themes, platforms and social networks are proposed by simple members and approved by staff members. The approved social networks can be used by members on their profiles.

The bookmars are referred as "study materials" across the website. Each study material has an associated comment list, and each member is able to send and receive private messages to/from other members.

Study materials, comments, private messages and public member profiles can be reported as inappropriate by simple members, and the reports can be processed by staff members.

Simple members are able to perform the following actions:
- update their own public profiles
- propose themes, platforms or social networks not yet on file
- review their incoming private messages (sent by other members); reply to private messages; report a private message
- review their outgoing private messages (to other members)
- add study materials to themes (contribute with bookmarks)
- edit or hide their own contributions; report a study material
- access study materials by themes, platforms, members, direct links
- access the comment list associated to each study material; add comments to the list; edit or hide their own comments; report a comment
- access each member's public profile; report a public profile

Staff members are able to perform the following additional actions:
- process proposed themes, platforms and social networks. These items are added to the database with "private" status. Upon publishing, the item status is set to "public" and it becomes visible to simple members. Upon hiding or archiving the item, it becomes permanently hidden from simple members.
- process items reported by simple members. Reports are added to the database with "initiated" status. Upon ignoring a report, its status is set to "archived". Upon processing a report, the reported item status is set to "archived", thus it's hidden permanently from simple members.
- review the activity of the members listed on the reports. A member's activity includes: added study materials, comments and reports of any status.

#### Not yet implemented:
- member sign-up verification (via email)
- members should be able to change their emails or passwords on file (with verification via email)
- "forgotten password" process (with verification via email)
- full-text, case insensitive search (it requires a SQL or NoSQL engine with specific indexing capabilities)
- limiting the count and frequency of actions accomplished by simple members (it requires a server-side memory caching solution)
- periodical removal of hidden items, which have no associated reports on file (cron job)
- periodical removal of archived items (cron job)
- periodical removal of ignored reports (cron job)

Note: my project is a MVP, and it will go live after implementing some of the above listed features.

### Database

The database is currently implemented as a sqlite3 file - included in the project's root folder. 

This is a test database, it contains random text, and it has only test users with the following names (their passwords are the same as their names):
- super - the super user
- timtim - staff member
- dandan, janjan, kenken, marmar - simple members

Note: all the database tables are available via the "127.0.0.1:8000/admin" URL (Django's admin interface).

There are eight tables:

#### Member
- for authentication I'm using the "django.contrib.auth" module
- the "djuser" field in this table is the user's name, extracted from "request.user.username"
- this table includes the member's public profile data (full name, location etc.)

#### Network
A list of Internet domain names representing social networks - for example "twitter.com".

#### Theme
A list of subject matters for categorizing the study materials - for example "Electronics".

#### Platform
A list of Internet domain names: learning platforms and other sites hosting online digital content suitable for learning - for example "alison.com", "oreilly.com" etc.

#### Suggestion
- a list of study materials (bookmarks) added by members
- it includes mandatory title and Url, optional author, year of publishment, opinion

#### Comment
Comments associated to the study materials.

#### Messages
Private messages sent between members.

#### Flag
Reported items (study materials, comments, private messages, public member profile).


## Files and Folders

### Root Folder

- db.sqlite3 - test database
- manage.py - Django file
- README.md - this file
- requirements.txt - it includes "Django==3.0.1"

### colorin folder

- __init__.py - Python file
- asgi.py - Django 3 file, unused (for web servers with asynchronous operations support)
- settings.py - Django file: in INSTALLED_APPS list added the "members" and "staff" applications; replaced the SECRET_KEY with a dummy string
- urls.py - Django file - added paths to the "members" and "staff" applications
- wsgi.py - Django file, unused (for web servers)

### members folder

- __init__.py - Python file
- admin.py - Django file - added my database tables (made them available via the Django admin interface)
- apps.py - Django file
- helpers.py - my custom source code file: a collection of small helper functions I've used in view.py, in both applications of the project ("members" and "staff")
- models.py - added my object model (numeric choices, database tables and relations)
- tests.py - Django file, unused
- urls.py - Django file - added my routes
- views.py - Django file - added my code

#### migrations folder

Django folder used by their ORM.

#### static/members folder

- site.css - styling used across the site
- small image files used on the site: back.png, cancel.png, envelope.png, flag.png, inma.png, logo40.png, logout.png, member.png, outma.png, up.png
- commentlist.js - included in commentlist.html
- layout.js - included in layout.html
- memberboard.js - included in memberboard.html
- memberdetails.js - included in memberdetails.html
- memberprofile.js - included in memberprofile.html
- platformlist.js - included in platformlist.html
- staffboard.js - included in stafboard.html
- themedetails.js - included in themedetails.js

#### templates/members folder

- commentlist.html - list of comments associated to a given study material
- incominglist.html - list of incoming private messages of a given member
- layout.html - the master template - all the other templates in the "members" and "staff" applications are based on this template
- memberboard.html - the simple member's dashboard, it includes the theme list
- memberdetails.html - the member's public profile, followed by a list of all the study materials (bookmarks) added by this member
- memberprofile.html - page for updating the member's public profile, it includes the social network list
- mylogin.html - page for login
- mysignup.html - page for signup
- outgoinglist.html - list of outgoing private messages of a given member
- platformdetails.html - list of study materials added by members and hosted by a given platform
- platformlist.html - list of platforms
- themedetails.html - list of study materials added by members to a given theme

### staff folder

- __init__.py - Python file
- admin.py - Django file, unused
- apps.py - Django file
- models.py - Django file, unused
- tests.py - Django file, unused
- urls.py - Django file - added my routes
- views.py - Django file - added my code

#### migrations

Django folder used by their ORM.

#### templates/staff folder

- membercomments.hml - list of comments added by a given member
- memberreports.html - list of reports added by a given member
- membersuggestions.html - list study materials added by a given member
- profileinfo.html - the public profile of a given member, it includes links to the lists of study materials, comments and reports added by this member
- reportedcomment.html - details of a given comment, reported by a member
- reportedmessage.html - details of a given private message, reported by a member
- reportedprofile.html - details of a given public profile, reported by a member
- reportedsuggestion.html - details of a given study material, reported by a member
- staffboard.html - the staff member's board, it includes the lists of proposed themes, platforms and social networks waiting for approval
- staffreport.html - list of items reported by members as inappropriate
