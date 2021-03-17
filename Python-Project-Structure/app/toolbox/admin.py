from flask_admin.contrib.sqla import ModelView


class AdminView(ModelView):

    def is_accessible(self):
        return True
