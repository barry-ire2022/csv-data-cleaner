# CSV Data Cleaning Tool

This is a simple **Python Streamlit app** that allows you to clean CSV files easily in your browser without installing anything extra.  

It automatically:

- Normalizes dates (column `Date`)  
- Cleans and validates email addresses (column `Email`)  
- Applies sentence case to comments (column `Comment`)  
- Trims whitespace  
- Fills empty cells with `"N/A"`  
- Removes duplicate rows  

---

## Sample CSV Format

Your CSV file should have columns like these:

| Date       | Email                   | Comment           | OtherColumn |
|------------|------------------------|-----------------|-------------|
| 2025-01-15 | john.doe@gmail.com      | great service    | 123         |
| 15-02-2025 | jane.smith@             | excellent product| 456         |
|            |                        |                 |             |

**Notes:**

- `Date` can be in multiple formats (e.g., `YYYY/MM/DD`, `DD-MM-YYYY`)  
- `Email` missing `@` or domain will be corrected (e.g., `user` → `user@example.com`)  
- Empty cells will be replaced with `"N/A"`  
- `Comment` text will be converted to sentence case  

---

## How to Use

1. Click **"Upload CSV file"** in the app.  
2. Preview the **original data**.  
3. The app will show the **cleaned data** instantly.  
4. Download the cleaned CSV using the **Download** button.  

---

## Requirements

- Python 3.9+  
- Streamlit  
- pandas  

Install requirements with:

```bash
pip install -r requirements.txt
