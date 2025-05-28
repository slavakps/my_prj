import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from src.trans_reader import read_transactions_from_csv, read_transactions_from_excel


class TestTransactions(unittest.TestCase):
    # Тест для CSV
    @patch('builtins.open', mock_open(read_data="date,amount,category\n2023-01-01,1000,Salary\n2023-01-02,-50,Groceries"))
    def test_read_csv(self):
        result = read_transactions_from_csv()
        self.assertEqual(result, [
            {'date': '2023-01-01', 'amount': '1000', 'category': 'Salary'},
            {'date': '2023-01-02', 'amount': '-50', 'category': 'Groceries'}
        ])

    # Тест для Excel
    @patch('pandas.read_excel')
    def test_read_excel(self, mock_read):
        mock_read.return_value = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'amount': [1000, -50],
            'category': ['Salary', 'Groceries']
        })
        result = read_transactions_from_excel()
        self.assertEqual(result, [
            {'date': '2023-01-01', 'amount': 1000, 'category': 'Salary'},
            {'date': '2023-01-02', 'amount': -50, 'category': 'Groceries'}
        ])

if __name__ == '__main__':
    unittest.main()