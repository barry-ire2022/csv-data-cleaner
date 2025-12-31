import pandas as pd
import re
import streamlit as st

# ---------- Helper Functions ----------

def sentence_case(text):
    """Convert text to sentence case, fill empty comments with 'N/A'"""
    text = str(text).strip()
    if not text or text.lower() == "nan":
        return "N/A"
    return text[0].upper() + text[1:].lower()


def clean_email(email):
    """Clean and normalize email addresses. Fill empty emails with 'N/A'"""
    email = str(email).strip()
    if not email or email.lower() == "nan":
        return "N/A"

    # Add missing @example.com if no @
    if "@" not in email:
        email += "@example.com"

    # Fix trailing dot before domain
    if email.endswith("."):
        email = email[:-1] + ".com"

    # Fix missing domain suffix if @ exists
    if "@" in email and not re.search(r"\.\w+$", email):
        email += ".com"

    return email


def normalize_date(value):
    """Convert multiple date formats, fill empty or invalid dates with 'N/A'"""
    value = str(value).strip()
    if not value or value.lower() == "nan":
        return "N/A"

    cleaned = re.sub(r"[.\-]", "/", value)

    try:
        dt = pd.to_datetime(cleaned, format="%Y/%m/%d", errors="raise")
    except Exception:
        try:
            dt = pd.to_datetime(cleaned, dayfirst=True, errors="raise")
        except Exception:
            try:
                dt = pd.to_datetime(cleaned, errors="raise")
            except Exception:
                return "N/A"  # default for invalid date

    return dt.strftime("%d %b '%y")


# ---------- Data Cleaning Logic ----------

def clean_data(df):
    # Replace NaN with empty string first
    df = df.fillna("")

    # Strip whitespace for all cells
    df = df.applymap(lambda x: str(x).strip())

    # Normalize dates if column exists
    if "Date" in df.columns:
        df["Date"] = df["Date"].apply(normalize_date)

    # Clean emails if column exists
    if "Email" in df.columns:
        df["Email"] = df["Email"].apply(clean_email)

    # Sentence case comments if column exists
    if "Comment" in df.columns:
        df["Comment"] = df["Comment"].apply(sentence_case)

    # For any other blank cells, replace with "N/A"
    df = df.replace(r'^\s*$', "N/A", regex=True)

    # Remove duplicates
    df = df.drop_duplicates()

    return df


# ---------- Streamlit UI ----------

st.set_page_config(page_title="CSV Data Cleaning Tool", layout="wide")

st.title("CSV Data Cleaning Tool")

st.write(
    "Upload a CSV file to automatically:\n"
    "- Normalize dates (column 'Date')\n"
    "- Clean and validate email addresses (column 'Email')\n"
    "- Apply sentence case to comments (column 'Comment')\n"
    "- Trim whitespace\n"
    "- Remove duplicate rows\n"
    "- Fill all missing or empty cells with 'N/A'"
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, dtype=str)

        st.subheader("Original Data")
        st.dataframe(df, width="stretch")

        cleaned_df = clean_data(df)

        st.subheader("Cleaned Data")
        st.dataframe(cleaned_df, width="stretch")

        csv = cleaned_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")
