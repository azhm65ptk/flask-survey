from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app=Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
RESPONSE='response'

@app.route("/")
def show_survey_start():
    """Select a survey."""

    return render_template("main.html", survey=survey)

@app.route('/begin',methods=['POST'])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSE]=[]
    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def handle_question():
    """saving response and redirect to next question."""
    
    #get the response choice/ from input name#'answer'
    choice =request.form['answer']

    #adding the response to the session
    response=session[RESPONSE]
    response.append(choice)
    session[RESPONSE]=response

    if(len(response)== len(survey.questions)):
        #they've answered all the questions! thank them
        return redirect('/complete')
    else: 
        return redirect(f"/questions/{len(response)}")

@app.route('/questions/<int:id>')
def show_question(id):
    """Display current question."""
    response= session.get(RESPONSE)

    if(response is None):
        return redirect('/')
    
    if(len(response)== len(survey.questions)):
        #they answered all the questions! so done!
        return redirect('/complete')

    if(len(response) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(response)}")

    question=survey.questions[id]
    return render_template('question.html',question=question, question_num=id)



@app.route('/complete')
def complete():
    """survey completed.Show completion page"""

    return render_template('completion.html')




    

