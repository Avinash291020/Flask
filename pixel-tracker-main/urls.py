import csv
import urllib.parse

def prepend_tracking_pixel(input_csv_file, output_csv_file, base_url):
    """
    Prepends the base URL to the TRACKING_PIXEL column in a CSV file.

    Args:
        input_csv_file (str): Path to the input CSV file.
        output_csv_file (str): Path to the output CSV file.
        base_url (str): Base URL of your tracking server (e.g., "https://imtocss.pythonanywhere.com").
    """

    rows = []
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email_id = row.get('email_id') # Extract email ID
            tracking_pixel_suffix = row.get('TRACKING_PIXEL')  # Extract existing TRACKING_PIXEL from the CSV
            if email_id and tracking_pixel_suffix:
                # Safely URL-encode the email_id in case it contains special characters
                encoded_email_id = urllib.parse.quote(email_id)

                #Prepend the base url
                tracking_pixel = f"{base_url}{tracking_pixel_suffix}"

                row['TRACKING_PIXEL'] = tracking_pixel
            else:
                print(f"Warning: Missing 'email_id' or 'TRACKING_PIXEL' in row: {row}")
                row['TRACKING_PIXEL'] = ''  # Or some default value
            rows.append(row)

    fieldnames = reader.fieldnames  # No need to add fieldnames; they already exist

    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        writer.writerows(rows)  # Write the data rows

# Example Usage:
input_file = 'emails.csv'       # Replace with your input CSV file name
output_file = 'emails_tracked.csv'  # Replace with your desired output file name
base_url = "https://ozibookflask.pythonanywhere.com/" # Add forward slash to the end for this example

prepend_tracking_pixel(input_file, output_file, base_url)
print(f"Tracking URLs generated and saved to {output_file}")