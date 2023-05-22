# TikTokHTTPInterceptor (iOS)

This script lets you hook some Objective-C methods involved in HTTP requests creation and responses processing.

To compile the agent just run from the main folder:
```
make
```

Install dependencies with:
```
pip3 install -r requirements.txt
```

And start to intercept HTTP requests and responses with:
```
python3 main.py -U -f com.zhiliaoapp.musically
```

NB: I do not guarantee that this script intercepts all HTTP traffic made by the app. Maybe other requests/responses are processed by other classes/methods I currently do not hook.
