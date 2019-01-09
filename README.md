
##  Clone twitter account

A command line script to clone public profiles.
I'll use this account: https://twitter.com/ClonedProfile.

## Usage

```
usage: clone_profile.py [-h] [-p] [-c] [-d] [-f] [-up] [--user USER]

optional arguments:
  -h, --help    show this help message and exit
  -p, --print   print tweets from the given profile
  -c, --clone   clone some tweets from the given profile
  -d, --delete  delete all tweets from the account
  -f, --follow  follow all users from the given profile
  -up           update profile photo using the profile photo from the given
                profile
  --user USER   provide user to clone from the command line
  ```
  
  ## Configuration file
You have to repleace "X" in ___access.py___ file by your corresponding authentication data.
```
[access.py]
CONSUMER_KEY = YOUR_CONSUMER_KEY_HERE
CONSUMER_SECRET = YOUR_CONSUMER_SECRET_HERE
ACCESS_TOKEN = YOUR_ACCESS_TOKEN_HERE
ACCESS_SECRET = YOUR_ACCESS_TOKEN_SECRET_HERE
```

## Examples
A couple of example calls from the command line:
Delete all tweets:
```
python3 clone_profile.py --delete
```
Clone the last 20 tweets from @BarackObama:
```
python3 clone_profile.py --clone --user BarackObama  
```
Update the profile cloning @BarackObama:
```
python3 clone_profile.py -up --user BarackObama  
``` 

## Requeriments
- python 3
- tweepy

## License
MIT
