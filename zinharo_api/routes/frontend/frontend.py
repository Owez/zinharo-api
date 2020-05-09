from flask import Blueprint, render_template, request

frontend_blueprint = Blueprint("frontend", __name__)

@frontend_blueprint.route("/")
def index():
    """Index website route"""

    return render_template("index.html")


@frontend_blueprint.route("/server")
def server():
    """Server donation ad page"""

    return render_template("server.html")


@frontend_blueprint.route("/notice")
def notice():
    """Notice/disclaimer on misuse"""

    return render_template("notice.html")

@frontend_blueprint.route("/admin")
def hackjoke():
    """Call potential hackers out"""

    return render_template("hackjoke.html")

@frontend_blueprint.route("/contact")
def contact():
    """Contact page"""

    return render_template("contact.html")


@frontend_blueprint.route("/cap/<id>")
def cap_detail(id: int):
    """Detail for a specific cap"""

    return render_template("cap.html", id=id)
