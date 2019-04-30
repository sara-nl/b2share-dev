# B2SHARE dev env

## Pull in all submodules

```
git submodule update --recursive --init
```

## Start docker composite

```
docker-compose up
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
## Install test data and create fake DOIs

```
goinside b2share-dev_postgres_1
/build/import_data.sh
```
Install package `libpq-dev`

```
cd validator
pipenv --python 3 install -r requirements.txt
pipenv shell
python generate_fake_dois.py --dryrun
python generate_fake_dois.py
python generate_fake_dois.py --dryrun
```
