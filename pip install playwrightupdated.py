import csv
import re

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
INVALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")

# Expanded mock dataset simulating scraped Google Business Profiles & websites
MOCK_BUSINESSES = [
    {
        "name": "Lakeview Dental Studio",
        "business_type": "Dentist",
        "city": "Chicago",
        "website": "https://www.lakeviewdental.example.com",
        "homepage_html": "<div>Welcome! Hero image: smile@2x.png</div>",
        "contact_html": "<p>Appointments: care@lakeviewdental.example.com | billing@lakeviewdental.example.com</p>",
    },
    {
        "name": "Windy City Orthodontics",
        "business_type": "Dentist",
        "city": "Chicago",
        "website": "https://www.windycityortho.example.com",
        "homepage_html": "<a href='mailto:info@windycityortho.example.com'>Email Us</a><footer>INFO@WINDYCITYORTHO.EXAMPLE.COM</footer>",
        "contact_html": "",
    },
    {
        "name": "roast & pour Coffee Co.",
        "business_type": "Cafe",
        "city": "Chicago",
        "website": "https://www.roastandpour.example.com",
        "homepage_html": "<img src='latte@3x.jpg'><p>Walk-ins only, no email support.</p>",
        "contact_html": "<form>Contact Form</form>",
    },
    {
        "name": "Brooklyn Bean Roasters",
        "business_type": "Cafe",
        "city": "New York",
        "website": "https://www.brooklynbean.example.com",
        "homepage_html": "<div>Specialty Coffee</div>",
        "contact_html": "<span>Wholesale: orders@brooklynbean.example.com, Press: hello@brooklynbean.example.com</span>",
    },
    {
        "name": "Hudson Digital Marketing",
        "business_type": "Marketing Agency",
        "city": "New York",
        "website": "https://www.hudsondigital.example.com",
        "homepage_html": "<footer>newbiz@hudsondigital.example.com</footer>",
        "contact_html": "<footer>newbiz@hudsondigital.example.com</footer>",
    },
    {
        "name": "Manhattan Smile Care",
        "business_type": "Dentist",
        "city": "New York",
        "website": "https://www.manhattansmile.example.com",
        "homepage_html": "<div>logo@2x.svg</div>",
        "contact_html": "<p>Reach our front desk: desk@manhattansmile.example.com</p>",
    },
    {
        "name": "Lone Star Growth Agency",
        "business_type": "Marketing Agency",
        "city": "Austin",
        "website": "https://www.lonestargrowth.example.com",
        "homepage_html": "<p>Let's scale: pitch@lonestargrowth.example.com</p>",
        "contact_html": "",
    },
    {
        "name": "South Congress Espresso",
        "business_type": "Cafe",
        "city": "Austin",
        "website": "https://www.sococoffee.example.com",
        "homepage_html": "<div>Open 7am - 6pm</div>",
        "contact_html": "<p>Catering: events@sococoffee.example.com</p>",
    },
]


def extract_emails(html_content):
    matches = re.findall(EMAIL_REGEX, html_content)
    clean_emails = set()

    for email in matches:
        lowered = email.lower()
        if not lowered.endswith(INVALID_EXTENSIONS):
            clean_emails.add(lowered)

    return sorted(list(clean_emails))


def filter_businesses(businesses, city_query, type_query):
    matched = []
    for biz in businesses:
        city_match = not city_query or city_query in biz["city"].lower()
        type_match = not type_query or type_query in biz["business_type"].lower()

        if city_match and type_match:
            matched.append(biz)

    return matched


def run_scraper():
    print("--- Business Lead & Email Extractor (Mock Mode) ---")
    print("Available sample cities: Chicago, New York, Austin")
    print("Available sample types: Dentist, Cafe, Marketing Agency\n")

    city_input = input("Enter target city (or press Enter for all): ").strip().lower()
    type_input = input("Enter business type (or press Enter for all): ").strip().lower()

    filtered = filter_businesses(MOCK_BUSINESSES, city_input, type_input)

    if not filtered:
        print("\nNo businesses matched your search criteria.")
        return

    results = []
    total_emails = 0

    print(f"\nFound {len(filtered)} matching business(es). Extracting emails...\n")

    for biz in filtered:
        # Step 1: Check homepage HTML
        emails = extract_emails(biz["homepage_html"])
        source = "Homepage"

        # Step 2: Fallback to contact page HTML if none found on homepage
        if not emails and biz["contact_html"]:
            emails = extract_emails(biz["contact_html"])
            source = "Contact Page"

        total_emails += len(emails)
        email_str = ", ".join(emails) if emails else "Not Found"

        print(f"- {biz['name']} ({biz['city']}) -> {email_str}")

        results.append({
            "Business Name": biz["name"],
            "Business Type": biz["business_type"],
            "City": biz["city"],
            "Website": biz["website"],
            "Emails": email_str,
            "Source": source if emails else "-",
        })

    # Build a clean filename based on user inputs
    city_slug = re.sub(r"\W+", "_", city_input) if city_input else "all_cities"
    type_slug = re.sub(r"\W+", "_", type_input) if type_input else "all_types"
    filename = f"leads_{city_slug}_{type_slug}.csv"

    fieldnames = ["Business Name", "Business Type", "City", "Website", "Emails", "Source"]
    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone! Extracted {total_emails} unique email(s) and saved to '{filename}'.")


if __name__ == "__main__":
    run_scraper()