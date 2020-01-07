# Project 3

Web Programming with Python and JavaScript

## Database

The database is implemented as a sqlite3 file - included in the project's root folder.

The GROUP table includes product categories like Sicilian Pizza or Subs.

Each PRODUCT table item has a specific recipe (composition and processing), regardless of its dimensions. 

Each OFFER table item includes the unit price & dimensions (small, large etc.) of a PRODUCT table item.

There is one-to-many relationship between GROUP items and PRODUCT items. There is one-to-many relationship between PRODUCT items and OFFER items.

The PART table items represent a list of items (toppings), which have no price, because they are included in the various recipes. One product may include 0, 1, 2 or 3 parts. I consider that the "special" offer represents pizza with a special type of cheese (no toppping).

The EXTRAS table items represent a list of items (extras), which have their own prices, and are optional, offered in any combination.

The orders are kept in two tables having one-to-many relationship: OrderHeader with order-level data (like client and status), and respectively OrderDetail with one row for each product added into the cart and then checked out by the client.

### Prices

The unit prices listed on the client's (and staff member's) page are LIST prices, they are pulled from the OFFER table.

When somebody uses Django's admin interface for updating the OFFER table, all the clients and staff members who are logging in or refreshing their browser page after the update, will see the new LIST price.

When a client is clicking on a product's LIST price, that price is added to his/her cart, and it becomes PURCHASE price. The PURCHASE price is then used for checking out the cart and registering the order in the OrderHeader and the OrderDetails tables.

The same happens with the names of products, parts and extras - in the OrderDetails table they are stored as they have been set in the moment of being added to the cart.

Motivation: from juridical point of view there is no simple way to update the text and/or money amount on a document, which represents a legal agreement between two parties.

### Models

#### Group
- name

#### Product
- name
- category - foreign key on Group
- parts - maximum number of parts for this product
- extras - maximum number of extras for this product

#### Offer
- name
- price
- owner - foreign key on Product

#### Part
- name

#### Extra
- name
- price

#### OrderHeader
- client - user name (from Django "request.user.username")
- total - payable on order level
- status - it can take one of the following values: "placed", "completed", "on-hold", "canceled". The list is currently declared in the "staff.js" source file. Motivation: the use cases need to be discussed with the to-be customers.
- stamp - Python's "datetime.datetime.now()" output converted in string. Motivation: migrating date-time values between different platforms and databases is better supported this way.

#### OrderDetail
- oid - foreign key on OrderHeader
- name - product name
- namex - text - it includes the set of parts or extras selected by the client
- price - product's unit price
- pricex - price/product for the set of extras selected by the client
- quantity - quantity - on product level
- total - payable on product level - it should be quantity*(price+pricex)
- gid - group id for the product 
- pid - product id
- tid - offer id for the product

## Structure

### Test User list

- super - super user
- cook - staff user
- clerk - staff user
- john - client
- mary - client

The test passwords are the same as the test user names.

### Back-end

All the database tables are available via the "127.0.0.1:8000/admin" URL (Django's admin interface), and I've added/updated the complete menu offer by using that interface (groups, products, prices, toppings, extras etc).

Currently the database and Django's admin interface permit adding both parts and extras to each product, but the website's user interface is ready to handle only one of them: or parts or extras.

### Server-side Templates

- mylogin.html and mysignup.html are used for client or staff member authentication & authorization, employing Django's inbuilt modules
- clientboard.html - clients are redirected to this page after being logged in
- staffboard.html - staff members are redirected to this page after being logged in

The above mentioned two pages are using mostly JavaScript and Ajax requests for updating the user interface and interacting with the server.

## Files and Folders

### Root Folder

- db.sqlite3 - test database
- manage.py - Django file - "as is", received in project3.zip
- README.md - this file
- requirements.txt - updated to "Django==3.0.1" because I've installed and used the latest stable version of Django, available as of December 2019

### pizza folder

"as is", received in project3.zip

### orders folder

- __init__.py Django file
- admin.py - Django file - added my list of objects (database tables) available via the Django admin interface
- apps.py - Django configuration file
- models.py - added my object model (database tables and relations)
- tests.py - Django file - haven't added unit tests
- urls.py - Django file - added my routes
- views.py - Django file - added my code to handle http requests

#### migrations folder

Django folder used by their ORM

#### static/orders folder

- add.png, cancel.png, cart.png, logo.png, logout.png, order.png, pay.png, send.png, tick.png - small images used on the website
- pizza.css - style sheet used across the website
- client.js - my custom code used in clientboard.html
- staff.js - my custom code used in staffboard.html

#### templates/orders folder

- layout.html - common layout file for the following four templates
- mylogin.html - for client and staff member login
- mysignup.html - for new client signup
- clientboard.html - logged in clients are able to manage the cart (add products, remove products, check out with confirmation), and to list their orders (their list contains id, date, total, status info on order level)
- staffboard.html - logged in staff members are able to list client orders and update the order status (their order list contains both order-level data and product-level details)

## Notes

Software used for elaborating the project:
- Python 3.8
- Django 3.0.1
- others: Windows 10 Pro, VS Code, browsers

This project is a POC, please don't use it "as is" in real-life scenarios.
