from flask import jsonify, request, g

from api import db
from api.models import User
from api.errors import bad_request
from api.auth import bp
from api.auth import basic_auth
from api.auth import token_auth


@bp.route('/tst')
def index():
    return 'Hello!', 200


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if len(data.keys()) == 0:
        return bad_request('no data provided')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    return response

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204