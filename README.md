# Sentiment Analysis of Wendys tweets

Grab n amount of tweets from given range with words "wendys spicy nuggets" and use textblob to determine a polarity score. This script is python3 only.

- pip install -r requirements.txt

## Purpose

This is a demonstration of how to query tweets from older than 7 days and run sentiment anaylsis on them. This example is comparing the polarity of tweets before and after Wendys released their spicy nuggets. The output proves the amount of positive tweets about Wendys went up after they released the nuggets.

## Output Example

```bash
----Announcement to reveal----
Positive tweets percentage: 21.64486862259927 %
Negative tweets percentage: 32.26110521974785 %
Neutral tweets percentage: 46.094026157652884 %


----Reveal to current----
Positive tweets percentage: 36.0 %
Negative tweets percentage: 27.0 %
Neutral tweets percentage: 37.0 %
```