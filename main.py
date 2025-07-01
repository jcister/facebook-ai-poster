import os
import random
import feedparser
import google.generativeai as genai
import requests

# --- CONFIGURATION ---
# Load credentials from environment variables (best practice for security)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID")
FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")

# List of RSS feeds for graphic design news and trends
RSS_FEEDS = [
    "https://www.creativebloq.com/feeds/all",
    "http://feeds.feedburner.com/AigaEyeOnDesign",
    "https://itsnicethat.com/feed",
    "https://abduzeedo.com/rss.xml",
    "https://www.smashingmagazine.com/feed/",
]

# --- 1. FETCH LATEST ARTICLE FROM A RANDOM RSS FEED ---
def get_latest_article():
    """
    Picks a random feed, checks if it's valid, and fetches its most recent article.
    Retries a few times with different feeds if one fails.
    """
    # Create a copy of the feed list to modify
    feeds_to_try = RSS_FEEDS.copy()
    # Shuffle the list to try them in a random order each time
    random.shuffle(feeds_to_try)
    
    # Try up to 3 different feeds from the shuffled list
    for feed_url in feeds_to_try[:3]:
        try:
            print(f"Attempting to fetch from feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            # --- ROBUSTNESS CHECK ---
            # Check if the feed was parsed correctly AND has entries
            if feed and feed.entries:
                latest_entry = feed.entries[0]
                article = {
                    "title": latest_entry.title,
                    "link": latest_entry.link,
                    "summary": latest_entry.summary.split('<')[0] # Basic text extraction
                }
                print(f"Successfully found article: {article['title']}")
                return article # Success! Exit the function.
            else:
                # This handles cases where the feed is valid but empty
                print(f"Warning: Feed '{feed_url}' is empty or could not be parsed. Trying next one.")

        except Exception as e:
            # This handles network errors or other unexpected exceptions
            print(f"Error fetching or parsing feed '{feed_url}': {e}. Trying next one.")
            
    # If the loop finishes without returning, no articles were found
    print("Error: Could not retrieve an article from any of the tried feeds.")
    return None
    
# --- 2. GENERATE FACEBOOK POST WITH GEMINI ---
def create_facebook_post(article):
    """Uses Gemini to generate a post based on the article."""
    if not article:
        return None
        
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')

    prompt = f"""
    You are an expert social media manager for a Facebook page focused on professional graphic design. Your tone is insightful, engaging, and professional.

    Based on the following article, create a Facebook post. The post must:
    1.  Start with a strong, attention-grabbing hook.
    2.  Clearly summarize the key insight or takeaway from the article.
    3.  End with an open-ended question to encourage discussion.
    4.  Do NOT use the article title directly in the post.
    5.  Include 4-5 relevant hashtags like #GraphicDesign #DesignTrends #LayoutDesign #Typography #UIUX.
    6.  The entire post should be concise, ideally under 150 words.

    **Article Title:** {article['title']}
    **Article Summary:** {article['summary']}

    Now, write the Facebook post.
    """
    
    try:
        print("Generating post with Gemini...")
        response = model.generate_content(prompt)
        # Add the source link to the generated text
        generated_post = response.text + f"\n\nRead the full story here:\n{article['link']}"
        print("Post generated successfully.")
        return generated_post
    except Exception as e:
        print(f"Error generating content with Gemini: {e}")
        return None

# --- 3. PUBLISH TO FACEBOOK PAGE ---
def publish_to_facebook(post_content):
    """Publishes the generated content to the Facebook Page."""
    if not post_content:
        return

    post_url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/feed"
    payload = {
        'message': post_content,
        'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
    }

    try:
        print("Publishing to Facebook...")
        response = requests.post(post_url, data=payload)
        response.raise_for_status()  # Raises an exception for bad responses (4xx or 5xx)
        print("Successfully posted to Facebook page.")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Facebook: {e}")
        print(f"Response: {e.response.text}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("Starting the AI content agent...")
    latest_article = get_latest_article()
    if latest_article:
        facebook_post = create_facebook_post(latest_article)
        if facebook_post:
            publish_to_facebook(facebook_post)
    print("Agent run complete.")