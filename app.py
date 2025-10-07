from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    prep_time = db.Column(db.Integer)
    favorites = db.relationship('Favorite', backref='recipe', lazy=True)
    ratings = db.relationship('Rating', backref='recipe', lazy=True)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)

class Rating(db.Model):
    __tablename__ = 'ratings'
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# AI Recipe Matcher
def match_recipes(user_ingredients, top_n=5):
    recipes = Recipe.query.all()
    if not recipes:
        return []
    
    recipe_texts = [r.ingredients.lower() for r in recipes]
    recipe_texts.append(user_ingredients.lower())
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(recipe_texts)
    
    user_vector = tfidf_matrix[-1]
    recipe_vectors = tfidf_matrix[:-1]
    
    similarities = cosine_similarity(user_vector, recipe_vectors)[0]
    top_indices = np.argsort(similarities)[::-1][:top_n]
    
    matched_recipes = []
    for idx in top_indices:
        if similarities[idx] > 0:
            matched_recipes.append({
                'recipe': recipes[idx],
                'score': round(similarities[idx] * 100, 2)
            })
    
    return matched_recipes

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    favorites = Favorite.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', favorites=favorites)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        matched_recipes = match_recipes(ingredients)
        return render_template('results.html', recipes=matched_recipes, query=ingredients)
    
    return render_template('search.html')

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
    avg_rating = sum([r.rating for r in ratings]) / len(ratings) if ratings else 0
    
    is_favorite = False
    if 'user_id' in session:
        is_favorite = Favorite.query.filter_by(
            user_id=session['user_id'], 
            recipe_id=recipe_id
        ).first() is not None
    
    return render_template('recipe.html', recipe=recipe, avg_rating=avg_rating, 
                         ratings=ratings, is_favorite=is_favorite)

@app.route('/favorite/<int:recipe_id>')
@login_required
def toggle_favorite(recipe_id):
    favorite = Favorite.query.filter_by(
        user_id=session['user_id'], 
        recipe_id=recipe_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        flash('Recipe removed from favorites!', 'info')
    else:
        new_favorite = Favorite(user_id=session['user_id'], recipe_id=recipe_id)
        db.session.add(new_favorite)
        flash('Recipe added to favorites!', 'success')
    
    db.session.commit()
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/rate/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    rating_value = int(request.form['rating'])
    comment = request.form.get('comment', '')
    
    existing_rating = Rating.query.filter_by(
        user_id=session['user_id'], 
        recipe_id=recipe_id
    ).first()
    
    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.comment = comment
    else:
        new_rating = Rating(
            user_id=session['user_id'], 
            recipe_id=recipe_id, 
            rating=rating_value, 
            comment=comment
        )
        db.session.add(new_rating)
    
    db.session.commit()
    flash('Rating submitted!', 'success')
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

if __name__ == '__main__':
    app.run(debug=True)