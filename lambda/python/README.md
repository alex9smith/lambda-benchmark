# Python lambda

## Build

```bash
rm -rf deploy
rm -f deploy.zip
pip install -r requirements.txt --target ./deploy
cd deploy
zip -r ../deploy.zip .
cd ..
zip deploy.zip lambda_function.py
```
