# Phishing Website Detection

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0-green.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-1.5-orange.svg)
![MLflow](https://img.shields.io/badge/MLflow-1.20-purple.svg)
![Docker](https://img.shields.io/badge/Docker-20.10-lightblue.svg)
![Render](https://img.shields.io/badge/Render-Cloud-deepgreen.svg)

This project focuses on detecting phishing websites using machine learning techniques. The goal is to build a robust model that can accurately classify websites as either phishing or legitimate based on various features extracted from the URL.

## Table of Contents

- [Introduction](#introduction)
- [Dataset](#dataset)
- [Features](#features)
- [Machine Learning Models](#machine-learning-models)
- [Model Tracking with MLflow](#model-tracking-with-mlflow)
- [Deployment](#deployment)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Docker](#docker)
- [CI/CD with GitHub Actions](#cicd-with-github-actions)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Phishing websites are designed to deceive users into providing sensitive information such as usernames, passwords, and credit card details. This project aims to detect such malicious websites using machine learning models trained on a dataset of URLs labeled as either phishing or legitimate.

## Dataset

The dataset used in this project is available [here](https://github.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/blob/master/DataFiles/5.urldata.csv). It contains various features extracted from URLs, such as URL length, presence of IP address, and domain age, among others.

## Features

The following features are extracted from each URL:

- **Have_IP**: Presence of an IP address in the URL.
- **Have_At**: Presence of '@' symbol in the URL.
- **URL_Length**: Length of the URL.
- **URL_Depth**: Depth of the URL path.
- **Redirection**: Presence of redirection in the URL.
- **https_Domain**: Use of HTTPS in the domain.
- **TinyURL**: Use of URL shortening services.
- **Prefix/Suffix**: Presence of prefix or suffix in the domain.
- **DNS_Record**: Presence of DNS record for the domain.
- **Domain_Age**: Age of the domain.
- **Domain_End**: Expiration date of the domain.
- **iFrame**: Presence of iframe in the webpage.
- **Mouse_Over**: Presence of mouseover events in the webpage.
- **Right_Click**: Presence of right-click disabling in the webpage.
- **Web_Forwards**: Presence of web forwarding in the webpage.

## Machine Learning Models

Several machine learning models were evaluated for this project:

- **Decision Tree**
- **Random Forest**
- **Logistic Regression**
- **XGBoost**

After thorough evaluation, **XGBoost** was chosen as the final model due to its superior performance in terms of accuracy and robustness.

## Model Tracking with MLflow

MLflow was used to track the performance of different models. This allowed for easy comparison of metrics such as accuracy, precision, recall, and F1-score. The best-performing model (XGBoost) was then selected for deployment.

## Deployment

The model was deployed using **Flask** and containerized with **Docker**. The application is hosted on **Render**, a cloud platform that provides seamless deployment and scaling.

## Usage

To use the phishing detection service, you can send a POST request to the `/predict_url` endpoint with the URL you want to check.

### Example Request

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "http://example.com"}' http://your-render-app-url/predict_url

---
title: "Phishing Detection API"
author: "Your Name"
date: "`r Sys.Date()`"
output: github_document
---

# API Endpoints

## `GET /`
Renders the home page.

## `POST /predict_url`
Accepts a JSON object with a URL and returns a prediction.

### Example Response
```json
{
    "is_phishing": 0,
    "result": "Legitimate Website"
}
```

# Docker

The application is containerized using Docker. To build and run the Docker container:

```bash
docker build -t phishing-detection .
docker run -p 5001:5001 phishing-detection
```

# CI/CD with GitHub Actions

Continuous Integration and Continuous Deployment (CI/CD) is implemented using GitHub Actions. Every push to the `main` branch triggers a workflow that:

- Builds the Docker image
- Runs tests
- Deploys the application to Render

# Requirements

The project dependencies are listed in the `requirements.txt` file. Below is a breakdown of the key packages used:

## Core Libraries

- **Flask**: A lightweight web framework for building the API.
- **requests**: A library for making HTTP requests, used for fetching webpage content.
- **beautifulsoup4**: A library for parsing HTML and extracting features like iframes.
- **python-whois**: A library for querying WHOIS information about domains.

## Machine Learning Libraries

- **scikit-learn**: Used for preprocessing and model evaluation.
- **xgboost**: An optimized gradient boosting library for training the final model.
- **pandas**: Used for handling datasets and feature extraction.
- **numpy**: Used for numerical computations.

## Visualization and Tracking

- **seaborn**: Used for exploratory data analysis (EDA).
- **matplotlib**: Used for creating visualizations.
- **mlflow**: Used for tracking experiments and model performance.

## Deployment

- **gunicorn**: A WSGI HTTP server for serving the Flask app in production.

To install all dependencies, run:

```bash
pip install -r requirements.txt
```

# Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

# License

This project is licensed under the MIT License. See the `LICENSE` file for details.
