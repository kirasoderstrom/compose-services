
# wiki

The wiki setup is 'semi automated'

```

export WIKI_PASSWORD=foobar-123
export DB_PASSWORD=$WIKI_PASSWORD
export SECRET_KEY=7393471b19ea9b3ff65ed1fcc1893c6825a0a23675fb7131d5d6264c2df42413


# start the wiki service __without__ LocalSettings
>>> in wiki/docker-compose.yml comment out this line
 - ./onprem/wiki/mediawiki/LocalSettings.php:/var/www/mediawiki/bmeg-wiki/LocalSettings.php:ro

# start the wiki service
rs wiki

# after startup, intialize the DB
dc exec wiki-service  /script/install.sh  admin $WIKI_PASSWORD

# copy the MEDIAWIKI_SECRET_KEY that install provides back to your compose file

export SECRET_KEY=XXXX

# restart the wiki
rs wiki

# update the schema

dc exec wiki-service php maintenance/update.php --quick

# add at least one admin user before anyone logs in.

dc exec wiki-service php maintenance/createAndPromote.php  --bureaucrat --sysop --force  <Capitalcaseusername> $WIKI_PASSWORD



Note:
  * Capitalcaseusername  = walsbr@ohsu.edu becomes Walsbr
  dc exec wiki-service php maintenance/createAndPromote.php  --bureaucrat --sysop --force  Walsbr $WIKI_PASSWORD


  * <some password> = necessary to create user but not used in authenticating since we are using Auth_remoteuser

# to reset all ; drop db and run all commands again
dc exec  mysql-service mysql -u wikiuser --password=$DB_PASSWORD -e "drop database wikidb;"

```




```
Load compounds to wiki:

extract from bmeg:  see /mnt/bmeg-etl/transform/wiki/transform.py
Copy /mnt/bmeg-etl/outputs/wiki/Compound.wiki.json.gz from bmeg to wiki  /home/ubuntu/compose-services/wiki/data/Compound.wiki.json.gz


Then start a nohup job to load pages
nohup docker-compose -f docker-compose.yml -f onprem/docker-compose.yml -f wiki/docker-compose.yml exec -T wiki-service php maintenance/importDump.php --dbuser $MEDIAWIKI_DB_USER  --dbpass $MEDIAWIKI_DB_PASSWORD --memory-limit max  --no-updates  /data/imports/compounds.xml

```
