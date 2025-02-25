import camelot
filePathEqualUnequalAngles='equalUnequalAnglesCopy.pdf'

# Extract tables from the PDF
tables = camelot.read_pdf(filePathEqualUnequalAngles, pages='all')

# Print the extracted tables
for i, table in enumerate(tables):
    print(f"Table {i + 1} on page {table.page}:")
    print(table.df)  # This will display the table as a DataFrame

# Optionally, export the tables to CSV
tables[0].to_csv("extracted_table.csv")
