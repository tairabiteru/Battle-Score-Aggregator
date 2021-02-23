"""
Main routing module.

This file contains the 'meat 'n' potatoes' as it were. It defines all of the
"subdirectories" of the webserver, as well as the actions required on behalf
of the server whenever one of these pages is accessed.
"""

from dash.conf import conf
from orm.judge import Judge, JudgeNotFound, JudgeExists
from orm.team import TeamExists

from aiohttp import web
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from datetime import datetime
from passlib.hash import bcrypt
import uuid


# Routing table
routes = web.RouteTableDef()


async def get_user(request, redirect=True):
    """
    Obtain the current user from the session. If none exists, redirect to login.
    Whether or not the function redirects is controlled by the kwarg, as
    sometimes this is not desirable.
    """
    session = await get_session(request)
    try:
        user = session['username']
        sessionID = session['ID']
        if sessionID != Judge.obtain(user).sessionID:
            raise KeyError
        return session['username']
    except KeyError:
        if redirect:
            session['redirect'] = str(request.rel_url)
            raise web.HTTPFound("/login")
        raise web.HTTPUnauthorized


@routes.get("/")
@template("index.html")
async def index_GET(request):
    """Handle GET requests for /."""
    return {}


@routes.get("/judge")
@template("judge.html")
async def judge_GET(request):
    """Handle GET requests for /judge."""
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
    """
    Handle POST requests for /login.

    A POST request is sent from /login when the user actually tries to log in.
    Thus, we need to validate their password entry, then redirect them
    to the appropriate page. We also check here to see if a judge is already
    logged in elsewhere, since under this system, we do not permit multiple
    logins, as it could cause data collisions.
    """
    session = await get_session(request)
    post = await request.post()

    username = post.get("username")
    password = post.get("password")

    # Validate username
    try:
        judge = Judge.obtain(username)
    except JudgeNotFound:
        return {'response': f"No user named '{username}' exists."}

    # Validate password entry
    if not bcrypt.verify(password, judge.password):
        return {'response': "Invalid password."}

    # Check for existing logins.
    if judge.loggedIn:
        return {'response': f"Judge is already logged in elsewhere. If you've just logged out, try waiting {conf.loginTimeout} seconds, then try again."}

    # Login successful, set session and server-side session info.
    session['username'] = judge.username
    sessionID = uuid.uuid4().hex
    session['ID'] = sessionID
    judge.sessionID = sessionID
    judge.save()

    # If a redirect was specified in their session, redirect to that page.
    # Otherwise, redirect to /judge.
    try:
        raise web.HTTPFound(session['redirect'])
    except KeyError:
        raise web.HTTPFound("/judge")
    return {'response': ''}


@routes.get("/total")
@template("total.html")
async def total_GET(request):
    """Handle GET requests for /total"""
    return {'placement': Judge.placement(), 'judges': Judge.obtainall()}


@routes.get("/export")
@template("export.html")
async def export_GET(request):
    """Handle GET requests for /export"""
    return {'placement': Judge.placement(), 'judges': Judge.obtainall()}


# Pages prefixed with /api/ are all pages which are not meant to be accessed
# directly. Instead, they allow JS to communicate with the server behind the
# scenes using AJAX.

@routes.get("/api/total")
async def total(request):
    """Handle AJAX requests for /total"""
    return web.json_response(Judge.placement())


@routes.post("/api/save-scores")
async def api_saveScores_POST(request):
    """
    Handle AJAX requests for /judge.

    This handles AJAX requests which are sent whenever a score is saved.
    """
    username = await get_user(request, redirect=False)

    judge = Judge.obtain(username)
    data = await request.json()

    # lol Solomon would *love* this.
    for round, questions in data.items():
        for qnumber, answers in questions.items():
            for teamname, answer in answers.items():
                for i, team in enumerate(judge.teams):
                    if team.name == teamname:
                        judge.teams[i].rounds[round][qnumber] = answer
    judge.save()
    return web.Response(text="success")


@routes.get("/api/update-judge")
async def api_updateJudge_GET(request):
    """Handle AJAX requests for /api/judge-update"""
    judges = {}
    for judge in Judge.obtainall():
        judges[judge.username] = {}
        judges[judge.username]['lastScored'] = f"Q{judge.lastQuestionScored}"
        judges[judge.username]['helpFlag'] = judge.helpFlag
        judges[judge.username]['loggedIn'] = judge.loggedIn

    return web.json_response({'allUnscored': Judge.allUnscoredQuestions(), 'judges': judges})


@routes.post("/api/heartbeat")
async def api_heartbeat_POST(request):
    username = await get_user(request, redirect=False)
    judge = Judge.obtain(username)
    judge.lastHeartbeat = datetime.now()
    judge.save()
    return web.Response(text="success")


@routes.post("/api/help-request")
async def api_saveScores_POST(request):
    """Handle AJAX requests for /api/help-request"""
    username = await get_user(request, redirect=False)

    judge = Judge.obtain(username)
    data = await request.json()
    judge.helpFlag = data['helpFlag']
    judge.save()
    return web.Response(text="success")


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
