# Red Points Test

## How to use

Crawler needs python3.6 or newer

### [Optional] Virtualenv (Ubuntu)

#### Install Virtualenv

`sudo apt-get install virtualenv`

#### Create Virtualenv

`virtualenv -p [python path] [directory]`

for example:

`virtualenv -p python3.8 venv`

`virtualenv -p python3.6 venv`

#### Activate Virtualenv

`source [directory]/bin/activate`

for example:

`source venv/bin/activate`

#### Deactivate Virtualenv

`deactivate`

### Run Crawler

#### Write Input

Modify file `source/config.yml`

#### Install requirements

`pip install -r requirements/dev.txt`

Or via Makefile:

`make install-req`

#### Run Crawler

```bash
cd source
python main.py
```

Or via Makefile:

`make run`

### Run tests

#### Install requirements

`pip install -r requirements/dev.txt`

Or via Makefile:

`make install-req`

#### Run pytest

`python -m pytest`

Or via Makefile:

`make run-test`
