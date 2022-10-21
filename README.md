# Groceries Price History Tracker
## What is this?
This project is a webapp which tracks the change in cost of my groceries over time due to inflation.

At the moment this project only tracks a handful of products from a single supermarket website.
## Show me (demo)
http://groceries-data-frontend.s3-website-ap-southeast-2.amazonaws.com

## Backend System Design
Main Components:
- Rest API exposed by API Gateway
- DynamoDB tables - Price History Data
- Scraper - running on a home PC
![Backend System Design](https://user-images.githubusercontent.com/10220603/197082334-687c44bd-b586-4a6f-9069-58f5ca614bf8.png)

## Scraper
Uses a Debian Docker container, running Python and Selenium (Chrome) to scrape product info and price data.

The supermarket website in question requires JavaScript to load the price information from its REST API.
Therefore, scraping isn't as simple as just requesting the HTML & parsing it...

## Frontend
Simple React app which also uses Material UI and recharts.

Calls the REST API exposed by the backend API Gateway.

## TODO
- Better test coverage
  - frontend tests
  - testcontainers for scraper
- Frontend
  - Make it look better.
  - Chart: adjust timescale by day, week, month, year.
  - Product images
- Handle when supermarket website changes the URL for a product.
- Support other supermarket websites
- Compare product pricing between websites
- Cloudformation template for all AWS resources used
