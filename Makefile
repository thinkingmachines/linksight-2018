.PHONY: install ssh build-staging
install: venv requirements.txt
	venv/bin/pip-sync
venv:
	python3 -m venv venv
	venv/bin/pip install pip-tools
requirements.txt: requirements.in
	venv/bin/pip-compile requirements.in > requirements.txt
ssh:
	gcloud compute --project linksight-208514 \
		ssh \
		--zone asia-southeast1-b \
		linksight
prod.env.enc: prod.env
	gcloud kms --project linksight-208514 \
		encrypt \
		--plaintext-file=prod.env \
		--ciphertext-file=prod.env.enc \
		--location=global \
		--keyring=linksight \
		--key=linksight
staging.env.enc: staging.env
	gcloud kms --project linksight-208514 \
		encrypt \
		--plaintext-file=staging.env \
		--ciphertext-file=staging.env.enc \
		--location=global \
		--keyring=linksight \
		--key=linksight
build-staging: deploy/cloudbuild-staging.yaml
	gcloud builds submit --config deploy/cloudbuild-staging.yaml .
