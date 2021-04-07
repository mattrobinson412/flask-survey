# necessary imports for the application.
from flask import (Flask, request, render_template, redirect, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey, surveys

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "fkdal324lhl0f042iaf"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


# variable that keeps track of the user's responses.


#
@app.route('/')
def home_page():
    """render a page that shows the user the title, instructions, and a button to start surveys."""
    name = satisfaction_survey.title
    directions = satisfaction_survey.instructions
    return render_template('home.html', title=name, instructions=directions)


@app.route('/start', methods=["GET", "POST"])
def start_survey():
    """Begins survey when user is ready and clears responses."""
    session['responses'] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["GET", "POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:q>')
def survey_questions(q):
    """renders the question for the survey chosen by the user on the homepage."""

    responses = session['responses']

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != q):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {q}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[q]
    return render_template("question.html", question_num=q, question=question)
    

@app.route('/complete')
def completed_survey():
    """Renders the completed page and thanks the user for completing the survey."""

    return render_template('complete.html')