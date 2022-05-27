# Projects
A slight culmination of some code i have developed
# TellMeAStory4
Authors:
Joshua Adewunmi,
Drew Barlow,
Kush Shah,
Jason Nachman, and
Kyle Wright.
To explore the project, visit this Heroku link.
NOTE: Heroku has been having issues with GitHub deployment. We apologize if the link does not work properly.

To run this project:
Clone this repository or download and extract the source code.
Run python3 pip install -r requirements.txt to install the necessary dependencies.
Receive an API key from MapBox.
Set APIKEY = <your_key> in story/tellmeastory/constants.py.
Run python3 story/manage.py migrate.
Run python3 story/manage.py runserver and visit localhost:8000.
If you wish to run tests:
Run python3 story/manage.py test story/<APP_NAME>/tests.
NOTE: <APP_NAME> should be replaced by either tellmeastory or managetags.
Notes about tests:
There must be an image named "test_image.jpeg" in media/storyimages/.
Google Chrome must be installed! We use Selenium for some tests.
Issues occur in the database when pulling a branch. If this is the case, run these commands:
cd story
python3 manage.py flush
rm db.sqlite3
rm tellmeastory/migrations/00*
rm managetags/migrations/00*
python3 manage.py makemigrations
python3 manage.py migrate
