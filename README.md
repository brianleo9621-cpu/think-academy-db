# Think Academy — SAT Response Database

Automates the extraction of student SAT responses from a CSV file into a normalized MySQL database. Saves ~3 hours of manual data entry per week.

## Project Structure
```
think-academy-db/
├── schema.sql        # Database table definitions
├── seed.py           # Loads CSV data into MySQL
├── .gitignore        # Keeps credentials and data private
├── .env              # Your local credentials (not on GitHub)
└── README.md         # You are here
```

## Prerequisites

- Python 3.x
- MySQL Community Server

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/brianleo9621-cpu/think-academy-db.git
cd think-academy-db
```

**2. Install MySQL**

Download MySQL Community Server from dev.mysql.com/downloads/mysql/

**3. Create the database**
```bash
mysql -u root -p
CREATE DATABASE think_academy;
EXIT;
```

**4. Create your .env file**

Create a file called `.env` in the project folder:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=think_academy
```
Note: you can name the database anything, just make sure DB_NAME matches.

**5. Create the tables**

Open schema.sql in VS Code and click Run on active connection in SQLTools.

**6. Install Python dependencies**
```bash
pip install mysql-connector-python python-dotenv
```

## Usage

**1. Add your CSV file**

Place your CSV in the project folder named `sat_responses.csv` with these columns:
```
name, email, age, score, submitted_at
```

**2. Run the script**
```bash
python seed.py
```

**3. Check the output**
```
Done! Inserted 100 responses.
Connection closed.
```

## Adding New Data

To add more responses later, just drop in a new CSV and run seed.py again. Existing students won't be duplicated — only new responses get added.

## Database Schema

**students**
| Column | Type | Description |
|---|---|---|
| student_id | INT | Auto generated primary key |
| name | VARCHAR | Student full name |
| email | VARCHAR | Unique student email |
| age | INT | Student age |

**sat_responses**
| Column | Type | Description |
|---|---|---|
| response_id | INT | Auto generated primary key |
| student_id | INT | Links to students table |
| score | INT | SAT score |
| submitted_at | DATETIME | Submission timestamp |