import os

# Define more varied and realistic examples for each category
categories = {
    "invoice": [
        "Invoice #12345 for Services Rendered - Amount Due: $150.00",
        "Invoice #98765 for Consulting Services - Amount Due: $350.00",
        "Invoice #11121 for Products Sold - Total Amount: $450.00",
        "Invoice #55432 for Monthly Subscription - Amount Due: $120.00",
        "Invoice #77664 for Services - Total: $200.00",
        "Payment Due for Invoice #22334 - Amount: $99.99",
        "Invoice dated March 2025 - Consulting Fees: $600.00",
        "Invoice for Legal Services Rendered - Due: $1,200.00",
        "Invoice Summary: Graphic Design - $875.00",
        "Invoice #84922 - Website Development - Total: $2,000.00"
    ],
    "bank_statement": [
        "Bank Statement for July 2025 - Account Balance: $2,500.00",
        "Monthly Statement for Account #23456 - Balance: $3,000.00",
        "Bank Statement - Savings Account - Balance: $5,100.00",
        "Transaction Summary for Bank Account #65432 - Current Balance: $1,200.00",
        "Account #11223 Statement - Balance: $4,800.00",
        "Checking Account Statement - Available Balance: $950.00",
        "Summary of Transactions - August 2025 - Balance: $3,400.00",
        "Bank of America - Statement Ending September 2025",
        "Wells Fargo Account Summary - Current Balance: $6,420.00",
        "Statement for Account #77889 - Deposits and Withdrawals Listed"
    ],
    "drivers_license": [
        "Driver's License #AB1234567 - Valid till 2028",
        "Driver's License #CD7654321 - Expires 2027",
        "Driver's License #EF2468135 - Expiration Date: 2029",
        "Driver's License #GH1357924 - Valid until 2026",
        "Driver's License #IJ9876543 - Expires on 2028",
        "British Driving Licence - Valid through 2030",
        "NY State Driver License - Class D - Expires: 2025",
        "California DL #A1234567 - Exp: 04/2029",
        "Texas Driver's License - DL# 87654321 - Valid till 2031",
        "License Type: Full Driving License - Issued in UK - Expires 2032"
    ]
}

output_base_dir = "sample_docs"
os.makedirs(output_base_dir, exist_ok=True)

# Write each text to a .txt file in its category subfolder
for category, texts in categories.items():
    category_dir = os.path.join(output_base_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    for idx, text in enumerate(texts):
        filename = f"{category}_{idx + 1}.txt"
        file_path = os.path.join(category_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

print("Sample documents written to 'sample_docs/<category>/' folders.")
