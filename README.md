# From Layer Zero - AI Facebook Poster

This project contains the automation script responsible for generating and publishing content to the ["From Layer Zero" Facebook page](https://www.facebook.com/people/From-Layer-Zero/61575164066217/). It leverages Artificial Intelligence to create unique images and accompanying text, exploring themes of digital art and creativity.

## ✨ Benefits

*   **Automation**: Eliminates the manual effort of creating and posting content.
*   **Consistency**: Ensures a steady stream of new posts to keep the page's audience engaged.
*   **Creativity on Autopilot**: Continuously explores new artistic and textual ideas using AI prompts.
*   **Content Pipeline**: Provides a single, version-controlled place to manage the entire content generation and publishing process.

## 🛠️ Technologies Used

- **Python 3.8+**: Main programming language for automation.
- **Google Gemini API**: Used for both image and caption generation.
- **Facebook Graph API**: For posting content to Facebook.
- **python-dotenv**: For managing environment variables.
- **Requests**: For HTTP requests to APIs.

## ⚙️ Workflow

The script follows this workflow:

1.  **Content Generation**: The Google Gemini API is prompted to generate a new image based on a creative prompt.
2.  **Caption Creation**: Gemini is also used to generate a fitting, philosophical, or descriptive caption for the image.
3.  **Facebook API Integration**: The script authenticates with the Facebook Graph API using a page access token.
4.  **Automated Posting**: The generated image and text are uploaded and published as a new post on the "From Layer Zero" page.

This entire process can be scheduled to run at regular intervals (e.g., using a cron job on a server or a GitHub Action) for a fully autonomous content strategy.

## 🚧 Future Development

- **Video Generation**: Integrate AI video generation (e.g., using RunwayML or Pika Labs) for richer content.
- **Multi-Platform Posting**: Expand to Instagram, Twitter, or Threads.
- **Advanced Scheduling**: Add a scheduling system for more flexible posting times.
- **Analytics Dashboard**: Track engagement and post performance.
- **Custom Prompt Templates**: Allow dynamic prompt customization for both images and captions.
- **User Interface**: Build a simple web dashboard for managing posts and settings.

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

*   Python 3.8+
*   Git
*   Google Gemini API key
*   A Facebook Page Access Token with the necessary permissions (`pages_read_engagement`, `pages_manage_posts`)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/jcister/facebook-ai-poster.git
    cd facebook-ai-poster
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    *(You should create a `requirements.txt` file by running `pip freeze > requirements.txt` if needed)*
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a file named `.env` in the root directory and add your secret keys. The `.gitignore` file is already set up to protect this file from being committed.
    ```env
    # .env file
    FACEBOOK_PAGE_ID="your_page_id"
    FACEBOOK_ACCESS_TOKEN="your_long_lived_access_token"
    GEMINI_API_KEY="your_gemini_api_key"
    ```

### Usage

To run the script and post to your page, execute the main Python file:

```sh
python main.py
```