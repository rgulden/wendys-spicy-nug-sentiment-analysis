import urllib.parse, urllib.request, http.cookiejar
import json, re, datetime, sys
from pyquery import PyQuery


class TweetManager:
    def __init__(self):
        self.maxTweets = 0
        self.within = "15mi"

    def setUsername(self, username):
        self.username = username
        return self

    def setSince(self, since):
        self.since = since
        return self

    def setUntil(self, until):
        self.until = until
        return self

    def setQuerySearch(self, querySearch):
        self.querySearch = querySearch
        return self

    def setMaxTweets(self, maxTweets):
        self.maxTweets = maxTweets
        return self

    def setTopTweets(self, topTweets):
        self.topTweets = topTweets
        return self

    def setNear(self, near):
        self.near = near
        return self

    def setWithin(self, within):
        self.within = within
        return self

    def getTweets(self, receiveBuffer=None, bufferLength=100, proxy=None):
        refreshCursor = ""

        results = []
        resultsAux = []
        cookieJar = http.cookiejar.CookieJar()

        if (
            hasattr(self, "username")
            and (self.username.startswith("'") or self.username.startswith('"'))
            and (self.username.endswith("'") or self.username.endswith('"'))
        ):
            self.username = self.username[1:-1]

        active = True

        while active:
            json = self.getJsonReponse(refreshCursor, cookieJar, proxy)
            if len(json["items_html"].strip()) == 0:
                break

            refreshCursor = json["min_position"]
            scrapedTweets = PyQuery(json["items_html"])
            # Remove incomplete tweets withheld by Twitter Guidelines
            scrapedTweets.remove("div.withheld-tweet")
            tweets = scrapedTweets("div.js-stream-tweet")

            if len(tweets) == 0:
                break

            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)

                usernameTweet = tweetPQ("span:first.username.u-dir b").text()
                txt = re.sub(
                    r"\s+",
                    " ",
                    tweetPQ("p.js-tweet-text")
                    .text()
                    .replace("# ", "#")
                    .replace("@ ", "@"),
                )
                retweets = int(
                    tweetPQ(
                        "span.ProfileTweet-action--retweet span.ProfileTweet-actionCount"
                    )
                    .attr("data-tweet-stat-count")
                    .replace(",", "")
                )
                favorites = int(
                    tweetPQ(
                        "span.ProfileTweet-action--favorite span.ProfileTweet-actionCount"
                    )
                    .attr("data-tweet-stat-count")
                    .replace(",", "")
                )
                dateSec = int(
                    tweetPQ("small.time span.js-short-timestamp").attr("data-time")
                )
                id = tweetPQ.attr("data-tweet-id")
                permalink = tweetPQ.attr("data-permalink-path")

                geo = ""
                geoSpan = tweetPQ("span.Tweet-geo")
                if len(geoSpan) > 0:
                    geo = geoSpan.attr("title")

                tweet = {
                    "id": id,
                    "permalink": "https://twitter.com" + permalink,
                    "username": usernameTweet,
                    "text": txt,
                    "date": datetime.datetime.fromtimestamp(dateSec),
                    "retweets": retweets,
                    "favorites": favorites,
                    "geo": geo,
                    "mentions": "",
                    "hashtags": "",
                }

                tweet["mentions"] = " ".join(
                    re.compile("(@\\w*)").findall(tweet["text"])
                )
                tweet["hashtags"] = " ".join(
                    re.compile("(#\\w*)").findall(tweet["text"])
                )

                results.append(tweet)
                resultsAux.append(tweet)

                if receiveBuffer and len(resultsAux) >= bufferLength:
                    receiveBuffer(resultsAux)
                    resultsAux = []

                if self.maxTweets > 0 and len(results) >= self.maxTweets:
                    active = False
                    break

        if receiveBuffer and len(resultsAux) > 0:
            receiveBuffer(resultsAux)

        return results

    def getJsonReponse(self, refreshCursor, cookieJar, proxy):
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

        urlGetData = ""

        if hasattr(self, "username"):
            urlGetData += " from:" + self.username

        if hasattr(self, "querySearch"):
            urlGetData += " " + self.querySearch

        if hasattr(self, "near"):
            urlGetData += "&near:" + self.near + " within:" + self.within

        if hasattr(self, "since"):
            urlGetData += " since:" + self.since

        if hasattr(self, "until"):
            urlGetData += " until:" + self.until

        if hasattr(self, "topTweets"):
            if self.topTweets:
                url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"

        url = url % (urllib.parse.quote(urlGetData), urllib.parse.quote(refreshCursor))

        headers = [
            ("Host", "twitter.com"),
            (
                "User-Agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            ),
            ("Accept", "application/json, text/javascript, */*; q=0.01"),
            ("Accept-Language", "de,en-US;q=0.7,en;q=0.3"),
            ("X-Requested-With", "XMLHttpRequest"),
            ("Referer", url),
            ("Connection", "keep-alive"),
        ]

        if proxy:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({"http": proxy, "https": proxy}),
                urllib.request.HTTPCookieProcessor(cookieJar),
            )
        else:
            opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(cookieJar)
            )
        opener.addheaders = headers

        try:
            response = opener.open(url)
            jsonResponse = response.read()
        except:
            print(
                "Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd"
                % urllib.parse.quote(urlGetData)
            )
            return None

        dataJson = json.loads(jsonResponse)

        return dataJson
