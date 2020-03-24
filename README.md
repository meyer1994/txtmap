# TXTMAP

[![Build Status](https://travis-ci.org/meyer1994/txtmap.svg?branch=dev)](https://travis-ci.org/meyer1994/txtmap)
[![codecov](https://codecov.io/gh/meyer1994/txtmap/branch/dev/graph/badge.svg)](https://codecov.io/gh/meyer1994/txtmap)

This is an open source clone of [YourWorldOfText](https://www.yourworldoftext.com/)

## Development
You can deploy your own version very easily. This project uses [Serverless](serverless.com) and is built using AWS Lambda and RDS. However, it should be fairly easy to port it to Heroku, Google Cloud or any other.

To make changes:
```bash
(venv) $ pip install -r requirements-dev.txt
```

To Test:
```bash
$ make postgres test  # Will start a postgres container, using docker
$ make report  # Code coverage
```

### Stack
It uses AWS. Here is a list of the resources used:

- 1 PostgreSQL (RDS)
- 1 AWS Lambda Function
- 1 API Gateway V2 (WebSockets)

### Deploy
To deploy, you will need to have a database already up. We use SSM Parameter Store to store the DB password and host. See [here](https://serverless.com/framework/docs/providers/aws/guide/variables/#reference-variables-using-the-ssm-parameter-store) for more info.

After everything is done, just execute:
```bash
$ serverless deploy --verbose
```
