from flask import Flask, render_template, request, redirect, session, flash, url_for
import uuid
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ------------------------ Mock Databases ------------------------
mock_users = {}         # { email: hashed_password }
mock_bookings = []      # list of dicts for bookings

mock_movies = {
    "1": {
        "title": "End game: Avengers",
        "image": "Avengers.jpg",
        "rating": "9.2/10",
        "duration": "3h 13m",
        "genre": "Crime / Thriller",
        "price": 145
    },
    "2": {
        "title": "The Dark Knight",
        "image": "The Dark Knight.jpg",
        "rating": "9.0/10",
        "duration": "152 minutes",
        "genre": "Action, Crime, Drama",
        "price": 150
    },
    "3": {
        "title": "Inception",
        "image": "inception.jpg",
        "rating": "8.8/10",
        "duration": "148 minutes",
        "genre": "Action, Sci-Fi, Thriller",
        "price": 155
    }
}

@app.route('/booking')
def booking_page():
    if 'user' not in session:
        return redirect('/login')
    movie = request.args.get('movie', 'Sample Movie')
    return render_template('booking_form.html', movie=movie)


# ------------------------ Routes ------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


# ------------------------ Authentication ------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if email in mock_users:
            flash("Email already registered.")
            return redirect('/register')

        mock_users[email] = password
        flash("Registered successfully! Please log in.")
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if mock_users.get(email) == password:
            session['user'] = email
            flash("Login successful!")
            return redirect('/home')
        else:
            flash("Invalid credentials.")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect('/login')


# ------------------------ Main Pages ------------------------

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('home.html', user=session['user'], movies=mock_movies)

def send_mock_email(email, movie, date, time, seat, booking_id):
    print(f"""
    EMAIL SENT TO: {email}
    Booking Confirmed:
    Movie: {movie}
    Date: {date}
    Time: {time}
    Seat: {seat}
    Booking ID: {booking_id}
    """)




@app.route('/book', methods=['POST'])
def book_ticket():
    if 'user' not in session:
        return redirect('/login')

    booking = {
        'Email': session['user'],
        'Movie': request.form['movie'],
        'Date': request.form['date'],
        'Time': request.form['time'],
        'Seat': request.form['seat'],
        'BookingID': str(uuid.uuid4())
    }

    mock_bookings.append(booking)

    # ✅ Correct function name here
    send_mock_email(
        booking['Email'],
        booking['Movie'],
        booking['Date'],
        booking['Time'],
        booking['Seat'],
        booking['BookingID']
    )

    return render_template('tickets.html', booking=booking)

    if 'user' not in session:
        return redirect('/login')
    booking = {
        'Email': session['user'],
        'Movie': request.form['movie'],
        'Date': request.form['date'],
        'Time': request.form['time'],
        'Seat': request.form['seat'],
        'BookingID': str(uuid.uuid4())
    }
    mock_bookings.append(booking)
    send_mock_email(booking['Email'], booking['Movie'], booking['Date'], booking['Time'], booking['Seat'], booking['BookingID'])
    return render_template('tickets.html', booking=booking)

    if 'user' not in session:
        return redirect('/login')

    movie = request.form['movie']
    seats = request.form['seats']
    time = request.form['time']
    price = 145  # Or fetch based on movie

    booking = {
        'Email': session['user'],
        'Movie': movie,
        'Seat': seats,
        'Time': time,
        'Date': '2025-07-01',
        'BookingID': str(uuid.uuid4())
    }

    mock_bookings.append(booking)

    print(f"EMAIL SENT TO {booking['Email']}: Movie {booking['Movie']} on {booking['Date']} at {booking['Time']} | Seats: {booking['Seat']}")

    flash("Booking successful!")
    return redirect('/tickets')


@app.route('/tickets')
def tickets():   # ✅ This matches the HTML now
    if 'user' not in session:
        return redirect('/login')

    user_bookings = [b for b in mock_bookings if b['Email'] == session['user']]
    if not user_bookings:
        flash("No bookings found.")
        return redirect('/home')

    return render_template('tickets.html', booking=user_bookings[-1])




# ------------------------ Run App ------------------------

if __name__ == '__main__':
    app.run(debug=True)