APP = app/main
PORT = 8080

run:
	FLASK_APP=${APP} FLASK_ENV=development flask run --host 0.0.0.0 --port ${PORT}