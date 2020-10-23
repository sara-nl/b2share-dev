# B2SHARE dev env

This is the Docker definition for a development environment for B2SHARE.

## Requirements

Make sure to install:

```
docker
docker-compose
```

## Prepare

Clone this repository to a folder on your system:

```
git clone https://github.com/sara-nl/b2share-dev.git
```

Download the B2SHARE repository to a folder called `b2share` inside the dev environment:

```
git clone https://github.com/EUDAT-B2SHARE/b2share.git
```

Copy the environment file from the `dockerize` repository:

```
wget https://raw.githubusercontent.com/EUDAT-B2SHARE/dockerize/master/b2share.env -O .env
```

Set the environment variables in the env file, make sure to add `B2SHARE_SOURCE` and `B2SHARE_DATADIR`, e.g.:

```
B2SHARE_DATADIR=./instance
B2SHARE_SOURCE=./b2share
```

## Start docker composite

Start up your environment:

```
docker-compose up
```

Enter the b2share container.

### Init configuration and run upgrades

Go inside container `b2share-dev_b2share_1` and run the `init_config.sh` script:

```
./init_config.sh
```

### Init the indices

Create elasticsearch index:

```
./init_index.sh
```

## Initialisation

### Init UI
(one time)

Go inside container `b2share-dev_b2share_1` and run the `init_ui.sh` script:

```
./init_ui.sh
```

### Init demo data

Before you see any data, you can make sure some initial data is visible. This is optional.

Go inside container `b2share-dev_b2share_1` and run the `init_data.sh` script:

```
./init_data.sh
```

## Run B2SHARE

Go inside container `b2share-dev_b2share_1` and run the `run.sh` script:

```
./run.sh
```

You should now be able to open the website via [http://localhost](http://localhost).

## Development

When updating Python files, you need to rerun the Flask application. Inside the b2share container, kill the existing process (Ctrl-C):

```
./run.sh
```

When updating any React or JS files, rerun this command or run:

```
npx webpack [--config webpack.config.devel.js]
```

in the `webui` folder. Use the `devel` config file during development, omit the option to get the production settings.

## Optional

Some additional steps can be executed.

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
