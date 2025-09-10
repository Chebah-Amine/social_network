# Social Network – CS50 Web Project 4

A social media web application built as part of **CS50 Web Programming with Python and JavaScript**.
The app allows users to register, log in, create posts, like/unlike posts, follow/unfollow users, and browse posts by people they follow.

This project demonstrates key concepts of **Django**, **frontend/backend integration**, and **full-stack web development**.

---

## 📽️ Project Demo

Watch the demo video on YouTube:
👉 [Project Video Walkthrough](https://youtu.be/qmUAHNA1-38)

---

## ⚙️ Features

* User authentication (register, login, logout)
* Create, edit, and paginate posts
* Like/unlike posts with dynamic updates
* Follow/unfollow other users
* Dedicated pages for:

  * All posts
  * Posts by a specific user (profile)
  * Posts from followed users
* Responsive UI with Django templates

---

## 🛠️ Tech Stack

* **Backend**: Django (Python)
* **Frontend**: HTML, CSS, JavaScript (vanilla, with Django templates)
* **Database**: SQLite (development)
* **Containerization**: Docker + Docker Compose
* **Testing**: Pytest + pytest-django + Coverage
* **CI/CD**: GitHub Actions + SonarCloud

---

## 🧪 Tests

Unit and integration tests are written using **pytest**.

Main coverage:

* Authentication (login, register, logout)
* Creating and validating posts
* Following/unfollowing users
* Profile and following feeds
* Likes/unlikes
* Edge cases (unauthorized actions, invalid form input, etc.)

Run tests locally and generate the coverage inside Docker:

```bash
make test
```

---

## 🔄 Continuous Integration

The project uses **GitHub Actions** with:

* Linting and formatting checks
* Automated tests with `pytest`
* Coverage report uploaded to **SonarCloud** for code quality analysis

---

## 🐳 Docker Setup

The application is fully containerized with **Docker Compose**.

### Build and run:

```bash
make start
```

---

## 📂 Project Structure

```
app/
|── .github/workflows/ # CI pipelines
│── network/         # Core app (models, views, forms, urls)
│── project4/        # Django project settings
│── tests/           # Unit and integration tests
docker/              # Docker configuration
requirements/        # Python dependencies
```

---

## 🚀 Future Improvements

* Add notifications for likes and follows
* Enhance frontend with React
* Deploy on a production server with HTTPS (Heroku / Render / Fly.io)
