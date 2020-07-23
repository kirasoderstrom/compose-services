
all: fence/ gen3-s3indexer/ hatchery-lite/ data-portal/ tube/ covid19_datadictionary/ analysis-etl/ dashboard-multi/

# build and tag an instance of fence
fence/: 
	git clone https://github.com/ohsu-comp-bio/fence.git
	cd fence ;\
		git checkout onprem ; \
		docker build --network=host -t onprem/fence .

# build and tag an instance of indexs3client
indexs3client/:  
	git clone https://github.com/ohsu-comp-bio/indexs3client.git
	cd indexs3client ;\
		git checkout onprem ; \
		docker build --network=host -t onprem/indexs3client .

# build and tag an instance of s3indexer
gen3-s3indexer/: indexs3client/ 
	git clone https://github.com/ohsu-comp-bio/gen3-s3indexer.git
	cd gen3-s3indexer ;\
		git checkout onprem ; \
		docker build --network=host -t onprem/s3indexer .

# build and tag an instance of hatchery-local
hatchery-lite/:
	git clone https://github.com/ohsu-comp-bio/hatchery-lite.git
	cd hatchery-lite;\
		git checkout master ; \
		docker build --network=host -t onprem/hatchery .


# build and tag an instance of data-portal
data-portal/:
	git clone https://github.com/ohsu-comp-bio/data-portal.git
	cd data-portal ;\
		git checkout workspace-default-notebook ; \
		docker build --network=host -t onprem/data-portal .

# build and tag an instance of tube
tube/:
	git clone https://github.com/ohsu-comp-bio/tube.git
	cd data-portal ;\
                git checkout secure-elastic; \
                docker build --network=host -t onprem/tube .

covid19_datadictionary/:
	# git clone git@github.com:uc-cdis/covid19_datadictionary.git
	git clone https://github.com/ohsu-comp-bio/covid19_datadictionary.git
	
analysis-etl/:
	# you will need to setup .netrc to hold userid/password
	git clone https://itgcode.ohsu.edu/scm/key/analysis-etl.git
	cd analysis-etl ;\
		docker build --network=host -t onprem/analysis-etl .

dashboard-multi/:
	# you will need to setup .netrc to hold userid/password
	git clone https://itgcode.ohsu.edu/scm/key/dashboard-multi.git
	cd dashboard-multi/ ;\
		git checkout no_sqldb_deps; \
		docker build --network=host -t onprem/dashboard-multi .
