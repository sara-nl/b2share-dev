# B2SHARE dev env

## Start docker composite

```
B2SAHRE=/path/to/b2share/git/repo docker-compose up
```

for example:

```
B2SHARE=../b2share docker-compose up
```

## Prepare UI:
(one time)

go inside container b2share-dev_b2share_1


```
./init_ui.sh 
```

## Init demo data

go inside container b2share-dev_b2share_1

```
supervisorctl start celery
supervisorctl start celery_beat

b2share demo load_config
b2share db init
b2share upgrade run -v
b2share demo load_data
b2share run -h 0.0.0.0
```
## Install test data

```
goinside b2share-dev_postgres_1
/build/import_data.sh
```

```
goinside b2share-dev_b2share_1
/build/init_data.sh
```

## Create Fake DOIs and validate data

Install package `libpq-dev`

```
cd validator
pipenv --python 3 install -r requirements.txt
pipenv shell
python generate_fake_dois.py --dryrun
python generate_fake_dois.py
python generate_fake_dois.py --dryrun
```
After generation of fake dois:
```
goinside b2share-dev_b2share_1:

b2share index destroy
b2share index init
b2share index run
b2share index reindex --yes-i-know
b2share index run
```

Validate records

Get token from b2share and store it as validator/token.txt

```
cd validator
pipenv shell

# aggregate languages
python validate.py --lang --token token.txt  --schema datacite-v3/metadata.xsd

# validate
python validate.py --validate --token token.txt  --schema datacite-v4/metadata.xsd
```

