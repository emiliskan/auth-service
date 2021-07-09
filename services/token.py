from typing import Optional

from config.extentions import db, jwt, redis
from models import Token, User
from services.utils import generate_tokens, identify_user


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = redis.get(jti)
    return token_in_redis is not None


def update_refresh_token() -> Optional[dict]:
    user_id, token_id, _ = identify_user()
    old_token = Token.query.get(token_id)

    if not old_token:
        return

    user = db.session.query(User).join(User.token).filter_by(id=old_token.id).first()
    token_pair, token_instance = generate_tokens(user_id)
    user.token = [token_instance]
    db.session.add(user)
    db.session.delete(old_token)
    db.session.commit()
    return token_pair
