
from flask import jsonify
from app.jobs.model import Job
from app.config.connect import db

def get_jobs():
    try:
        jobs = Job.query.all()
        response = [job.to_dict() for job in jobs]
        return response
    except Exception as e:
        db.session.rollback() 
        return jsonify({f"error": "{e}"})
def get_job_by_id(job_id):
    try:
        response = Job.query.get(job_id)
        if response:
            return response.to_dict()
        else:
            return jsonify({"error": "Job not found", "status": 404})
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": f"Failed to retrieve job\n{e}", "status": 500})
          
def add_JOB(arg):
    try:
        query = Job(arg['title'],arg['company'],arg['location'], arg['salary'],arg['url'],arg['created_at'])
        db.session.add(query)
        db.session.commit() 
        
        return jsonify({"message": "Job added successfully", "status": 200})
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": f"Failed to add job\n{e}", "status": 500})
def get_del_job_by_id(job_id):
    try:
        response = Job.query.get(job_id)
        if response:
            db.session.delete(response)
            db.session.commit() 
            return jsonify({"message": "Job deleted successfully", "status": 200})
        else:
            return jsonify({"error": "Job not found", "status": 404})
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": f"Failed to delete job\n{e}", "status": 500})

def update_job_id(id, arg):
    try:
        job = Job.query.get(id)
        if job:
            job.title = arg['title']
            job.url = arg['url']
            db.session.commit()
            return jsonify({"message": "Job updated successfully", "status": 200})

        return jsonify({"error": "Job not found","status": 404})

    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": f"Failed to update job: {str(e)}", "status": 500})
    
def filter_title(query):
    print("query",query)
    try:
        jobs = Job.query.filter(Job.title.ilike(f"%{query}%")).all()
        # if jobs:
        return [job.to_dict() for job in jobs if job is not None]
        # else:
        #     return jobs
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": f"Failed to filter jobs by title: {e}", "status": 500})

def add_multiple_jobs(jobs_list):

    try:
        # Create Job objects from the list of dictionaries
        job_objects = [
            Job(
                job['title'],
                job['company'],
                job['location'],
                job['salary'],
                job['url'],
                job['created_at']
            )
            for job in jobs_list
        ]
        
        # Bulk insert all job objects
        db.session.bulk_save_objects(job_objects)
        db.session.commit()
        
        return jsonify({"message": "Jobs added successfully", "status": 200})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add jobs: {str(e)}", "status": 500})
