#!/usr/bin/env python3
"""
Personal Finance Tracker
A Python tool to analyze expenses from CSV files and generate HTML reports.
"""

import csv
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict
import argparse 

class FinanceTracker: 
    def __init__(self):
      self.transactions = [] 
      self.categories = defaultdict(float)
      self.monthly_data = defaultdict(lambda: defaultdict(float))

    def load_csv(self, filename):
        """load transactions from CSV file""" 
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                # Try to detect CSV format
                sample = file.read(1024)
                file.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter

                reader = csv.DictReader(file, delimiter=delimiter) 

                for row in reader:
                  # Flexible column mapping
                  transaction = self._parse_transaction(row)
                  if transaction:
                      self.transactions.append(transaction)
              print(f"✅ Loaded {len(self.transactions)} transactions from {filename}")
              return True 

          except FileNotFoundError: 
              print(f"❌ File {filename} not found")
              return False 
          except Exception as e:
              print(f"❌ Error loading CSV: {e}")
              return False 

    
      def _parse_transaction(self, row):
          """Parse a transaction row with flexible column names"""
          # Common column name variations
          date_cols = ['date', 'Date', 'DATE', 'transaction_date', 'Transaction Date']
          amount_cols = ['amount', 'Amount', 'AMOUNT', 'value', 'Value', 'price', 'Price']
          desc_cols = ['description', 'Description', 'DESC', 'desc', 'details', 'Details']
          category_cols = ['category', 'Category', 'CATEGORY', 'type', 'Type']

          # Find the actual column names
          date_col = next((col for col in date_cols if col in row), None)
          amount_col = next((col for col in amount_cols if col in row), None)
          desc_col = next((col for col in desc_cols if col in row), None)
          category_col = next((col for col in category_cols if col in row), None)

          if not date_col or not amount_col:
              return None

          try:
              # Parse date
              date_str = row[date_col].strip()
              date_obj = self._parse_date(date_str) 

              # Parse amount
              amount_str = row[amount_col].strip().replace('$', '').replace(',', '')
              amount = float(amount_str)

              # Get description and category 
              description = row.get(desc_col, 'Unknown').strip() if desc_col else 'Unknown'
              category = row.get(category_col, 'Other').strip() if category_col else 'Other'

              return {
                  'date': date_obj,
                  'amount': amount,
                  'description': description,
                  'category': category
              }

            except (ValueError, TypeError) as e:
               print(f"⚠️ Skipping invalid row: {e}")
               return None
       

  
