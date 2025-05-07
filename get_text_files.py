# Let's generate 5 text files for each category: Invoice, Bank Statement, and Driver's License
categories = {
    "invoice": [
        "Invoice #12345 for Services Rendered - Amount Due: $150.00",
        "Invoice #98765 for Consulting Services - Amount Due: $350.00",
        "Invoice #11121 for Products Sold - Total Amount: $450.00",
        "Invoice #55432 for Monthly Subscription - Amount Due: $120.00",
        "Invoice #77664 for Services - Total: $200.00"
    ],
    "bank_statement": [
        "Bank Statement for July 2025 - Account Balance: $2,500.00",
        "Monthly Statement for Account #23456 - Balance: $3,000.00",
        "Bank Statement - Savings Account - Balance: $5,100.00",
        "Transaction Summary for Bank Account #65432 - Current Balance: $1,200.00",
        "Account #11223 Statement - Balance: $4,800.00"
    ],
    "drivers_license": [
        "Driver's License #AB1234567 - Valid till 2028",
        "Driver's License #CD7654321 - Expires 2027",
        "Driver's License #EF2468135 - Expiration Date: 2029",
        "Driver's License #GH1357924 - Valid until 2026",
        "Driver's License #IJ9876543 - Expires on 2028"
    ]
}

# Save each of these examples into text files for training
import os

output_dir = "sample_docs"
os.makedirs(output_dir, exist_ok=True)

# Create files for each category
for category, texts in categories.items():
    for idx, text in enumerate(texts):
        with open(os.path.join(output_dir, f"{category}_{idx+1}.txt"), "w") as file:
            file.write(text)

output_dir  # Return the path to where the files were saved
