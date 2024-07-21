from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
load_dotenv()
# PostgreSQL connection

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"Database URL: {DATABASE_URL}")
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    print("Successfully connected to the database")
except psycopg2.Error as e:
    print(f"Unable to connect to the database: {e}")

@app.route('/jobs', methods=['GET'])
def get_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of jobs per page
    offset = (page - 1) * per_page

    cur.execute("SELECT title, company_name, location, date, url, description FROM job_postings LIMIT %s OFFSET %s",
                (per_page, offset))
    jobs = cur.fetchall()
    jobs_list = []
    for job in jobs:
        job_dict = {
            "title": job[0] if len(job) > 0 else None,
            "company_name": job[1] if len(job) > 1 else None,
            "location": job[2] if len(job) > 2 else None,
            "date": job[3] if len(job) > 3 else None,
            "url": job[4] if len(job) > 4 else None,
            "description": job[5] if len(job) > 5 else None
        }
        jobs_list.append(job_dict)

    # Get total count of jobs
    cur.execute("SELECT COUNT(*) FROM job_postings")
    total_jobs = cur.fetchone()[0]

    return jsonify({
        "jobs": jobs_list,
        "total": total_jobs,
        "page": page,
        "per_page": per_page
    })

@app.route('/events', methods=['GET'])
def get_events():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of events per page
    offset = (page - 1) * per_page

    cur.execute("SELECT name, date, location, url, img_url FROM events LIMIT %s OFFSET %s",
                (per_page, offset))
    events = cur.fetchall()
    events_list = []
    for event in events:
        events_list.append({
            "name": event[0],
            "date": event[1],
            "location": event[2],
            "url": event[3],
            "img_url": event[4]
        })

    # Get total count of events
    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]

    return jsonify({
        "events": events_list,
        "total": total_events,
        "page": page,
        "per_page": per_page
    })

if __name__ == '__main__':
    app.run(debug=True)