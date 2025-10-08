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
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    favorites = db.relationship('Favorite', backref='recipe', lazy=True)
    ratings = db.relationship('Rating', backref='recipe', lazy=True)
    uploader = db.relationship('User', foreign_keys=[uploaded_by], backref='uploaded_recipes')

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

@app.route('/upload-recipe', methods=['GET', 'POST'])
@login_required
def upload_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        prep_time = int(request.form['prep_time'])
        image_url = request.form.get('image_url', 'https://via.placeholder.com/400x300?text=Recipe')
        
        # Validation
        if not name or not ingredients or not instructions:
            flash('Please fill in all required fields!', 'danger')
            return redirect(url_for('upload_recipe'))
        
        new_recipe = Recipe(
            name=name,
            ingredients=ingredients,
            instructions=instructions,
            prep_time=prep_time,
            image_url=image_url,
            uploaded_by=session['user_id']
        )
        
        db.session.add(new_recipe)
        db.session.commit()
        
        flash('Recipe uploaded successfully!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=new_recipe.recipe_id))
    
    return render_template('upload_recipe.html')

@app.route('/all-recipes')
def all_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'newest')
    
    # Base query
    query = Recipe.query
    
    # Apply search filter
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Recipe.name.like(search_filter),
                Recipe.ingredients.like(search_filter)
            )
        )
    
    # Apply sorting
    if sort_by == 'oldest':
        query = query.order_by(Recipe.recipe_id.asc())
    elif sort_by == 'name':
        query = query.order_by(Recipe.name.asc())
    elif sort_by == 'time':
        query = query.order_by(Recipe.prep_time.asc())
    else:  # newest (default)
        query = query.order_by(Recipe.recipe_id.desc())
    
    recipes = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('all_recipes.html', recipes=recipes)

@app.route('/my-recipes')
@login_required
def my_recipes():
    # Get recipes uploaded by current user
    recipes = Recipe.query.filter_by(uploaded_by=session['user_id']).order_by(Recipe.recipe_id.desc()).all()
    return render_template('my_recipes.html', recipes=recipes)

@app.route('/edit-recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if user owns this recipe
    if recipe.uploaded_by != session['user_id']:
        flash('You can only edit your own recipes!', 'danger')
        return redirect(url_for('all_recipes'))
    
    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']
        recipe.prep_time = int(request.form['prep_time'])
        recipe.image_url = request.form.get('image_url', recipe.image_url)
        
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe.recipe_id))
    
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/delete-recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if user owns this recipe
    if recipe.uploaded_by != session['user_id']:
        flash('You can only delete your own recipes!', 'danger')
        return redirect(url_for('all_recipes'))
    
    # Delete associated favorites and ratings first
    Favorite.query.filter_by(recipe_id=recipe_id).delete()
    Rating.query.filter_by(recipe_id=recipe_id).delete()
    
    db.session.delete(recipe)
    db.session.commit()
    
    flash('Recipe deleted successfully!', 'info')
    return redirect(url_for('my_recipes'))

if __name__ == '__main__':
    app.run(debug=True)