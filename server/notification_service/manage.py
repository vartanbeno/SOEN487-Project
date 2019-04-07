import main
import models


@main.app.shell_context_processor
def make_shell_context():
    return dict(app=main.app, db=models.db, Person=models.Person, Admin=models.Admin, NotificationType = models.NotificationType)
