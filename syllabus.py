from flask import Flask, render_template, redirect, url_for, Blueprint, request, session, flash,jsonify
import db_access,json

syllabus_bp = Blueprint('syllabus',__name__)

@syllabus_bp.route('/syllabus_detail',methods=['GET'])
def syllabus_detail():
    
    id = request.args.get('id')
    if not id:
        id = session.get('subject_id')
    detail_data = db_access.syllabus_detail(id)

    session['subject_id'] = detail_data[0]
    prev_data = db_access.previous_data(id)
    review_list = db_access.review_list(id)

    keys = ["difficulty", "assignment", "interest", "speed", "understanding"]

    sums = [0] * 5
    count = len(review_list)
    
    for row in review_list:
        for i in range(5):
            sums[i] += row[i+1]
            
    ave = {
    key: round(sums[i] / count, 1) if count != 0 else 0.0
    for i, key in enumerate(keys)
    }
    

    
    
    return render_template('sllabusconfirm.html',detail_data=detail_data,prev_data=prev_data,review_list=review_list,ave=ave)
