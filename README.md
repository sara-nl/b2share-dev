# B2SHARE dev env

## Start docker composite

```
B2SHARE=/path/to/b2share/git/repo docker-compose up
```

for example:

```
B2SHARE=../b2share docker-compose up
```

## Prepare UI
(one time)

Go inside container `b2share-dev_b2share_1` and run the `init_ui.sh` script:

```
goinside b2share-dev_b2share_1
./init_ui.sh
```

When updating any React or JS files, rerun this command or run:

```
npx webpack [--config webpack.config.devel.js]
```

in the `webui` folder.

## Init configuration and run upgrades

Go inside container `b2share-dev_b2share_1` and run the `init_config.sh` script:

```
goinside b2share-dev_b2share_1
./init_config.sh
```

## Init demo data

Go inside container `b2share-dev_b2share_1` and run the `init_data.sh` script:

```
goinside b2share-dev_b2share_1
./init_data.sh
```

## Init index
Create elasticsearch index:

```
goinside b2share-dev_b2share_1
./init_index.sh
```

## Run B2SHARE

Go inside container `b2share-dev_b2share_1` and run the `run.sh` script:

```
goinside b2share-dev_b2share_1
./run.sh
```

## Optional

### Create Fake DOIs and validate data

Install package `libpq-dev`

```
cd validator
pipenv --python 3 install -r requirements.txt
pipenv shell
python generate_fake_dois.py --dryrun
python generate_fake_dois.py
python generate_fake_dois.py --dryrun
```

After generation of fake DOIs:
```
goinside b2share-dev_b2share_1:
./init_index.sh
```

### Validate records

Get token from B2SHARE and store it as `validator/token.txt`

```
cd validator
pipenv shell

# aggregate languages
python validate.py --lang --token token.txt  --schema datacite-v3/metadata.xsd

# validate
python validate.py --validate --token token.txt  --schema datacite-v4/metadata.xsd
```
