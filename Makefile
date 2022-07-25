APP = app/main
PORT = 8080
REMOTE = 142.93.164.184
REMOTE_USER = git
VIRTUAL_ENV = env
PROJECT_DIR = /home/git/web/victorsguide2beer

run:
	. ${VIRTUAL_ENV}/bin/activate; \
	FLASK_APP=${APP} FLASK_ENV=development flask run --host 0.0.0.0 --port ${PORT}; \

deploy:
#git commit
	@echo "SSH:ing to remote..."
	ssh ${REMOTE_USER}@${REMOTE} "cd ${PROJECT_DIR} && git reset --hard origin/master"


# Install
# pip install flask jinja-markdown