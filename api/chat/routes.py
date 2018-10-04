from api.chat import bp
from api.auth import token_auth


@bp.route('/')
@token_auth.login_required
def get_chat():
    return 'Your are within the chat!', 200