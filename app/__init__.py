from flask import Flask, request
from app.api import hello


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.register_blueprint(hello.blueprint)

    @app.after_request
    def log_response(response):
        app.logger.info('{method} {url}\n{response}'.format(
            method=request.method,
            url=request.url,
            response=response
        ))
        return response

    return app
