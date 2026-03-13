import os
import json
import tweepy
import anthropic

# --- Twitter client ---
twitter = tweepy.Client(
    bearer_token=os.environ.get("BEARER_TOKEN"),
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token=os.environ["ACCESS_KEY"],
    access_token_secret=os.environ["ACCESS_SECRET"],
)

# --- Claude client ---
claude = anthropic.Anthropic()

SEARCH_QUERY = os.environ.get("SEARCH_QUERY", "Python -is:retweet lang:ja")
MAX_RESULTS = int(os.environ.get("MAX_RESULTS", "10"))
# フィルターのオン/オフ: FILTER_ENABLED=false で無効化 (デフォルト: 有効)
FILTER_ENABLED = os.environ.get("FILTER_ENABLED", "true").lower() not in ("false", "0", "no")


def fetch_tweets():
    response = twitter.search_recent_tweets(
        query=SEARCH_QUERY,
        max_results=MAX_RESULTS,
        tweet_fields=["created_at", "author_id", "text"],
    )
    return response.data or []


def filter_meaningful(tweets):
    """Claude APIで無意味なツイートを除外する。有意義なツイートのインデックスリストを返す。"""
    tweet_list = [
        {"index": i, "text": t.text}
        for i, t in enumerate(tweets)
    ]

    response = claude.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=(
            "あなたはSNSコンテンツのフィルタリング専門家です。"
            "与えられたツイートリストを分析し、有意義なツイートのindexのみをJSON配列で返してください。\n"
            "除外すべきツイートの例:\n"
            "- スパム・宣伝・アフィリエイトリンクのみ\n"
            "- 意味のない一言（「おはよう」「疲れた」のみ等）\n"
            "- 絵文字や記号だけで構成されたもの\n"
            "- 同じ文言の繰り返し\n"
            "有意義なツイートの例:\n"
            "- 技術的な知見や情報共有\n"
            "- 意見・考察・議論\n"
            "- ニュース・出来事の報告\n"
            "出力形式: {\"meaningful_indices\": [0, 2, 3, ...]}"
        ),
        messages=[
            {
                "role": "user",
                "content": f"以下のツイートをフィルタリングしてください:\n{json.dumps(tweet_list, ensure_ascii=False, indent=2)}",
            }
        ],
    )

    text = next(b.text for b in response.content if b.type == "text")
    result = json.loads(text)
    return set(result.get("meaningful_indices", []))


def main():
    tweets = fetch_tweets()
    if not tweets:
        print("No tweets found.")
        return

    print(f"Query: {SEARCH_QUERY}")
    print(f"Fetched: {len(tweets)} tweets")

    if FILTER_ENABLED:
        print("Filter: ON — filtering with Claude...\n")
        meaningful_indices = filter_meaningful(tweets)
        kept = [t for i, t in enumerate(tweets) if i in meaningful_indices]
        dropped = len(tweets) - len(kept)
        print(f"Result: {len(kept)} kept / {dropped} dropped\n")
    else:
        print("Filter: OFF\n")
        kept = tweets
    print("=" * 60)
    for tweet in kept:
        print(f"[{tweet.created_at}] author:{tweet.author_id}")
        print(f"  {tweet.text}")
        print()


if __name__ == "__main__":
    main()
