# Importing the frameworks

from flask import *
import database

user_details = {}
session = {}
page = {}

# Initialise the application
app = Flask(__name__)
app.secret_key = 'aab12124d346928d14710610f'


#####################################################
##  INDEX
#####################################################

@app.route('/')
def index():
    # Check if the user is logged in
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['title'] = 'Brisbane Olympics System'
    
    return redirect(url_for('list_event'))

    #return render_template('index.html', session=session, page=page, user=user_details)

#####################################################
##  LOGIN
#####################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Check if they are submitting details, or they are just logging in
    if (request.method == 'POST'):
        # submitting details
        login_return_data = check_login(request.form['id'], request.form['password'])

        # If they have incorrect details
        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect login info, please try again.")
            return redirect(url_for('login'))

        # Log them in
        page['bar'] = True
        strtest = 'Welcome back, ' + login_return_data['first_name'] + ' ' + login_return_data['last_name']
        flash(strtest)
        session['logged_in'] = True

        # Store the user details
        global user_details
        user_details = login_return_data
        return redirect(url_for('index'))

    elif (request.method == 'GET'):
        return(render_template('login.html', page=page))

#####################################################
##  LOGOUT
#####################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out. See you soon!')
    return redirect(url_for('index'))

#####################################################
##  LIST EVENT
#####################################################

@app.route('/list_event', methods=['POST', 'GET'])
def list_event():
    # Check if user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # User is just viewing the page
    if (request.method == 'GET'):
        # First check if specific event
        event_list = database.findEventsByOfficial(user_details['official_id'])
        if (event_list is None):
            event_list = []
            flash("There are no events in our system for official " + user_details['first_name'] + " " + user_details['last_name'])
            page['bar'] = False
        return render_template('event_list.html', event=event_list, session=session, page=page)

    # Otherwise try to get from the database
    elif (request.method == 'POST'):
        search_term = request.form['search']
        if (search_term == ''):
            event_list_find = database.findEventsByOfficial(user_details['official_id'])
        else:    
            event_list_find = database.findEventsByCriteria(search_term)
        if (event_list_find is None):
            event_list_find = []
            flash("Event \'{}\' does not exist for user ".format(request.form['search']) + user_details['username'])
            page['bar'] = False
        return render_template('event_list.html', event=event_list_find, session=session, page=page)

#####################################################
##  Add Event
#####################################################

@app.route('/new_event' , methods=['GET', 'POST'])
def new_event():
    # Check if the user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # If we're just looking at the 'new event' page
    if(request.method == 'GET'):
        times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        return render_template('new_event.html', user=user_details, times=times, session=session, page=page)

	# If we're adding a new event
    success = database.addEvent(request.form['event_name'],
                                 request.form['sport'],
                                 request.form['referee'],
                                 request.form['judge'],
                                 request.form['medal_giver'])
    if(success == True):
        page['bar'] = True
        flash("Event added!")
        return(redirect(url_for('index')))
    else:
        page['bar'] = False
        flash("There was an error adding a new event")
        return(redirect(url_for('new_event')))

#####################################################
## Update Event
#####################################################
@app.route('/update_event', methods=['GET', 'POST'])
def update_event():
    # Check if the user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # Get the event ID
    event_id = request.args.get('event_id')

    # Get the event details
    event_results = get_event(event_id, user_details['official_id'])

    # If we're just looking at the 'update event' page
    if (request.method == 'GET'):
        # If event details cannot be retrieved
        if event_results is None:
            event_results = []
		    # Do not allow viewing if there is no event to update
            page['bar'] = False
            flash("You do not have access to update that record!")
            return(redirect(url_for('index')))

	    # Otherwise, if event details can be retrieved
        times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        return render_template('update_event.html', eventInfo=event_results, user=user_details, times=times, session=session, page=page)

    # If we're updating event
    success = database.updateEvent(request.form['event_id'],
                                request.form['event_name'],
                                request.form['sport'],
                                request.form['referee'],
                                request.form['judge'],
                                request.form['medal_giver'])
    if (success == True):
        page['bar'] = True
        flash("Event record updated!")
        return(redirect(url_for('index')))
    else:
        page['bar'] = False
        flash("There was an error updating the event")
        return(redirect(url_for('index')))

def get_event(event_id, official_id):
    for event in database.findEventsByOfficial(official_id):
        if event['event_id'] == event_id:
            return event
    return None

def check_login(username, password):
    userInfo = database.checkUserCredentials(username, password)

    if userInfo is None:
        return None
    else:
        tuples = {
            'official_id': userInfo[0],
            'username': userInfo[1],
            'first_name': userInfo[2],
            'last_name': userInfo[3],
            'password': userInfo[4],
        }
        return tuples
