# volca_sample_manager
volca_sample_manager

## Installation and Running

1. Download the code from github

```bash
git clone git@github.com:rabramley/volca_sample_manager.git
```

2. Install the requirements

Go to the `volca_sample_manager` directory and type the command:

```bash
sudo apt-get install libldap2-dev
sudo apt-get install libsasl2-dev

pip install -r requirements.txt
```

3. Create the database using

Staying in the `volca_sample_manager` directory and type the command:

```bash
./manage.py version_control
./manage.py upgrade
```

4. Run the application

Staying in the `volca_sample_manager` directory and type the command:

```bash
./app.py
```

5. Start Celery Worker

This application uses Celery to run background tasks.
To start Celery run the following command from the `volca_sample_manager`
directory:

```
celery -A celery_worker.celery worker
```

## Development

### Testing

To test the application, run the following command from the project folder:

```bash
pytest
```

# Redis

## Install

Follow the procedure on this site: https://redis.io/topics/quickstart

Which, if they haven't changed are:

1. `wget http://download.redis.io/redis-stable.tar.gz`
2. `tar xvzf redis-stable.tar.gz`
3. `cd redis-stable`
4. `sudo make install`

## Run

`redis-server`

To check that it is working run: `redis-cli ping`
