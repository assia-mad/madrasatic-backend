# madrasatic-backend
# la_base_de_données:
   1-installer et configurer POSTGRESQL
   2-quelques postgres commandes:
       psql -U user -W   // connecter avec "user"   //dans repertoire bin de postgres
       \c dbName; // connecter a la bd
       \dt  // show tables
       select * from tablename;
       delete from tableName where ... // supprimer une ligne a partir d'une table
# python et django 
 installer python 
 installer django , django rest_framework   // en utilisant la commande pip 
 # qlq cmd necessaire
   dans le repertoire de projet : 
   py manage.py makemigrations
   py manage.py migrate
   py manage.py runserver
   pour creer un admin de projet : py manage.py createsuperuser
   
# install all packages 
Run pip install -r requirements.txt (Python 2), or pip3 install -r requirements.txt (Python 3)
