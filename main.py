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

# A wide and trendy list of sources for diverse content
RSS_FEEDS = [
    # === Core Industry News & Trends ===
    "https://www.creativebloq.com/feeds/all",
    "https://www.itsnicethat.com/feed",
    "https://www.smashingmagazine.com/feed/",

    # === Tutorials & How-Tos (Blogs) ===
    "https://blog.spoongraphics.co.uk/feed",      # Spoon Graphics for tutorials & freebies
    "https://design.tutsplus.com/articles.atom",  # Envato Tuts+ for tutorials

    # === Tutorials & Inspiration (YouTube) ===
    # Phlearn (Photoshop Tutorials)
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC47XN5gaAoH24i-hGv30GqQ",
    # Satori Graphics (Illustrator & Design Theory)
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCsItrB-6tAfoP2s2L7sL4-w",
    # The Futur (Business of Design)
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC-b3c7kxa5vU-bnmaROgvog",

    # === What's Trending RIGHT NOW (Reddit) ===
    "https://www.reddit.com/r/graphic_design.rss",
    "https://www.reddit.com/r/photoshop.rss",
    "https://www.reddit.com/r/AdobeIllustrator.rss",

    # === Visual Inspiration ===
    "https://www.booooooom.com/feed/",
    "https://abduzeedo.com/rss.xml",
]


# --- 1. FETCH LATEST ARTICLE FROM A RANDOM RSS FEED ---
def get_latest_article():
    """
    Picks a random feed, checks if it's valid, and fetches its most recent article.
    Retries a few times with different feeds if one fails.
    """
    feeds_to_try = RSS_FEEDS.copy()
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
                # Basic text extraction, removing HTML tags
                summary_text = latest_entry.summary.split('<')[0]
                
                article = {
                    "title": latest_entry.title,
                    "link": latest_entry.link,
                    "summary": summary_text 
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
    # Using a modern, capable model
    model = genai.GenerativeModel('gemini-1.5-pro-latest') 

    prompt = f"""
    You are the fun, passionate, and knowledgeable voice for a popular graphic design Facebook page. Your personality is like a friendly design mentor who gets excited about cool tips, amazing art, and clever ideas.

    **Your Audience:** A vibrant mix of seasoned pros, design students, hobbyists, and people just curious about creative work. Your tone must be engaging, approachable, and easy to understand. Avoid overly technical jargon.

    **Your Task:** Based on the article below, write a short, exciting Facebook post.

    **RULES:**
    1.  **Hook Them In:** Start with a relatable question or a "Wow!" statement.
    2.  **Share the Core Idea:** Simply explain the coolest or most useful point from the article. Think "Hey, did you know..." or "Here's a neat trick...".
    3.  **Spark a Conversation:** End with a fun, open-ended question that anyone can answer.
    4.  **Be Human:** Use simple language. It's okay to be a little playful or add a touch of humor if the topic allows.
    5.  **Hashtags:** Include 4-5 relevant and friendly hashtags. Mix professional (#GraphicDesign, #Typography) with community tags (#DesignInspo, #CreativeLife, #LearnDesign).

    **CRITICAL INSTRUCTION:** Your entire response must be ONLY the text of the Facebook post itself. Do NOT include any introductory phrases like "Of course!", "Here is the post:", or any other text outside of the post content. The response must start DIRECTLY with the first word of the Facebook post's hook.

    ---
    **ARTICLE TO PROCESS:**
    **Title:** {article['title']}
    **Summary:** {article['summary']}
    ---

    Now, create the post.
    """
    
    try:
        print("Generating post with Gemini...")
        response = model.generate_content(prompt)
        # Use .strip() to remove any accidental leading/trailing whitespace from the AI's response
        generated_post = response.text.strip() + f"\n\nRead the full story here:\n{article['link']}"
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