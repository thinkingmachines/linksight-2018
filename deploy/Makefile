.PHONY: deploy secrets instance setup-instances

SECRETS_DIR = secrets/$(ENV)
SECRETS = $(wildcard $(SECRETS_DIR)/cleartext/*)
ENCRYPTED = $(patsubst $(SECRETS_DIR)/cleartext/%, $(SECRETS_DIR)/%.enc, $(SECRETS))

deploy: secrets cloudbuild.yml
	gcloud builds --project linksight-208514 \
		submit \
		--config cloudbuild.yml \
		--substitutions=TAG_NAME=$(ENV),_HOST=$(HOST) \
		..

secrets: $(ENCRYPTED)

$(SECRETS_DIR)/%.enc: $(SECRETS_DIR)/cleartext/%
	gcloud kms --project linksight-208514 \
		encrypt \
		--plaintext-file=$< \
		--ciphertext-file=$@ \
		--location=global \
		--keyring=linksight \
		--key=linksight

instance:
	terraform plan -out main.tfplan
	terraform apply main.tfplan

setup-instances:
	ansible-playbook -i hosts.yml playbook.yml
