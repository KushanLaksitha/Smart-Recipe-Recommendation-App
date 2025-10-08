-- Create Database
CREATE DATABASE IF NOT EXISTS recipe_db;
USE recipe_db;

-- Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recipes Table
CREATE TABLE recipes (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    image_url VARCHAR(255),
    prep_time INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Favorites Table
CREATE TABLE favorites (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, recipe_id)
);

-- Ratings Table
CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    UNIQUE KEY unique_rating (user_id, recipe_id)
);

-- Insert Sample Recipes
INSERT INTO recipes (name, ingredients, instructions, image_url, prep_time) VALUES
('Spaghetti Carbonara', 'spaghetti, eggs, bacon, parmesan cheese, black pepper, salt', 
'1. Cook spaghetti according to package directions. 2. Fry bacon until crispy. 3. Mix eggs and cheese. 4. Combine hot pasta with bacon and egg mixture. 5. Season with pepper and salt.',
'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400', 20),

('Chicken Stir Fry', 'chicken breast, soy sauce, vegetables, garlic, ginger, oil, rice',
'1. Cut chicken into strips. 2. Heat oil in wok. 3. Cook chicken until golden. 4. Add vegetables and stir fry. 5. Season with soy sauce, garlic, and ginger. 6. Serve with rice.',
'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400', 25),

('Margherita Pizza', 'pizza dough, tomato sauce, mozzarella cheese, fresh basil, olive oil',
'1. Roll out pizza dough. 2. Spread tomato sauce evenly. 3. Add mozzarella cheese. 4. Bake at 450°F for 12-15 minutes. 5. Top with fresh basil and drizzle olive oil.',
'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400', 30),

('Caesar Salad', 'romaine lettuce, caesar dressing, croutons, parmesan cheese, lemon',
'1. Wash and chop romaine lettuce. 2. Toss with caesar dressing. 3. Add croutons and parmesan. 4. Squeeze fresh lemon juice. 5. Serve immediately.',
'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400', 10),

('Scrambled Eggs', 'eggs, butter, milk, salt, pepper',
'1. Beat eggs with milk, salt, and pepper. 2. Melt butter in pan. 3. Pour egg mixture. 4. Stir gently until cooked. 5. Serve hot.',
'https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400', 5),

('Tomato Soup', 'tomatoes, onion, garlic, vegetable broth, cream, basil, salt, pepper',
'1. Sauté onion and garlic. 2. Add chopped tomatoes and broth. 3. Simmer for 20 minutes. 4. Blend until smooth. 5. Stir in cream and basil. 6. Season to taste.',
'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400', 30),

('Grilled Cheese Sandwich', 'bread, cheese, butter',
'1. Butter one side of each bread slice. 2. Place cheese between bread slices, butter side out. 3. Grill on medium heat until golden. 4. Flip and cook other side. 5. Serve hot.',
'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400', 10),

('Vegetable Curry', 'mixed vegetables, curry powder, coconut milk, onion, garlic, ginger, rice',
'1. Sauté onion, garlic, and ginger. 2. Add curry powder and cook 1 minute. 3. Add vegetables and coconut milk. 4. Simmer until vegetables are tender. 5. Serve with rice.',
'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400', 35),

('Pancakes', 'flour, eggs, milk, sugar, baking powder, butter, maple syrup',
'1. Mix dry ingredients. 2. Add eggs and milk, whisk until smooth. 3. Heat butter in pan. 4. Pour batter and cook until bubbles form. 5. Flip and cook other side. 6. Serve with maple syrup.',
'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400', 15),

('Greek Salad', 'cucumber, tomato, red onion, olives, feta cheese, olive oil, lemon juice, oregano',
'1. Chop vegetables into chunks. 2. Combine in bowl. 3. Add olives and feta. 4. Drizzle with olive oil and lemon juice. 5. Sprinkle oregano. 6. Toss gently.',
'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400', 15);


ALTER TABLE recipes 
ADD COLUMN uploaded_by INT DEFAULT NULL AFTER prep_time,
ADD FOREIGN KEY (uploaded_by) REFERENCES users(user_id) ON DELETE SET NULL;

-- Add indexes for better performance
CREATE INDEX idx_uploaded_by ON recipes(uploaded_by);
CREATE INDEX idx_recipe_name ON recipes(name);
CREATE INDEX idx_prep_time ON recipes(prep_time);

SELECT 'Database upgrade completed!' as Status;
exit;