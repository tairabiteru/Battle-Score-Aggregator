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
py -3 -m pip install aiohttp==3.6.2 aiohttp_jinja2 aiohttp_session jinja2 toml cryptography passlib bcrypt marshmallow
```
Please note that the `aiohttp` version __MUST__ be `3.6.2`. This is due to an issue with `aiohttp_session` which results in sessions being lost during HTTP redirects if the aiohttp version is higher than that.

## Installation
* Install the above dependencies.
* Copy the project contents to the desired folder.
* Run `python3 main.py` on Linux, or `py -3 main.py` on Windows.

## Usage
The admin interface is enabled by default, as in new installations, the first thing you'd probably want to do is to create new judges, but please note that the admin interface should **NEVER** be enabled in production. It can be disabled in `conf.toml`, once you've created your judges and teams.

Judges can be created by navigating to `http://host:port/admin` where `host` and `port` are the ports specified in `conf.toml`.

Once judges are created, they are considered semi-permanent. They cannot be deleted unless they are quite *literally* deleted from the `/storage` folder. Likewise, if a Judge forgets their password, there is no recourse of action for this. The judge must be created anew.

Once created, a judge can log in with their username and password by navigating to `http://host:port/judge`. Here, the judge may enter scores.

Totals can be found at `http://host:port/total`. Here, the scores and placements of all teams are updated dynamically using AJAX.

## FAQ
- **How do I edit a judge's username?** - There's no way to do this through the web interface. You can however, change the `username` field in their corresponding JSON file in the `/storage` directory.

- **How do I change a judge's password?** - You can't. The judge will have to be created anew. You cannot simply edit the password field in the JSON file for the judge because the password is stored in an encrypted format. (Really, if you know how to program and know how to use `passlib` and `bcrypt`, you could do it. But that's above and beyond the scope here.)

- **How do I move teams between judges?** - Okay, this applies pretty much for all questions about changing any information about teams or judges: Judges and teams, once created, are pretty much permanent. Unless you're willing to edit the JSON files, there's no way to change any information about judges through the web interface.

- **How do I delete a judge?** - Delete the judge's corresponding JSON file. There is no way to do this through the web interface by design.

- **Why does the admin interface have to be disabled in production?** - During production when the server is exposed to clients, the admin interface will be accessible to ANYONE who is privy to it. When actually scoring, this is obviously not desirable, as it opens up a massive security hole.

- **Can this be used on the internet?** - Alone, no. The normal operating scenario for this system is for it to be running on a server on a LAN only. In other words, this should NOT be used on the internet, as the internal server is not robust enough for that application.

## Changelog
* Ver. α 0.21
  - Fixed a bug which caused the judge's page to render incorrectly.
* Ver. α 0.2
  - Switch the position of the "Add Judge" and "Add Team" buttons.
  - Make it so that a judge cannot be added unless at least one team is added.
  - Make it so that team names cannot be empty.
* Ver. α 0.1
  - Initial commit.

## To-do
- Add in a failover message in the event that the session expires on the judge's page.
- Add the ability of the scoring page to know when all scores have been entered for a given question.
- Remove "2" as a valid score.
- Make the judge's page exportable as CSV.
- Make the total page exportable as a cleaned HTML table.
- Separate questions by round.
- Make it so that the entire database can be exported as CSV in case of score challengers.

## License
[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
