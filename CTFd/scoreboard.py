from flask import Blueprint, render_template
from collections import OrderedDict

from CTFd.utils import config, get_config
from CTFd.utils.config.visibility import scores_visible
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_infos
from CTFd.utils.scores import get_standings
from CTFd.utils.user import is_admin
from CTFd.utils.countries import get_countries
from CTFd.models import Teams, db

scoreboard = Blueprint("scoreboard", __name__)

OVERALL = "Overall"

@scoreboard.route("/scoreboard")
@check_account_visibility
@check_score_visibility
def listing():
    infos = get_infos()

    if config.is_scoreboard_frozen():
        infos.append("Scoreboard has been frozen")

    if is_admin() is True and scores_visible() is False:
        infos.append("Scores are not currently visible to users")

    standings = get_standings()

    user_mode = get_config("user_mode")
    if user_mode == "teams":

        # Create an ordered list of team region buckets (so that they could be rendered East to West on the screen)
        buckets = OrderedDict()
        buckets[OVERALL] = []

        # We hijacked "country" field to mean "region"
        for region in get_countries():
            buckets[region] = []

        for team in standings:
            buckets[OVERALL].append(team)

            # Throw away any team with an invalid region, they will have to set the right region in the team settings
            # in order to show up in the right scoreboard region (note that once they change the region, for some 
            # reason it takes a bit of time to be reflected in the scoreboard)
            if team.country not in buckets or team.country == OVERALL:
                continue
            buckets[team.country].append(team)

        return render_template("scoreboard.html", buckets=buckets, infos=infos)
    
    else:
        return render_template("scoreboard.html", standings=standings, infos=infos)
