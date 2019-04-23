from main import app
from ImgManager.models import db, Client, Album, Image


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Person=Client, Album=Album, Picture=Image)
