
How to translate Memopol2 ?

- go to the source folder (the same folder where this readme is located)

- check that you don't already have your translation in locale/<your language code>

if not : 

- create locale directory if needed : 
  mkdir locale

- create messages for your language (for french)
  django-admin.py makemessages -l fr

- go to the po file directory : 
  cd locale/fr/LC_MESSAGES

- edit the po file : 
  emacs django.po

- translate the "msgid" (don't touch them) in the "msgstr" strings

- send us the .po file either through git or by mail.

