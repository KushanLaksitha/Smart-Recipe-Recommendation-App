# 🍳 Smart Recipe Recommendation App

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

A web application that uses AI to recommend recipes based on available ingredients, helping users reduce food waste and discover new meals.

---

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)
*Landing page with hero section and feature highlights*

### Recipe Search (AI-Powered)
![Search Page](screenshots/search.png)
*Enter your available ingredients and get AI-powered recipe recommendations*

### Search Results
![Results Page](screenshots/results.png)
*View matching recipes with AI similarity scores*

### Recipe Detail
![Recipe Detail](screenshots/recipe-detail.png)
*Complete recipe information with ingredients, instructions, and ratings*

### Browse All Recipes
![Browse Recipes](screenshots/browse.png)
*Explore all recipes with search, filter, and pagination*

### Upload Recipe
![Upload Recipe](screenshots/upload.png)
*Share your own recipes with the community*

### My Recipes Dashboard
![My Recipes](screenshots/my-recipes.png)
*Manage your uploaded recipes - edit and delete*

### Favorites Dashboard
![Favorites](screenshots/favorites.png)
*Save and organize your favorite recipes*

---

## ✨ Features

### 🔐 User Authentication
- Secure user registration and login
- Password hashing with Werkzeug
- Session management
- Protected routes

### 🤖 AI-Powered Recipe Matching
- **TF-IDF Vectorization** - Converts ingredients to numerical vectors
- **Cosine Similarity** - Calculates ingredient match percentage
- Smart ingredient matching algorithm
- Real-time similarity scoring

### 📤 Recipe Management
- **Upload Recipes** - Share your culinary creations
- **Edit Recipes** - Update your recipes anytime
- **Delete Recipes** - Remove recipes you've uploaded
- **Browse All** - Explore community recipes
- **My Recipes** - Manage your contributions

### ❤️ Favorites System
- Save recipes you love
- Quick access from dashboard
- Remove favorites easily

### ⭐ Ratings & Reviews
- Rate recipes 1-5 stars
- Leave comments and reviews
- View average ratings
- See what others think

### 🔍 Advanced Search & Filters
- Search by name or ingredients
- Sort by: Newest, Oldest, Name, Prep Time
- Pagination for easy browsing
- Real-time search

### 📱 Responsive Design
- Mobile-first approach
- Works on all devices
- Touch-friendly interface
- Adaptive layouts

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.8+ | Core programming language |
| Flask | 3.0.0 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM for database |
| PyMySQL | 1.1.0 | MySQL connector |
| Scikit-learn | 1.3.2 | Machine learning (AI) |
| Werkzeug | 3.0.1 | Security utilities |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| HTML5 | - | Structure |
| CSS3 | - | Styling |
| JavaScript (ES6+) | - | Interactivity |
| Bootstrap | 5.3.0 | UI framework |
| Bootstrap Icons | 1.11.0 | Icons |

### Database
- **MySQL 5.7+** - Relational database

### AI/ML
- **TF-IDF Vectorizer** - Text feature extraction
- **Cosine Similarity** - Similarity measurement

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.8 or higher
- ✅ MySQL Server 5.7 or higher
- ✅ pip (Python package manager)
- ✅ Virtual environment (recommended)

---

## 🚀 Installation Guide

### Step 1: Clone or Download Project

```bash
git clone https://github.com/yourusername/smart-recipe-app.git
cd smart-recipe-app
```

Or download and extract the ZIP file.

### Step 2: Create Project Structure

```
smart-recipe-app/
├── app.py
├── seed.py
├── requirements.txt
├── database.sql
├── database_upgrade.sql
├── README.md
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── search.html
│   ├── results.html
│   ├── recipe.html
│   ├── dashboard.html
│   ├── all_recipes.html
│   ├── upload_recipe.html
│   ├── edit_recipe.html
│   └── my_recipes.html
└── screenshots/
    └── (add your screenshots here)
```

### Step 3: Set Up Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Install & Configure MySQL

**Windows:**
- Download from [mysql.com](https://dev.mysql.com/downloads/installer/)
- Install and set root password
- Start MySQL service

**Mac:**
```bash
brew install mysql
brew services start mysql
```

**Linux:**
```bash
sudo apt-get install mysql-server
sudo systemctl start mysql
```

### Step 6: Create Database

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE recipe_db;
exit;
```

Or import the SQL file:
```bash
mysql -u root -p < database.sql
```

### Step 7: Run Database Upgrade

```bash
mysql -u root -p recipe_db < database_upgrade.sql
```

### Step 8: Configure Database Connection

Open `app.py` and update line 9:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/recipe_db'
```

Replace `YOUR_PASSWORD` with your MySQL root password.

### Step 9: Initialize Database

```bash
python seed.py
```

### Step 10: Run the Application

```bash
python app.py
```

Open your browser and visit:
```
http://localhost:5000
```

---

## 📖 Usage Guide

### 1️⃣ Register an Account
1. Click "Get Started" or "Register"
2. Enter username, email, and password
3. Click "Register"

### 2️⃣ Search for Recipes (AI-Powered)
1. Log in to your account
2. Click "Search Recipes"
3. Enter ingredients you have (comma-separated)
   - Example: `chicken, tomatoes, garlic, onions, pasta`
4. Click "Find Recipes"
5. View results with AI match percentages

### 3️⃣ Browse All Recipes
1. Click "Browse All" in navigation
2. Use search box to find specific recipes
3. Sort by: Newest, Oldest, Name, or Prep Time
4. Navigate through pages

### 4️⃣ Upload Your Own Recipe
1. Click "Upload Recipe"
2. Fill in the form:
   - Recipe name
   - Ingredients (comma-separated)
   - Step-by-step instructions
   - Prep time (minutes)
   - Image URL (optional)
3. Click "Upload Recipe"

### 5️⃣ Manage Your Recipes
1. Click "My Recipes"
2. View all your uploaded recipes
3. Click "Edit" to modify
4. Click "Delete" to remove (with confirmation)

### 6️⃣ Save Favorites
1. View any recipe
2. Click the ❤️ heart icon
3. Access from "My Favorites"

### 7️⃣ Rate & Review
1. Open a recipe detail page
2. Select rating (1-5 stars)
3. Add optional comment
4. Click "Submit Rating"

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Recipes Table
```sql
CREATE TABLE recipes (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    image_url VARCHAR(255),
    prep_time INT,
    uploaded_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);
```

### Favorites Table
```sql
CREATE TABLE favorites (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    UNIQUE(user_id, recipe_id)
);
```

### Ratings Table
```sql
CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    UNIQUE(user_id, recipe_id)
);
```

---

## 🧠 How the AI Works

### TF-IDF (Term Frequency-Inverse Document Frequency)

The app uses TF-IDF to convert text (ingredients) into numerical vectors:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(recipe_ingredients)
```

**What it does:**
- Converts ingredient lists to numerical vectors
- Gives more weight to unique ingredients
- Reduces weight of common ingredients

### Cosine Similarity

Measures similarity between user ingredients and recipe ingredients:

```python
from sklearn.metrics.pairwise import cosine_similarity

similarities = cosine_similarity(user_vector, recipe_vectors)
```

**Similarity Score:**
- 100% = Perfect match (all ingredients present)
- 75%+ = Very good match
- 50-75% = Good match
- Below 50% = Partial match

### Example:

**User has:** `chicken, tomatoes, garlic, onions`

**Recipe 1:** `chicken, tomatoes, garlic, onions, pasta, olive oil`
- **Match: 85%** (4 out of 6 ingredients match)

**Recipe 2:** `beef, potatoes, carrots, onions`
- **Match: 25%** (1 out of 4 ingredients match)

Result: Recipe 1 is recommended first!

---

## 🎨 Customization

### Change Colors

Edit `static/css/style.css`:

```css
:root {
    --primary-color: #667eea;    /* Change to your color */
    --secondary-color: #764ba2;  /* Change to your color */
}
```

### Add More Sample Recipes

```sql
INSERT INTO recipes (name, ingredients, instructions, image_url, prep_time) 
VALUES (
    'Your Recipe Name',
    'ingredient1, ingredient2, ingredient3',
    '1. Step one. 2. Step two. 3. Step three.',
    'https://example.com/image.jpg',
    30
);
```

### Change App Name

Update in these files:
- `templates/base.html` (navbar and title)
- All template page titles
- `README.md`

---

## 🔧 Troubleshooting

### Database Connection Error
```
Error: Access denied for user 'root'
```
**Solution:** Update password in `app.py` line 9

### Missing Column Error
```
Error: Unknown column 'uploaded_by'
```
**Solution:** Run `database_upgrade.sql`

### Module Not Found
```
Error: No module named 'flask'
```
**Solution:** 
```bash
pip install -r requirements.txt
```

### Port Already in Use
```
Error: Address already in use
```
**Solution:** Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

