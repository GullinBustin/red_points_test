# red_points_test

Install Virtualenv

`sudo apt-get install virtualenv`

Create Virtualenv

`virtualenv -p [python path] [directory]`

`virtualenv -p python3.8 venv`
`virtualenv -p python3.6 venv`

Activate Virtualenv

`source venv/bin/activate`

Deactivate Virtualenv

`deactivate`

Install requirements

`make install-req`

`pip install -r requirements/dev.txt`

Run Crawler

`make run`

```bash
cd source
python main.py
```

Run test

`make run-test`

`python -m pytest`