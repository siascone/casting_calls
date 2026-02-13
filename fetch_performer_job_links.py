from playwright.sync_api import sync_playwright

def fetch_performer_job_links(url):
    with sync_playwright() as p:
        # Launch browser (headless=False lets you watch the magic happen)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        links = []
        page_count = 1
        
        # find categories and select performer
        category_selector = page.locator("#bsp-jobs-list-category")
        category_selector.select_option(value="Performer")
        # wait for postings to reload
        # page.locator("#component-saozdn").wait_for()
        page.wait_for_load_state("load")
        
        paid_selector = page.locator("#bsp-jobs-list-isPaid")
        paid_selector.select_option(value="1")
        # wait for postings to reload
        # page.locator("#component-saozdn").wait_for()
        page.wait_for_load_state("load")
        
        work_type_selector = page.locator("#bsp-jobs-list-isInternship")
        work_type_selector.select_option(value="0")
        # wait for postings to reload
        # page.locator("#component-saozdn").wait_for()
        page.wait_for_load_state("load")
        
        # pull first 2 pages of links to postings
        while page_count <= 2:
            print(f"Scraping page {page_count}...", flush=True)
            
            # 1. Collect the information
            # listings = page.locator(".loadmore-item").all_text_content()
            # all_data.extend(listings)
            
            # 1. Locate all parent containers with the specific class
            # Replace 'item-container-class' with your actual class name
            jobs = page.locator(".loadmore-item").all()
            
            for job in jobs:
                # Use the 'item' locator as the starting point to find the <a> tag
                # The '>>' syntax or chaining .locator() searches specifically inside this div
                link_element = job.locator("a")
                
                # 3. Extract the info you need
                link_url = link_element.get_attribute("href")
                # link_text = link_element.inner_text()
                
                links.append(link_url)
                
                # print(f"Found link: {link_text} -> {link_url}")

            # 2. Find the "Next" button
            # 'text="Next"' is a powerful Playwright selector
            # next_button = page.get_by_role("button", name="Next")

            more_button = page.locator("#load-more-oob")

            # 3. Check if it exists and is visible
            if more_button.is_visible():
                more_button.click()
                
                # Wait for the network to settle or a specific element to load
                page.wait_for_load_state("load")
                page_count += 1
            else:
                print("No more pages found.", flush=True)
                break

        print(f"Scraped {len(links)} job links total.", flush=True)
        browser.close()
        
        output_file_path = "./output_files/job_links.txt"
        with open(output_file_path, 'w') as file:
            file.write('\n'.join(links))
            
        return links

# Example usage:
# fetch_performer_job_links("https://playbill.com/jobs")
