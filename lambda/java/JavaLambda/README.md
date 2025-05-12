# App

This project contains an AWS Lambda maven application with [AWS Java SDK 2.x](https://github.com/aws/aws-sdk-java-v2) dependencies.

## Prerequisites

- Java 1.8+
- Apache Maven

## Development

The generated function handler class just returns the input. The configured AWS Java SDK client is created in `DependencyFactory` class and you can
add the code to interact with the SDK client based on your use case.

#### Building the project

```
AWS_REGION=eu-west-2 mvn clean install
```

#### Testing it locally

```
AWS_REGION=eu-west-2 mvn test
```

#### Adding more SDK clients

To add more service clients, you need to add the specific services modules in `pom.xml` and create the clients in `DependencyFactory` following the same
pattern as dynamoDbClient.
