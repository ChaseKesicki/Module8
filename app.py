# Importing the modules
# Render_template renders HTML, request handles form data
# Redirect and url_for direct users to a route in the website navigation
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Todo Model class
# Define the columns (attributes) for the class
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, default=None)  # Nullable for uncompleted games
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Add the repr method
    # This is a special Python method that returns
    # a string representing the object
    def __repr__(self):
        return f'<Game id={self.id} title={self.title} completed={self.completed} rating={self.rating}>'

# Create the database and table to hold the "To Do"s
with app.app_context():
    db.create_all()

# Create a home route that displays the To Do list
@app.route('/')
def index():
    games = Game.query.order_by(Game.created_at.desc()).all()
    return render_template('index.html', todos=todos)

# Create a route for adding a new Game to the database
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_game = Game(title=title)
        db.session.add(new_game)
        db.session.commit()
    return redirect(url_for('index'))

# Create a route to mark a Game as completed
@app.route('/toggle/<int:game_id>')
def toggle(game_id):
    game = Game.query.get_or_404(game_id)
    game.completed = not game.completed
    db.session.commit()
    return redirect(url_for('index'))

# Create a route to delete a Game item
@app.route('/delete/<int:game_id>')
def delete(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))
# Create a route to rate a Game item out of 5 stars
@app.route('/rate/<int:game_id>', methods=['POST'])
def rate(game_id):
    game = Game.query.get_or_404(game_id)
    if game.completed:
        rating = request.form.get('rating')
        if rating.isdigit() and 1 <= int(rating) <= 5:
            game.rating = int(rating)
            db.session.commit()
    return redirect(url_for('index'))

# Start the Flask app in debug mode
# Flask provides a debugger & shows the stack trace if an error occurs
# Debug mode also reloads the page if you change the
# code so you don't need to restart the server.
if __name__ == '__main__':
    app.run(debug=True)