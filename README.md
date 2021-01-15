# Battle Score Aggregator
A system to automatically count scores for Battle of the Books.

## Dependencies
* **Python 3.9.1** - This is the version I use in production, but any version that satisfies the pip requirements will work fine.
* **A bunch of dependencies** - They can be installed with the following command on Linux:
```bash
pip3 install aiohttp==3.6.2 aiohttp_jinja2 aiohttp_session jinja2 toml cryptography passlib bcrypt marshmallow
```
Or the following command on Windows:
```batch
pip install aiohttp==3.6.2 aiohttp_jinja2 aiohttp_session jinja2 toml cryptography passlib bcrypt marshmallow
```
Please note that the `aiohttp` version __MUST__ be `3.6.2`. This is due to an issue with `aiohttp_session` which results in sessions being lost during HTTP redirects if the aiohttp version is higher than that.

## Installation
* Install the above dependencies.
* Copy the project contents to the desired folder.
* Run `python3 main.py` on Linux, or `python main.py` on Windows.

## Usage
The admin interface is enabled by default, as in new installations, the first thing you'd probably want to do is to create new judges, but please note that the admin interface should **NEVER** be enabled in production.

Judges can be created by navigating to `http://host:port/admin` where `host` and `port` are the ports specified in `conf.toml`.

Once judges are created, they are considered semi-permanent. They cannot be deleted unless they are quite *literally* deleted from the `/storage` folder. Likewise, if a Judge forgets their password, there is no recourse of action for this. The judge must be created anew.

Once created, a judge can log in with their username and password by navigating to `http://host:port/judge`. Here, the judge may enter scores.

Totals can be found at `http://host:port/total`. Here, the scores and placements of all teams are updated dynamically using AJAX.

## License
[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
