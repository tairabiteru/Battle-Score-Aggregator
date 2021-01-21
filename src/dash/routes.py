"""Main routing file."""

from dash.conf import conf
from orm.judge import Judge, JudgeNotFound, JudgeExists
from orm.team import TeamExists

from aiohttp import web
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from passlib.hash import bcrypt


routes = web.RouteTableDef()


async def get_user(request):
    """Obtain the current user from the session. If none exists, redirect to login."""
    session = await get_session(request)
    try:
        return session['username']
    except KeyError:
        session['redirect'] = str(request.rel_url)
        raise web.HTTPFound("/login")


@routes.get("/")
@template("index.html")
async def index_GET(request):
    """Handle GET requests for /"""
    return {}


@routes.get("/judge")
@template("judge.html")
async def judge_GET(request):
    """Handle GET requests for /judge"""
    username = await get_user(request)
    judge = Judge.obtain(username)
    return {'judge': judge}


@routes.get("/login")
@template("login.html")
async def login_GET(request):
    """Handle GET requests for /login"""
    return {}


@routes.post("/login")
@template("login.html")
async def login_POST(request):
    """Handle POST requests for /login"""
    session = await get_session(request)
    post = await request.post()

    username = post.get("username")
    password = post.get("password")

    try:
        judge = Judge.obtain(username)
    except JudgeNotFound:
        return {'response': f"No user named '{username}' exists."}
    if not bcrypt.verify(password, judge.password):
        return {'response': "Invalid password."}

    session['username'] = judge.username

    try:
        raise web.HTTPFound(session['redirect'])
    except KeyError:
        raise web.HTTPFound("/judge")

    return {'response': ''}


@routes.get("/total")
@template("total.html")
async def total_GET(request):
    """Handle GET requests for /total"""
    return {'placement': Judge.placement()}


@routes.get("/api/total")
async def total(request):
    """Handle AJAX requests for /total"""
    return web.json_response(Judge.placement())


@routes.post("/api/save-scores")
async def api_saveScores_POST(request):
    """Handle AJAX requests for /judge"""
    username = await get_user(request)

    judge = Judge.obtain(username)
    data = await request.json()

    for s, scores in enumerate(data):
        for t, team in enumerate(judge.teams):
            try:
                judge.teams[t].questions[str(s+1)] = int(scores[t])
            except ValueError:
                if scores[t] == "":
                    judge.teams[t].questions[str(s+1)] = ""
                else:
                    raise
    judge.save()
    return web.Response(text="Playlist successfully deleted.")


# Admin is only enabled if setting say so.
if conf.adminEnabled:
    @routes.get("/admin")
    @template("admin.html")
    async def admin_get(request):
        """Handle GET requests for /admin"""
        judges = Judge.obtainall()
        return {'judges': judges}

    @routes.post("/admin")
    @template("admin.html")
    async def admin_POST(request):
        """Handle POST requests for /admin"""
        post = await request.post()

        username = post.get("username")
        password = bcrypt.hash(post.get("password"))
        judges = Judge.obtainall()

        teams = []
        for key, value in post.items():
            if key.startswith("team"):
                if not value:
                    return {'judges': judges, 'response': 'Team names cannot be empty.'}
                teams.append(value)

        if not teams:
            return {'judges': judges, 'response': 'You must specify at least one team per judge.'}

        try:
            Judge.create(username, password, teams)
            return {'judges': judges, 'response': 'Judge successfully created.'}
        except JudgeExists:
            return {'judges': judges, 'response': f"A judge named '{username}' already exists."}
        except TeamExists as e:
            return {'judges': judges, 'response': f"A team named '{e.team}' already exists."}

else:
    @routes.get("/admin")
    async def admin_get(request):
        """Handle GET requests for admin, even if disabled."""
        return web.Response(text="The admin interface is disabled.")
