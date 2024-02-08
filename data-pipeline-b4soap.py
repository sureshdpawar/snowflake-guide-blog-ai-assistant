import os
import requests
from bs4 import BeautifulSoup
import html2text

def download_and_save_in_markdown(url: str, dir_path: str) -> None:
    """Download the HTML content from the web page and save it as a markdown file."""
    # Extract a filename from the URL
    if url.endswith("/"):
        url = url[:-1]
    filename = url.split("/")[-1] + ".md"
    print(f"Downloading {url} into {filename}...")

    # Fetch the content using requests
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Convert to text using html2text
    h = html2text.HTML2Text()
    h.ignore_links = False
    markdown_content = h.handle(str(soup))

    # Write the markdown content to a file
    file_path = os.path.join(dir_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

def download(pages):
    """Download the HTML content from the pages and save them as markdown files."""
    base_dir = os.getcwd()  # Use the current working directory
    dir_path = os.path.join(base_dir, "content", "blogs")
    os.makedirs(dir_path, exist_ok=True)
    for page in pages:
        download_and_save_in_markdown(page, dir_path)
    return dir_path

PAGES = [
    "https://quickstarts.snowflake.com/guide/data_engineering_pipelines_with_snowpark_python",
    "https://quickstarts.snowflake.com/guide/cloud_native_data_engineering_with_matillion_and_snowflake",
    "https://quickstarts.snowflake.com/guide/data_engineering_with_apache_airflow",
    "https://quickstarts.snowflake.com/guide/getting_started_with_dataengineering_ml_using_snowpark_python",
    "https://quickstarts.snowflake.com/guide/data_engineering_with_snowpark_python_and_dbt"
]

if __name__ == "__main__":
    download(PAGES)
