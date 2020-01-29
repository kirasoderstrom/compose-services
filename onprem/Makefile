
all: fence/ gen3-s3indexer/ hatchery/ portal/ tube/

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
hatchery/:
	git clone https://github.com/ohsu-comp-bio/hatchery-lite.git
	cd hatchery-lite;\
		git checkout master ; \
		docker build --network=host -t onprem/hatchery .


# build and tag an instance of data-portal
portal/:
	git clone https://github.com/ohsu-comp-bio/data-portal.git
	cd data-portal ;\
		git checkout workspace-default-notebook ; \
		docker build --network=host -t onprem/data-portal .

# build and tag an instance of tube
tube/:
	git clone https://github.com/ohsu-comp-bio/tube.git
	cd data-portal ;\
                git checkout secure-elastic; \
                docker build --network=host -t onprem/data-portal .
