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

                # 2. Capture the full job description
                # find all sections with class "jobs-section"
                description_sections = page.locator(".jobs-section").all()
                
                description_sections_text = []
                # examine each section and pull all inner text
                for section in description_sections:
                    section_text = section.inner_text()
                    clean_section_text = section_text.strip()
                    description_sections_text.append(clean_section_text)
                
                # combine all section text into one text object
                all_text_combined = "\n".join(description_sections_text)
                all_text_cleaned = all_text_combined.strip()

                # capture job title
                
                job_title = page.locator(".bsp-component-title.jobs-page-title")
                job_title_text = job_title.inner_text()

                # 3. Create the object
                job_obj = {
                    "id": job_id,
                    "title": job_title_text,
                    "url": url,
                    "description": all_text_cleaned
                }
                
                job_results.append(job_obj)
                print(f"Processed Job ID: {job_id}", flush=True)

            except Exception as err:
                print(f"Skipping {url} due to error: {err}", flush=True)

        browser.close()
        
        # write to file
        output_file_path = "./output_files/job_descriptions.json"
        with open(output_file_path, "w") as f:
            json.dump(job_results, f, indent=4)
    # return job_results

# Execute and Save
links = fetch_performer_job_links("https://playbill.com/jobs")

final_data = scrape_job_descriptions(links)

