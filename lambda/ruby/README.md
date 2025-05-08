# Ruby lambda

## Tests

```bash
bundle exec rake test
```

## Build for deploy

First time setup:

```bash
gem install bundler
```

Install the dependencies locally:

```bash
bundle config set --local path 'vendor/bundle' && bundle install
```

> If you need to install globally again later, run
>
> ```bash
> bundle config set --local system 'true'
> ```

Zip the dependencies and Ruby code together:

```bash
rm -f deploy.zip
zip -r deploy.zip vendor
zip -uj deploy.zip lib/lambda_function.rb
```
