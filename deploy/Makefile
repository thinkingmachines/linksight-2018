.PHONY: secrets deploy-staging

deploy-staging: cloudbuild-staging.yml
	gcloud builds submit --config cloudbuild-staging.yml ..

secrets: cert.pem.enc ca.pem.enc key.pem.enc staging.env.enc

%.enc: secrets/%
	gcloud kms --project linksight-208514 \
		encrypt \
		--plaintext-file=$< \
		--ciphertext-file=$@ \
		--location=global \
		--keyring=linksight \
		--key=linksight
