
##  Clone twitter account

A command line script to clone public profiles.
I'll use this account: https://twitter.com/ClonedProfile.

## Usage

```
usage: clone_profile.py [-h] [-p PRINT] [-c CLONE] [-d] [-f FOLLOW] [-up]
                        [--user USER] [--export EXPORT]

optional arguments:
  -h, --help            show this help message and exit
  -p PRINT, --print PRINT
                        print N tweets from the given profile
  -c CLONE, --clone CLONE
                        clone N tweets from the given profile
  -d, --delete          delete all tweets from the authenticated account
  -f FOLLOW, --follow FOLLOW
                        follow N users from the given profile [slow]
  -up                   update profile data using the profile cloning the
                        given profile
  --user USER           provide user to clone from the command line
  --export EXPORT       in proccess...

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
Clone the last 111 tweets from @BarackObama:
```
python3 clone_profile.py --clone 111 --user BarackObama  
```
Update the profile cloning @BarackObama:
```
python3 clone_profile.py -up --user BarackObama  
``` 
Follow 10 users from @BarackObama:
```
python3 clone_profile.py -f 10 --user BarackObama  
``` 

## Requeriments
- python 3
- tweepy

## License
MIT
