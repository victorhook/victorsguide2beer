# Local configs
APP = app/app
TOOLS = tools
PORT = 8080

# Remote configs
REMOTE_IP = 142.93.164.184
REMOTE_USER = git
VIRTUAL_ENV = env
REMOTE_PROJECT_DIR = /home/git/web/victorsguide2beer

SUDO_PASS=`cat server_sudo_pass`

run:
	. ${VIRTUAL_ENV}/bin/activate; \
	FLASK_APP=${APP} FLASK_ENV=development flask run --host 0.0.0.0 --port ${PORT}; \

sync:
	@echo "Syncing remote database"
	rsync -a ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_PROJECT_DIR}/app/db.json app/db.json
	@echo "Syncing remote beer images"
	rsync -a ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_PROJECT_DIR}/app/static/beers app/static

new:
	. ${VIRTUAL_ENV}/bin/activate python; ${TOOLS}/new_post.py

deploy:
	@echo "SSH:ing to remote..."; \
	ssh ${REMOTE_USER}@${REMOTE_IP} "cd ${REMOTE_PROJECT_DIR} && git fetch && git reset --hard origin/master && . env/bin/activate && python3 tools/create_events.py && echo $(SUDO_PASS) | sudo -S systemctl restart apache2"

install:
	python -m venv env; \
	. env/bin/activate; \
	pip install -r requirements.txt
# flask jinja-markdown Flask-HTTPAuth

