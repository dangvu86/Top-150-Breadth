import pandas as pd
import io
import requests

def load_vnindex_data():
    """Load VNINDEX data from Google Sheets"""
    # Google Sheets public URL - export as Excel
    sheet_id = "111j7cIaLE8CrIzy1af-YbTT8ezfrxjzv"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    # Download the file
    response = requests.get(url)
    response.raise_for_status()

    # Read Excel from bytes
    df = pd.read_excel(io.BytesIO(response.content), header=12, skiprows=[13, 14])

    # Keep only needed columns
    df = df[['Ngày', 'Giá đóng cửa', '% Thay đổi']].copy()
    # Remove footer rows (where Ngày is not a valid date)
    df = df[pd.notna(df['Ngày'])]
    df = df[df['Ngày'] != 'Contact']
    # Convert date
    df['Ngày'] = pd.to_datetime(df['Ngày'], errors='coerce')
    # Remove any rows where date conversion failed
    df = df[pd.notna(df['Ngày'])]
    # Sort and reset index
    df = df.sort_values('Ngày').reset_index(drop=True)
    return df

def load_price_volume_data():
    """Load stock price and volume data from Google Drive"""
    # Google Drive public file - direct download URL
    file_id = "15y35qOprQHFP3Q6xXAHLm0APlOcts1tf"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Read CSV directly from URL
    df = pd.read_csv(url)

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Convert Trading Date to datetime
    df['Trading Date'] = pd.to_datetime(df['Trading Date'], format='%m/%d/%Y')

    # Clean numeric columns (remove commas and convert to float)
    numeric_cols = ['Daily Closing Price', 'Matching Volume', 'Matching Value']
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace(',', '').astype(float)

    # Sort by ticker and date
    df = df.sort_values(['TICKER', 'Trading Date']).reset_index(drop=True)
    return df
