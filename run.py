from dotenv import load_dotenv
# load .env settings
load_dotenv()

from MR_Blog import create_app

app = create_app()

if __name__ == '__main__':
	app.run(debug=app.config.get('DEBUG'))
else:
	raise ImportError('this file cannot be imported: ', __name__)