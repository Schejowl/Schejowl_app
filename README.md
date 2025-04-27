# Schejowl 🕓

Schejowl is a web application that helps groups easily find the best meeting times based on user preferences.
It's a smarter, modern clone of When2Meet.


## Features
- Choose availability with preference scores (0.2, 0.4, 0.6, 0.8, 1).
- Backend optimization to find the most preferred times.
- Easy and clean frontend UI.
- Built with **Django** + **React**.


## Team Members:
**Angel Koh** - Optimization problem subteam, worked on converting and finalizing the complete optimization model 

**Kyle Zhang** - Website UI subteam, created a new website on the local host server for efficiency and worked on implementing a new optimization model into website 

**Nick Lin** - Website UI subteam, worked on website UI 

**Nursultan Asilbekov** - Optimization problem subteam, worked on converting and finalizing complete optimization model, came up with Schejowl name, created the website 

**Varshini Loganathan** - Team Lead/Website UI subteam, led/scheduled meetings, converted Schej website UI into our website, built out showcase presentation 


## Latex Documentation of Optimization Model: 
https://www.overleaf.com/read/qtkndmstgmdt#c639e0


## How to Run Locally

### Backend (Django)

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
2. Navigate to the backend folder:
   ```bash
   cd backend
3. Make migrations and execute a migration
   ```bash
   python manage.py makemigrations
   pytthon manage.py migrate
4. Run the Django server
   ```bash
   python manage.py runserver

### Frontend (React)

1. Navigate to the frontend folder
   ```bash
   cd frontend 

2. Install React dependencies
   ```bash
   npm install
4. Start the React app
   ```bash
   npm start
The website will start at **http://localhost:3000/**.


