import datetime
import uuid
from flask import render_template,request,redirect,url_for,current_app,Blueprint

pages = Blueprint("habits",__name__,template_folder="templates",static_folder="static")

@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start+datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    return {"date_range":date_range}

def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()
    habits_on_date = current_app.db.habitcollection.find({"added":{"$lte":selected_date}})
    completions = [
        habit["habit"]
        for habit in current_app.db.habitcollection.find({"date": selected_date})
    ]
    return render_template("index.html",selected_date=selected_date,
                           completions=completions,
                            Habits=habits_on_date)

@pages.route("/add", methods=["GET","POST"])
def add():
    today = today_at_midnight()
    if request.method == "POST":
        habit = request.form.get("habit")
        current_app.db.habitcollection.insert_one({"_id":uuid.uuid4().hex, "added":today, "name":habit})
    return render_template("habit.html",selected_date=today)

@pages.route("/complete",methods=["POST","GET"])
def complete():
    date_str = request.form.get("date")
    habit = request.form.get("Habitid")
    date = datetime.datetime.fromisoformat(date_str)
    current_app.db.habitcollection.insert_one({"date":date, "habit":habit})
    return redirect(url_for("habits.index", date=date_str))

