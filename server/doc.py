from flask_apispec import FlaskApiSpec
from server import app

docs = FlaskApiSpec(app)

docs.register(notes)

app.add_url_rule('/notes', view_func=StoreResource.as_view('Store'))
docs.register(StoreResource)