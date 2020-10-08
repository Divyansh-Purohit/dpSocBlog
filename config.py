import os
basedir = os.path.abspath(os.path.dirname(__file__))
#os.environ["FLASKY_ADMIN"] = "Divyansh Purohit" set in flask shell


class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'SecretKey'
	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
	MAIL_PORT = os.environ.get('MAIL_PORT', '587')
	#MAIL_USE_SSL = True
	#MAIL_USE_TLS = False
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX')
	FLASKY_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = False
	SQLALCHEMY_RECORD_QUERIES = True 	#records the time taken by each query in a request
	FLASKY_SLOW_DB_QUERY_TIME = 0.5 #in seconds
	FLASKY_POSTS_PER_PAGE = 20
	FLASKY_FOLLOWERS_PER_PAGE = 50
	FLASKY_COMMENTS_PER_PAGE = 30

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.db')
		
class TestingConfig(Config):
	Testing = True
	SQLALCHEMY_DATA_BASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///test.db'
	WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
	SQLALCHEMY_DATA_BASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-prod.db')
		
	SQLALCHEMY_RECORD_QUERIES = TrueFLASKY_SLOW_DB_QUERY_TIME = 0.5

	@classmethod
	def init_app(cls, app):
		Config.init_app(app)
		#email errors to the administrators
		import logging
		from logging.handlers import SMTPHandler
		credential = None
		secure = None
		if getattr(cls, 'MAIL_USERNAME', None) is not None:
			credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
			if getattr(cls, 'MAIL_USE_TLS', None):
				secure()
				mail_handler = SMTPHnadler(
					mailhost = (cls.MAIL_SERVER, cls.MAIL_PORT),
					fromaddr = cls.FLASKY_MAIL_SENDER,
					toaddr = [cls.FLASKY_ADMIN],
					subject = cls.FLASKY_MAIL_SUBJECT_PREFIX + 'Application Error',
					credentials = credentials,
					secure = secure)
				mail_handler.setLevel(logging.ERROR)
				app.logger.addHandler(mail_handler)
config = {
	'development': DevelopmentConfig,
	'testing':TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}

from flask_mail import Mail, Message

mail = None

def configure_mail(app):
    # EMAIL SETTINGS
    global mail
    app.config.update(
        MAIL_SERVER = os.environ.get('MAIL_SERVER'),
        MAIL_PORT = 465,
        MAIL_USE_SSL = True,
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
        DEFAULT_MAIL_SENDER = 'dp2012div@gmail.com',
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'SecretKey',
    )
    mail=Mail(app)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
