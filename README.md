# CS50's Web Project 2 - Commerce (Under Development)

- [CS50's Web Project 2 - Commerce (Under Development)](#cs50s-web-project-2---commerce-under-development)
  - [Overview](#overview)
  - [Demo](#demo)
  - [Features](#features)
    - [Create Listing](#create-listing)
    - [Active Listings Page](#active-listings-page)
    - [Listing Page](#listing-page)
    - [Watchlist](#watchlist)
    - [Categories](#categories)
    - [Django Admin Interface](#django-admin-interface)
  - [Technologies](#technologies)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Project Structure](#project-structure)

## Overview
This is the **Commerce** project, developed as part of CS50's Web Programming with Python and JavaScript. It's an auction-based e-commerce platform where users can create, browse, bid on listings, and add items to their watchlist. Additionally, users can post comments on listings, while the auction creator can close the auction at any time.

## Demo
(Insert link to demo video or screenshots)

## Features

### Create Listing
Users can create a new auction by providing a title, description, starting bid, and optionally, an image URL and category.

### Active Listings Page
Displays all active auction listings, showing title, description, current price, and an optional photo. Users can click on a listing to view its details.

### Listing Page
Each listing displays detailed information including the current price and the seller's information. Logged-in users can:
- Add/remove the listing from their Watchlist.
- Place bids on the item (must be higher than the starting/current bid).
- Close the auction (if they are the listing creator).
- Post comments and see all comments related to the listing.
- See if they won the auction when closed.

### Watchlist
Signed-in users can add items to a personal watchlist and view them on a dedicated page.

### Categories
Displays all available categories. Clicking on a category shows all active listings under that category.

### Django Admin Interface
Admins can manage all aspects of the auction site (listings, bids, and comments) via the Django Admin panel.

## Technologies
- **Front-end:**
  - HTML 
  - CSS 
  - Bootstrap 
  - JavaScript

<div style="display:flex; align-items:center; gap:12px;"> 
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS">
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
</div>

<br>

- **Back-end:**
  - Python 
  - Django
  - SQLite

<div style="display:flex; align-items:center; gap:12px;"> 
  <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
</div>

## Requirements
- Python 3.12.5
- pip 24.2
- Django 5.1    
## Installation
1. Clone the repository to your local environment:
   ```bash
   git clone <repository-URL>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # For Unix or MacOS systems
   .\.venv\Scripts\activate  # For Windows PowerShell
   ```

3. Install the required dependencies with the command:
   ```bash
   pip install <dependency-name> or pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations auctions
   python manage.py migrate
   ```

5. Start the Django development server:
   ```bash
   python manage.py runserver 
   ```

6. Access the application in your browser at  `http://127.0.0.1:8000/`.


## Project Structure
- `auctions/` - Main Django application containing all the auctions functionalities.
- `static/` - Directory for static files such as CSS, JavaScript, and images.
- `templates/` - Contains the HTML templates used to render the auctions pages.
- `apps.py` - Django application configuration.
- `urls.py` - Defines the application's routes and maps URLs to corresponding views.
- `util.py` - Utility file with helper functions.
- `views.py` - Contains the views responsible for processing requests and rendering the appropriate pages.
