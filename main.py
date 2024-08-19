# def extract_short_hadiths(file_path, filename, max_length=280):
#     short_hadiths = []
#
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             parts = line.split('|', 1)
#             if len(parts) == 2:
#                 hadith_number = parts[0].strip()
#                 hadith_text = parts[1].strip()
#
#                 if len(hadith_text) <= max_length:
#                     short_hadiths.append(f"{hadith_text} (from {filename})")
#
#     return short_hadiths
#
#
# def save_short_hadiths(short_hadiths, output_file):
#     with open(output_file, 'w', encoding='utf-8') as file:
#         for hadith in short_hadiths:
#             file.write(hadith + "\n")
import os
import random
import tweepy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials from environment variables
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


def extract_short_hadiths(file_path, filename, max_length=280):
    short_hadiths = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split('|', 1)
            if len(parts) == 2:
                hadith_number = parts[0].strip()
                hadith_text = parts[1].strip()

                if len(hadith_text) <= max_length:
                    short_hadiths.append(f"{hadith_text} (from {filename})")

    return short_hadiths


def save_short_hadiths(short_hadiths, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for hadith in short_hadiths:
            file.write(hadith + "\n")


def tweet_hadith(hadith_text):
    # Authenticate to Twitter API v2
    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=API_KEY,
                           consumer_secret=API_SECRET_KEY,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_TOKEN_SECRET)

    # Tweet the Hadith
    try:
        response = client.create_tweet(text=hadith_text)
        print(f"Successfully tweeted! Tweet ID: {response.data['id']}")
    except tweepy.TweepyException as e:
        print(f"Error occurred: {e}")


def main():
    output_file = 'short_hadiths.txt'

    if not os.path.exists(output_file):
        # Process the files and generate short_hadiths.txt if it doesn't exist
        hadith_files_dir = '.'  # Current directory; change if files are in another folder
        all_short_hadiths = []

        for filename in os.listdir(hadith_files_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(hadith_files_dir, filename)
                short_hadiths = extract_short_hadiths(file_path, filename)
                all_short_hadiths.extend(short_hadiths)

        save_short_hadiths(all_short_hadiths, output_file)
        print(f"Saved {len(all_short_hadiths)} short Hadiths to {output_file}")
    else:
        print(f"Reading short Hadiths from {output_file}")

    with open(output_file, 'r', encoding='utf-8') as file:
        all_short_hadiths = file.readlines()

    if all_short_hadiths:
        random_hadith = random.choice(all_short_hadiths)
        hadith_text = random_hadith.split(' (from ', 1)[0]
        print("\nRandom Short Hadith:\n")
        print(hadith_text.strip())

        # Tweet the random Hadith
        tweet_hadith(hadith_text.strip())
    else:
        print("No short Hadiths found.")


if __name__ == "__main__":
    main()
