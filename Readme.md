# Movie Management System 🎬

A professional Desktop Application built with **Python** and **Tkinter** to manage a personal movie collection. This application follows a modular design, separating the User Interface from the Database logic, and uses **SQLite** for persistent storage.

## Features
- **Add Movies:** Save details like Title, Director, Year, and Rating.
- **View Collection:** Display all movies in a clean, scrollable list format.
- **Update Details:** Edit existing movie information easily.
- **Delete:** Remove movies from the database.
- **Persistent Storage:** Data is automatically saved in a local `movies.db` file.
- **Input Validation:** Prevents crashes by validating that Year and Rating are numbers.

## System Architecture

The project is structured into two main components:
1. **Database (`db.py`):** Handles all SQL operations (backend).
2. **MovieApp (`main.py`):** Handles the Graphical User Interface (frontend).

```mermaid
classDiagram
    class Database {
        +conn : sqlite3.Connection
        +cur : sqlite3.Cursor
        +add_movie(title, director, year, rating)
        +fetch_all() : list
        +remove_movie(id)
        +update_movie(id, title, director, year, rating)
    }

    class MovieApp {
        +root : Tk
        +db : Database
        +tree : Treeview
        +setup_ui()
        +add_movie()
        +update_movie()
        +delete_movie()
        +populate_list()
    }

    MovieApp --> Database : Instantiates & Uses
