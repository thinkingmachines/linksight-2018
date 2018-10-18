.PHONY: secrets deploy-staging

deploy-staging: cloudbuild.yml secrets
	gcloud builds --project linksight-208514 \
		submit \
		--config cloudbuild.yml \
		--substitutions=TAG_NAME=staging,_HOST=linksight-stg.thinkingmachin.es \
		..

secrets: cert.pem.enc ca.pem.enc key.pem.enc staging.env.enc

%.enc: secrets/%
	gcloud kms --project linksight-208514 \
		encrypt \
		--plaintext-file=$< \
		--ciphertext-file=$@ \
		--location=global \
		--keyring=linksight \
		--key=linksight
