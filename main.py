from src.widget import get_date, mask_account_card
from src.processing import sort_by_date, filter_by_state
from src.trans_reader import read_transactions_from_csv, read_transactions_from_excel, filter_transactions_by_description
from src.utils import load_transactions, sort_by_rub


def filter_transactions_by_user_input(transactions):
    """Функция для фильтрации транзакций по статусу"""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nДоступные для фильтрации статусы:", ", ".join(valid_statuses))
        status = input("Введите статус, по которому необходимо выполнить фильтрацию: ").strip().upper()

        if status in valid_statuses:
            filtered = filter_by_state(transactions, status)
            print(f'\nОперации отфильтрованы по статусу "{status}"')
            return filtered
        else:
            print(f'\nСтатус операции "{status}" недоступен.')


def file_selection():
    user_input = input()
    if user_input == "1":
        print("\nДля обработки выбран JSON-файл")
        return load_transactions()
    elif user_input == "2":
        print("\nДля обработки выбран CSV-файл")
        return read_transactions_from_csv()
    elif user_input == "3":
        print("\nДля обработки выбран XLSX-файл")
        return read_transactions_from_excel()
    else: "\nВведен некоректный номер"


def choice_sort_by_date(data):
    choice_sort = input()
    if choice_sort.lower() == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        sort_up_or_lower = input()
        if sort_up_or_lower == 'убыванию':
            is_reverse = True
            data = sort_by_date(data, is_reverse)
        else:
            is_reverse = False
            data = sort_by_date(data, is_reverse)
        return data
    else:
        return data


def end_result(data) -> None:
    if len(data) == 0:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f'\nВсего банковских операций в выборке: {len(data)}\n')

        for transaction in data:
            date = get_date(transaction.get('date'))
            try:
                mask_form = mask_account_card(transaction['from'])
                print(f'\n{date} {transaction["description"]}\n{mask_form}')
            except KeyError:
                print(f'\n{date} {transaction["description"]}')
            except AttributeError:
                print(f"\n{date} {transaction["description"]}\n")


            mask_to = mask_account_card(transaction['to'])
            try:
                amount = transaction['amount']
            except KeyError:
                amount = transaction["operationAmount"]["amount"]
            try:
                currency = transaction["currency_name"]
            except KeyError:
                currency = transaction["operationAmount"]["currency"]["name"]
            print(f'{mask_to}\nСумма: {amount} {currency}')


def main():
    print("""Привет! Добро пожаловать в программу работы с банковскими транзакциями.
    Выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла  """)
    data = file_selection()
    data = filter_transactions_by_user_input(data)
    print("Отсортировать операции по дате? Да/Нет: ")
    data = choice_sort_by_date(data)
    print("Выводить только рублевые транзакции? Да/Нет: ")
    data = sort_by_rub(data)
    print("Отфильтровать по слову в описании? Да/Нет")
    sort_by_word = input()
    data = filter_transactions_by_description(data, sort_by_word)
    print("Распечатываю итоговый список транзакций...")
    data = end_result(data)
    print(data)


if __name__ == "__main__":
    main()


