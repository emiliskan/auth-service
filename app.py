from redis import Redis
from flask import Flask

import role
import user

from config import Config
from db import init_db
from ma import init_ma

config = Config()

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

init_db(app)
init_ma(app)

redis = Redis(host=config.redis_host, port=config.redis_port)

# Routes
app.register_blueprint(role.role_views.blueprint, url_prefix='/roles')
app.register_blueprint(role.permission_views.blueprint)
app.register_blueprint(role.user_role_views.blueprint, url_prefix='/user_roles')


@app.route('/redis-info')
def redis_info():
    return redis.info()


def start_app():
    app.run(host=config.flask_host, port=config.flask_port, debug=config.debug)


if __name__ == '__main__':
    start_app()