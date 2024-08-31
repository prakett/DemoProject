import pdfplumber
import pandas as pd

def extract_pdf_to_csv(pdf_path, csv_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []

        # Iterate through each page in the PDF
        for page in pdf.pages:
            # Extract table from the current page
            table = page.extract_table()
            if table:
                all_tables.extend(table)

        # Convert list of tables to a DataFrame
        if all_tables:
            df = pd.DataFrame(all_tables[1:], columns=all_tables[0])  # Assuming the first row contains column names
        else:
            print("No tables found in the PDF.")
            return

        # Save DataFrame to CSV
        df.to_csv(csv_path, index=False)
        print(f"Data extracted and saved to {csv_path}")

# Paths to the PDF and output CSV file
pdf_path = "C:\\Users\\ASUS\\Desktop\\Dass42.pdf"
csv_path = 'path_to_save_csv_file.csv'

# Extract data and save to CSV
extract_pdf_to_csv(pdf_path, csv_path)
