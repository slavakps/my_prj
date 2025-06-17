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
            print(f'\nОперации отфильтрованы по статусу "{status}"\n')
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
    else:
        print("\nОшибка: введен некорректный номер. Пожалуйста, выберите 1, 2 или 3.\n")
        return file_selection()


def choice_sort_by_date(data):
    """Функция для выбора сортировки операций по дате."""
    while True:
        choice_sort = input("Отсортировать операции по дате? (Да/Нет): ").strip().lower()

        if choice_sort == "да":
            while True:
                sort_up_or_lower = input("Отсортировать по возрастанию или по убыванию?: ").strip().lower()
                if sort_up_or_lower in ("убыванию", "возрастанию"):
                    is_reverse = (sort_up_or_lower == "убыванию")
                    return sort_by_date(data, is_reverse)
                else:
                    print("Ошибка: введите 'возрастанию' или 'убыванию'!")

        elif choice_sort == "нет":
            return data

        else:
            print("Ошибка: введите 'Да' или 'Нет'!")


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
    3. Получить информацию о транзакциях из XLSX-файла\n""")
    data = file_selection()
    data = filter_transactions_by_user_input(data)
    data = choice_sort_by_date(data)
    data = sort_by_rub(data)
    sort_by_word = input("Отфильтровать по слову в описании? Да/Нет: ")
    data = filter_transactions_by_description(data, sort_by_word)
    print("Распечатываю итоговый список транзакций...")
    data = end_result(data)
    print(data)


if __name__ == "__main__":
    main()


