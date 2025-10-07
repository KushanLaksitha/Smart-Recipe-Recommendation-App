# 🍳 Smart Recipe Recommendation App

A web application that uses AI to recommend recipes based on available ingredients, helping users reduce food waste and discover new meals.

## ✨ Features

- 🔐 **User Authentication**: Secure registration and login system
- 🤖 **AI Recipe Matching**: Intelligent ingredient-based recipe recommendations using TF-IDF and cosine similarity
- ❤️ **Favorites System**: Save and manage your favorite recipes
- ⭐ **Ratings & Reviews**: Rate recipes and share your cooking experience
- 📱 **Responsive Design**: Beautiful Bootstrap UI that works on all devices
- 🔍 **Smart Search**: Find recipes that match your available ingredients

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Backend**: Python Flask
- **Database**: MySQL
- **AI/ML**: Scikit-learn (TF-IDF Vectorizer, Cosine Similarity)
- **Authentication**: Werkzeug Security

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

Create a project directory and add all the files.

### 2. Install MySQL

**Windows:**
- Download MySQL from [mysql.com](https://dev.mysql.com/downloads/installer/)
- Run the installer and set up root password
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

### 3. Create Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE recipe_db;
```

Or import the provided `database.sql` file:

```bash
mysql -u root -p < database.sql
```

### 4. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Database Connection

Open `app.py` and update the database URI with your MySQL credentials:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/recipe_db'
```

Replace:
- `username` with your MySQL username (default: `root`)
- `password` with your MySQL password

### 7. Initialize Database Tables

```bash
python seed.py
```

This will create all necessary tables in your database.

### 8. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📁 Project Structure

```
project_root/
├── app.py                 # Main Flask application
├── seed.py               # Database initialization script
├── requirements.txt      # Python dependencies
├── database.sql          # SQL schema and sample data
├── templates/            # HTML templates
│   ├── base.html        # Base template with navbar
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── search.html      # Ingredient search page
│   ├── results.html     # Search results page
│   ├── recipe.html      # Recipe detail page
│   └── dashboard.html   # User favorites dashboard
└── static/              # CSS/JS files (optional)
```

## 📸 Screenshots

### 🏠 Home Page
![Home Page Screenshot](screenshots/home.png)

### 🔍 Recipe Search
![Search Screenshot](screenshots/search.png)

### 🤖 AI Recommendation
![AI Recommendation Screenshot](screenshots/ai_results.png)

### ❤️ Create Account
![Favorites Screenshot](screenshots/register.png)

## 💡 How to Use

### 1. Register an Account
- Navigate to the registration page
- Enter username, email, and password
- Click "Register"

### 2. Search for Recipes
- Log in to your account
- Click "Search Recipes"
- Enter your available ingredients (comma-separated)
- Example: `chicken, tomatoes, garlic, pasta, cheese`
- Click "Find Recipes"

### 3. View Recipe Details
- Click on any recipe card to see full details
- View ingredients, instructions, and preparation time
- See ratings and reviews from other users

### 4. Save Favorites
- Click the heart icon to add recipes to your favorites
- Access your saved recipes from "My Favorites"

### 5. Rate Recipes
- After viewing a recipe, submit your rating (1-5 stars)
- Optionally add a comment about your experience

## 🧠 How the AI Works

The app uses **TF-IDF (Term Frequency-Inverse Document Frequency)** with **Cosine Similarity** to match recipes:

1. User inputs their available ingredients
2. System converts all recipe ingredients into TF-IDF vectors
3. Calculates cosine similarity between user input and each recipe
4. Returns top matching recipes with similarity scores
5. Higher scores mean better ingredient matches

## 🗄️ Database Schema

### Users Table
| Field | Type | Description |
|-------|------|-------------|
| user_id | INT (PK) | Primary key |
| username | VARCHAR(100) | Unique username |
| email | VARCHAR(100) | User email |
| password | VARCHAR(255) | Hashed password |

### Recipes Table
| Field | Type | Description |
|-------|------|-------------|
| recipe_id | INT (PK) | Primary key |
| name | VARCHAR(255) | Recipe name |
| ingredients | TEXT | Comma-separated ingredients |
| instructions | TEXT | Cooking instructions |
| image_url | VARCHAR(255) | Recipe image URL |
| prep_time | INT | Preparation time in minutes |

### Favorites Table
| Field | Type | Description |
|-------|------|-------------|
| favorite_id | INT (PK) | Primary key |
| user_id | INT (FK) | References users.user_id |
| recipe_id | INT (FK) | References recipes.recipe_id |

### Ratings Table
| Field | Type | Description |
|-------|------|-------------|
| rating_id | INT (PK) | Primary key |
| user_id | INT (FK) | References users.user_id |
| recipe_id | INT (FK) | References recipes.recipe_id |
| rating | INT | Rating value (1-5) |
| comment | TEXT | Optional comment |

## 🔧 Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check username and password in `app.py`
- Ensure database `recipe_db` exists

### Import Errors
- Activate virtual environment
- Run `pip install -r requirements.txt` again

### Port Already in Use
- Change the port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

## 🎨 Customization Ideas

### Add More Features
- Image upload for ingredients detection
- OpenAI API integration for recipe generation
- Recipe categories and filters
- Shopping list generation
- Nutritional information
- Cooking timer
- Social sharing

### Improve AI
- Use OpenAI GPT API for custom recipe generation
- Implement image recognition for ingredient detection
- Add dietary preferences filtering (vegetarian, vegan, etc.)
- Consider recipe difficulty levels

## 📝 Sample Data

The database includes 10 sample recipes:
- Spaghetti Carbonara
- Chicken Stir Fry
- Margherita Pizza
- Caesar Salad
- Scrambled Eggs
- Tomato Soup
- Grilled Cheese Sandwich
- Vegetable Curry
- Pancakes
- Greek Salad

## 🔐 Security Notes

⚠️ **Important for Production:**
- Change `SECRET_KEY` in `app.py`
- Use environment variables for sensitive data
- Enable HTTPS
- Implement rate limiting
- Add CSRF protection
- Use stronger password requirements

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

## 🤝 Contributing

Feel free to fork this project and add your own features!

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as a learning project for web development and AI integration.

---

Happy Cooking! 🍽️