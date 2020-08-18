from blueprints import app
import config


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host="0.0.0.0", port=app.config['APP_PORT'])
    