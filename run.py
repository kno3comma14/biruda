from flask_script import Manager

from api import create_app

app = create_app('development')

manager = Manager(app)

@manager.command
def migrate():
    pass

if __name__ == '__main__':
    manager.run()
