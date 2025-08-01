
# App

This project contains an AWS Lambda maven application with [AWS Java SDK 2.x](https://github.com/aws/aws-sdk-java-v2) dependencies.

## Prerequisites

- jenv (for managing multiple JDKs)
- Apache Maven
- Oracle GraalVM native image

## Set up native-image compiler on OSX

```
brew install jenv
# follow shell profile instructions
brew install --cask graalvm/tap/graalvm-community-jdk21
jenv add /Library/Java/JavaVirtualMachines/graalvm-community-openjdk-21/Contents/Home
jenv global 21
```

Now there are lots of frustrating OSX errors to allow the JDK executables to run.

Repeat:

```
AWS_REGION=eu-west-2 mvn -Pnative package
```

- click 'done' on popup
- Settings -> Privacy & Security -> scroll to bottom -> 'open anyway'
- re-run mvn -Pnative package
- next time click 'open anyway' in the popup

Once you get this error:

```
Error adding file to archive: .../lambda-benchmark/lambda/graalvm/GraalVMLambda/target/libaws-crt-jni.so -
```

You need to extract the linux arm64 jni from the CRT jar - by default on OSX only the darwin version is used which is not compatible with Graviton Lambdas.

```
jar xvf target/GraalVMLambda.jar jni/libaws-lambda-jni.linux-aarch_64.so
mv jni/libaws-lambda-jni.linux-aarch_64.so target/libaws-crt-jni.so
```

Now the package command should work

```
AWS_REGION=eu-west-2 mvn -Pnative package
```

## Development

The generated function handler class just returns the input. The configured AWS Java SDK client is created in `DependencyFactory` class and you can
add the code to interact with the SDK client based on your use case.

#### Building the project

```
AWS_REGION=eu-west-2 mvn -Pnative package
```

#### Testing it locally

```
AWS_REGION=eu-west-2 mvn test
```

#### Adding more SDK clients

To add more service clients, you need to add the specific services modules in `pom.xml` and create the clients in `DependencyFactory` following the same
pattern as dynamoDbClient.
