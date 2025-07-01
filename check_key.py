import os

print("--- Checking Environment Variables ---")

# Check for the Gemini Key
gemini_key = os.environ.get("GEMINI_API_KEY")
if gemini_key:
    # Print only the last 4 characters for security
    print(f"SUCCESS: Found GEMINI_API_KEY ending in '...{gemini_key[-4:]}'")
else:
    print("FAILURE: GEMINI_API_KEY was not found.")

# Check for the Facebook Page ID
page_id = os.environ.get("FACEBOOK_PAGE_ID")
if page_id:
    print(f"SUCCESS: Found FACEBOOK_PAGE_ID: {page_id}")
else:
    print("FAILURE: FACEBOOK_PAGE_ID was not found.")

print("------------------------------------")