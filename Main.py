import pdfplumber
import pandas as pd

filePath='contents.pdf'
filePathEqualUnequalAngles='equalUnequalAnglesCopy.pdf'
filePathEqualAngles='equalAngles.pdf'
 

# Open the specific PDF file
with pdfplumber.open(filePathEqualUnequalAngles) as pdf:
    # Create a list to hold extracted data
    table_data = []

    # Loop through each page in the PDF
    for page_num, page in enumerate(pdf.pages):
        # Extract the table from the current page
        tables = page.extract_table()
        
        if tables:
            print(f"Table from page {page_num + 1}:")
            for row in tables:
                # Clean and filter out rows that are None or empty
                if row and any(row):
                    table_data.append(row)
    
    # Convert the extracted data into a DataFrame for further manipulation
    if table_data:
        df = pd.DataFrame(table_data[1:], columns=table_data[0])  # Use first row as header
        print("\nExtracted DataFrame:")
        print(df)

        # Optionally, export to a CSV or Excel file
        df.to_csv("extracted_steel_data.csv", index=False)
        # df.to_excel("extracted_steel_data.xlsx", index=False)
