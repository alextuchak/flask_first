import models
import app
from flask_migrate import Migrate

applications = app.app
migrate = Migrate(applications, app.db)