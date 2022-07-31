# Scraper
## Requirements
- Docker
- AWS SNS topic (to receive product price data)
- AWS access creds to publish to this sns topic
## How to run this
1. Populate `.env` file with your AWS access creds and topic ARN:
```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
SNS_TOPIC_ARN=arn:aws:sns:ap-southeast-2:XXXXXX:topic_name
```
2. To run the scraper:
```commandline
docker compose up --build
```

## Updating products to be scraped
Update the yaml file referenced by environmental variable `PRODUCTS_YAML_FILE`.
A sample file called `ww_products.yml` is the default.
