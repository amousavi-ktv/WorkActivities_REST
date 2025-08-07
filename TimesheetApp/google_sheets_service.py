import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from django.conf import settings
import os

class GoogleSheetsService:
    def __init__(self):
        # Path to your service account key file
        self.credentials_file = os.path.join(settings.BASE_DIR, '../Resources/google_credentials.json') 
        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
    def get_client(self):
        credentials = Credentials.from_service_account_file(
            self.credentials_file, scopes=self.scope
        )
        return gspread.authorize(credentials)
    
    def create_or_update_sheet(self, sheet_name, data):
        """
        Create or update a Google Sheet with data
        """
        try:
            client = self.get_client()
            
            # Try to open existing sheet
            try:
                sheet = client.open(sheet_name)
                worksheet = sheet.sheet1
                worksheet.clear()  # Clear existing data
            except gspread.SpreadsheetNotFound:
                # Create new sheet if it doesn't exist
                sheet = client.create(sheet_name)
                worksheet = sheet.sheet1
                
                # Share with your email (replace with your email)
                sheet.share('your-email@gmail.com', perm_type='user', role='writer')
            
            # Convert data to list format for Google Sheets
            if data:
                # Add headers
                headers = list(data[0].keys())
                worksheet.append_row(headers)
                
                # Add data rows
                for row in data:
                    worksheet.append_row(list(row.values()))
            
            return f"Successfully updated sheet: {sheet_name}"
            
        except Exception as e:
            return f"Error: {str(e)}"
