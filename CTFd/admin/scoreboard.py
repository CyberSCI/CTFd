from flask import render_template
from collections import OrderedDict
from CTFd.admin import admin
from CTFd.utils.config import is_teams_mode
from CTFd.utils.countries import get_countries
from CTFd.utils.decorators import admins_only
from CTFd.utils.scores import get_standings, get_user_standings

OVERALL = "Overall"


@admin.route("/admin/scoreboard")
@admins_only
def scoreboard_listing():
    standings = get_standings(admin=True)
    user_standings = get_user_standings(admin=True) if is_teams_mode() else None

    if is_teams_mode():

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

        return render_template("admin/scoreboard.html", buckets=buckets)
    else:
        return render_template("admin/scoreboard.html", standings=standings)


    return render_template(
        "admin/scoreboard.html", standings=standings, user_standings=user_standings
    )
