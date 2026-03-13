# Think Academy — SAT Response Database

Automates the extraction of student SAT responses from a CSV file into a normalized MySQL database. Saves ~3 hours of manual data entry per week.

## Project Structure
```
think-academy-db/
├── Dockerfile            # Python container setup
├── docker-compose.yml    # Runs Python app and MySQL together
├── schema.sql            # Database table definitions
├── seed.py               # Loads CSV data into MySQL
├── .gitignore            # Keeps credentials and data private
├── .env                  # Your local credentials (not on GitHub)
└── README.md             # You are here
```

## Prerequisites

- Docker Desktop — download from docker.com/products/docker-desktop

That's it — no Python or MySQL install needed.

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/brianleo9621-cpu/think-academy-db.git
cd think-academy-db
```

**2. Create your .env file**

Create a file called `.env` in the project folder:
```
DB_HOST=db
DB_USER=root
DB_PASSWORD=password
DB_NAME=think_academy
```
Note: `DB_HOST` must be `db` — this is the MySQL service name inside Docker.
Note: You can name the database anything, just make sure `DB_NAME` matches `MYSQL_DATABASE` in docker-compose.yml.

**3. Add your CSV file**

Place your CSV in the project folder named `sat_responses.csv` with these columns:
```
name, email, age, score, submitted_at
```

## Usage

**Run the application:**
```bash
docker-compose up
```
Docker will automatically:
- Start a MySQL 8 database
- Create the `think_academy` database
- Run schema.sql to create the tables
- Run seed.py to load your CSV data

**Stop the application:**
```bash
docker-compose down
```

**After making code changes, rebuild:**
```bash
docker-compose up --build
```

## Adding New Data

To load new responses, drop in a new `sat_responses.csv` and run:
```bash
docker-compose up
```
Existing students won't be duplicated — only new responses get added.

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

## How It Works

1. Docker starts MySQL and runs schema.sql automatically
2. seed.py connects to MySQL using credentials from .env
3. CSV is read row by row and validated
4. Each student is inserted into the students table
5. Their score is inserted into sat_responses linked by student_id
6. Duplicate students are detected by email and skipped

## Tech Stack

- Python 3.11
- MySQL 8
- Docker
- Libraries: mysql-connector-python, python-dotenv