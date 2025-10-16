# 🎮 GameScope

**Date:** October 15, 2025, 01:57 PM +03  
**Author:** [Omar shilbaya]  

---

## 📝 Description

GameScope is a web-based platform designed to let users explore detailed game information, create and manage reviews, add comments, and interact with a community-driven review system. Built with a focus on a responsive, dark-themed interface, this app includes a search functionality to quickly find games, making it easy for users to discover and contribute to game content. The project was inspired by the need for a centralized hub to share and discuss game experiences, leveraging Django for robust backend support and custom CSS for a cohesive design.

---

## ⚙️ Technologies Used
- **Django**: For backend development and template rendering  
- **HTML**: For structuring web pages  
- **CSS**: Custom styling with variables for a consistent theme  
- **Git**: For version control  

---

## 📸 Screenshots/Logo

### 🖥️ Home Page  
![Home Page Screenshot](./gamescope_app/static/images/home1.png)


### ✍️ Game Details Page  
![Game Details Screenshot](./gamescope_app/static/images/game_details.png)


### 🔍 Search in Action  
![Search Screenshot](./gamescope_app/static/images/search.png)




---

## 💡 Features
- Detailed game information display (genre, platform, rating, etc.)  
- User authentication for review and comment creation  
- Responsive form pages for adding and editing reviews/comments  
- Message system for success/error feedback  
- Comment threading with nested replies  
- Integrated search functionality to find games quickly  

---

## 🗂️ Database Design
Below is the ERD showing the relationships between models in GameScope.

![ERD Diagram](./gamescope_app/static/images/ERD.png)

---

## ⚙️ Installation
1. Clone the repository
2. Install dependencies
3. Run migrations
4. Start the development server

---

## 📝 User Stories
- **View games:** As a user, I want to view a list of available games so that I can choose which game to explore or review.  
- **Search games:** As a user, I want to search for a specific game by name or genre so that I can quickly find the game I’m interested in.  
- **Game details:** As a user, I want to view detailed information about a game so that I can learn more about its features and release details.  
- **Write reviews:** As a user, I want to write a review for a game so that I can share my personal opinion and experience with others.  
- **Read reviews:** As a user, I want to read reviews written by other users so that I can see different perspectives about the game.  
- **Comment on reviews:** As a user, I want to comment on other users’ reviews so that I can discuss and exchange opinions about the games.

---

## 🚀 Getting Started
- **Deployed App**: [Visit GameScope Live](https://gamescope-mbhm.onrender.com) *(Replace with your deployed URL)*  

---
## 🧠 Summary of Challenges Encountered and Solutions Applied

### 1. Pagination of Game Listings
**Challenge:**  
When displaying a large number of games, loading them all at once made the page slow and cluttered. Implementing pagination was necessary to improve performance and user experience.  

**Solution:**  
Used Django’s built-in `Paginator` class to split the game list into pages. Adjusted the template logic to handle page navigation smoothly and styled the pagination controls for a clean, user-friendly layout.  

---

### 2. Database Reset After Deployment
**Challenge:**  
After deploying to Render, all data disappeared because Render’s free PostgreSQL instance resets data on rebuilds or restarts. This caused the loss of the admin user and game entries.  

**Solution:**  
Implemented automatic data seeding in the app’s `apps.py` file to recreate the superuser and repopulate the database with default game data whenever the application is deployed.  

---

### 3. Dynamic Superuser and Game Data Creation
**Challenge:**  
Render’s free plan doesn’t allow shell access, preventing the creation of a superuser or running management commands after deployment.  

**Solution:**  
Moved the logic to automatically create a superuser and populate game data into the `ready()` method of `apps.py`, ensuring these are created programmatically on app startup without requiring shell commands.  

---

## 🙌 Attributions
- Django documentation – framework and class-based views reference  
- MDN Web Docs – CSS and HTML best practices  
- CSS-Tricks – for responsive design guidance  


---


## 🔮 Next Steps
- Add user profile pages to track review history  
- Implement a star-based rating system  
- Enhance mobile responsiveness with touch-friendly controls  
- Enhance the style of the comments and reviews sections 

---

## 🧑‍💻 Author
**Name:** [omar shilbaya]  
**GitHub:** [OmarSalah885](https://github.com/OmarSalah885)

---
