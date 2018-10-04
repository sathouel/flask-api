# from flask import jsonify, request
#
# from api import app, db
# from api.models import User
#
# from api.errors import bad_request
#
#
# @app.route('/')
# def index():
#     return 'Hello World!', 200
#
#
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json() or {}
#     if len(data.keys()) == 0:
#         return bad_request('no data provided')
#     if User.query.filter_by(username=data['username']).first():
#         return bad_request('please use a different username')
#     if User.query.filter_by(email=data['email']).first():
#         return bad_request('please use a different email')
#     user = User()
#     user.from_dict(data, new_user=True)
#     db.session.add(user)
#     db.session.commit()
#     response = jsonify(user.to_dict())
#     response.status_code = 201
#     return response
