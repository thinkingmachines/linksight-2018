.PHONY: install ssh encrypt-env
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
encrypt-env:
	gcloud kms --project linksight-208514 \
		encrypt \
		--plaintext-file=prod.env \
		--ciphertext-file=prod.env.enc \
		--location=global \
		--keyring=linksight \
		--key=linksight
