.PHONY: install ssh dev worker flower
all: venv requirements.txt app/node_modules
	venv/bin/pip-sync
venv:
	python3 -m venv venv
	venv/bin/pip install pip-tools
requirements.txt: requirements.in
	venv/bin/pip-compile requirements.in > requirements.txt
app/node_modules: app/package.json
	cd app && npm install
ssh:
	gcloud compute --project linksight-208514 \
		ssh \
		--zone asia-southeast1-b \
		linksight
dev:
	pm2 start
