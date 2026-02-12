import json
from playwright.sync_api import sync_playwright
from fetch_performer_job_links import fetch_performer_job_links 


def scrape_job_descriptions(url_list):
    job_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for url in url_list:
            try:
                page.goto(url, wait_until="domcontentloaded")
                
                # 1. Extract ID from the URL 
                # Example: "https://site.com/job/software-eng-99827" -> "99827"
                # This splits by '/' and takes the last element
                job_id = url.rstrip('/').split('/')[-1]

                # 2. Capture the description text
                description_element = page.locator("h4:has-text('DESCRIPTION') + p")
                description = description_element.inner_text().strip() if description_element.count() > 0 else "N/A"

                # 3. Create the object
                job_obj = {
                    "id": job_id,
                    "url": url,
                    "description": description
                }
                
                job_results.append(job_obj)
                print(f"Processed Job ID: {job_id}")

            except Exception as err:
                print(f"Skipping {url} due to error: {err}")

        browser.close()
        
        # write to file
        output_file_name = "job_descriptions.json"
        with open(output_file_name, "w") as f:
            json.dump(job_results, f, indent=4)
    # return job_results

# Execute and Save
links = fetch_performer_job_links("https://playbill.com/jobs")

final_data = scrape_job_descriptions(links)

