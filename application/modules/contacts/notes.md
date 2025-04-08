Who we know, contacts from city/other useful people
models.py (has database stuff)
define new table called Contact (class)

###Contact def
contact_id = primary key
first_name = optional (32)
last_name = optional (32)
phone_number = str() (10) optional if email
email = optional if phone_number
notes = text()

routes.py (blueprint definition) look at roles, clearence (anyone in verified can create and view Contact)
forms.py
services.py (dependency injection) CRUD for contacts, private methods inside services (\_ prefix for privatefns)

application init.py add blueprint and model
new folder inside template (modual name) for contacts page
use roles as template
each contact represented with macro
using bootstrap 5 (roles as example)
card for each contact

modal (pop-up) for confirmation

unit-testing

make issue in github
