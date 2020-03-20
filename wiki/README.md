
# wiki

The wiki setup is 'semi automated'.  

Following is not a script, but a catalog of manual steps:

```

#set passwords in wiki/.env
export WIKI_PASSWORD=XXX
export DB_PASSWORD=$WIKI_PASSWORD
export SECRET_KEY=XXX

# manually comment out volume mapping of LocalSettings.php
# vi wiki/LocalSettings.php

# check mapping is commented
# clear previous instance of wiki
# drop db
# after startup, intialize the DB
grep -q "^ *- ./wiki/LocalSettings.php" wiki/docker-compose.yml && echo 'WARNING: edit docker-compose'
grep -q "# - ./wiki/LocalSettings.php" wiki/docker-compose.yml && \
  dc exec  mysql-service mysql -u wikiuser --password=$DB_PASSWORD -e "drop database wikidb;" && \
  unset SECRET_KEY && \
  rs wiki && \
  dc exec wiki-service  /script/install.sh  admin $WIKI_PASSWORD

# MANUALLY:copy the MEDIAWIKI_SECRET_KEY that install provides back to your compose file
# $wgSecretKey = "XXXXXXXXXXXX";
# !!!!!  export SECRET_KEY=XXXXXXXXXXXX
source wiki/.env


# MANUALLY:  uncomment the LocalSettings.php line in docker-compose
# restart the wiki
# update the schema
# add admin users before they log in.
# start background wiki job runners
grep -q "# - ./wiki/LocalSettings.php" wiki/docker-compose.yml && echo 'WARNING: edit docker-compose'
grep -q "^ *- ./wiki/LocalSettings.php" wiki/docker-compose.yml && \
  rs wiki && \
  dc exec wiki-service php maintenance/update.php --quick && \
  dc exec wiki-service php maintenance/createAndPromote.php  --bureaucrat --sysop --force  Walsbr $WIKI_PASSWORD && \
  dc exec -T -d  wiki-service sh -c "/data/run_jobs.sh > /data/run_jobs-0.out" && \
  dc exec -T -d  wiki-service sh -c "/data/run_jobs.sh > /data/run_jobs-1.out" && \
  dc exec -T -d  wiki-service sh -c "/data/run_jobs.sh > /data/run_jobs-2.out"

# validate its up
# fix docker mapping permissions snafu
# create special pages
# load special pages
dc exec wiki-service ps -ef | grep runJobs.php && \
  sudo chmod 777 wiki/data/imports && \
  sudo rm -f wiki/data/imports/special_pages.xml && \
  python3 wiki/data/import_special_pages.py  --output wiki/data/imports/special_pages.xml && \
  dc exec wiki-service php maintenance/importDump.php \
    --memory-limit max  /data/imports/special_pages.xml


# spot check to ensure special_pages updated
dc exec wiki-service php maintenance/pageExists.php Property:GID | grep exists  && echo "Special pages exists"

# browse website and verify links

# download wiki extract from BMEG
# TODO - replace with dvc instructions
scp -i ~/.ssh/id_rsa.pem ubuntu@10.96.11.98:/mnt/bmeg-etl/outputs/wiki/*.gz wiki/data/

# remove old xml files

sudo rm wiki/data/imports/*.xml

# create phenotypes
python3 wiki/data/import_pages.py  --input wiki/data/Phenotype.wiki.json.gz  --output wiki/data/imports/Phenotype --batch_size 100

# create compounds, ontologies and synonyms
python3 wiki/data/import_pages.py  --input wiki/data/Compound.wiki.json.gz --output wiki/data/imports/Compound --batch_size 100


# Choice:  import all data, or import only some using file wildcards

IMPORT_JOB_WORKERS=25

# import all, we sort randomly so we don't have to wait to browse files at the end
dc exec -T -d  wiki-service sh -c "ls -1p /data/imports/*.xml | sort -R | parallel -j $IMPORT_JOB_WORKERS php maintenance/importDump.php   --memory-limit max"  

# monitor progress ,  see CPU% of wiki and mysql
# Note: takes ~ 1 Hour
docker stats


# to extract data from the wiki

python3 transform/wiki/import_wiki_compounds.py --refresh_file transform/wiki/credentials.json --output outputs/wiki/CompoundSynonyms.json

python3 transform/wiki/import_wiki_phenotypes.py --refresh_file transform/wiki/credentials.json --output outputs/wiki/PhenotypeSynonyms.json



https://sequencediagram.org/
```
title BMEGWiki

participantgroup #lightgreen **bmeg-etl**
participant import_wiki_compounds.py
participant import_wiki_phenotype.py
participant compound_transform.py
participant compound_phenotype.py
database outputs/wiki/*.wiki.json
database outputs/wiki/*Synonym.json
end
participantgroup #lightgrey **gen3**
fontawesome f023 revproxy #1da1f2
end

participantgroup #lightblue **wiki**
participant import_pages.py
database wiki/data/imports/*.xml
participant importDump.php
fontawesome f266 wiki #1da1f2
actor curator
end

compound_transform.py->outputs/wiki/*.wiki.json: write
compound_phenotype.py->outputs/wiki/*.wiki.json: write
import_pages.py->outputs/wiki/*.wiki.json: read
import_pages.py->wiki/data/imports/*.xml: write
importDump.php->wiki/data/imports/*.xml: read
importDump.php->wiki: write
curator->wiki: edit
import_wiki_compounds.py->revproxy: token,query
revproxy->wiki: query
wiki-->import_wiki_compounds.py: [{}]
import_wiki_compounds.py->outputs/wiki/*Synonym.json: write
```
