
from src.processing import sort_by_date, filter_by_state
from src.trans_reader import read_transactions_from_csv, read_transactions_from_excel
from src.utils import load_transactions, get_transaction_amount_rub


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


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("\nВведите номер пункта: ").strip()

        try:
            if choice == "1":
                print("\nДля обработки выбран JSON-файл")
                transactions = load_transactions()
                filtered = filter_transactions_by_user_input(transactions)
                user_input_1 = input("Отсортировать операции по дате? Да/Нет: ")
                if user_input_1.lower() == "да":
                    user_input_2 = input("Отсортировать по возрастанию/убыванию?: ")
                    reverse_sort = user_input_2.lower() == "убыванию"
                    filtered_transactions = sort_by_date(filtered, reverse=reverse_sort)
                    user_input_3 = input("Выводить только рублевые транзакции? Да/Нет: ")
                    if user_input_3.lower() == "да":
                        filtered_transactions = get_transaction_amount_rub(transactions)
                        print(filtered_transactions)
                    else: print(filtered_transactions)
                elif user_input_1.lower() == "нет":
                    user_input_2 = input("Отсортировать по возрастанию/убыванию?: ")
                    if user_input_2.lower() == "убыванию":
                        filtered_transactions = sort_by_date(filtered, reverse=reverse_sort)
                        print(filtered_transactions)
                    else:
                        filtered_transactions = sort_by_date(filtered)
                        print(filtered_transactions)
            elif choice == "2":
                print("\nДля обработки выбран CSV-файл")
                transactions = read_transactions_from_csv()
                filtered = filter_transactions_by_user_input(transactions)
                user_input_1 = input("Отсортировать операции по дате? Да/Нет: ")
                if user_input_1.lower() == "да":
                    user_input_2 = input("Отсортировать по возрастанию/убыванию?: ")
                    reverse_sort = user_input_2.lower() == "убыванию"
                    filtered_transactions = sort_by_date(filtered, reverse=reverse_sort)
                    user_input_3 = input("Выводить только рублевые транзакции? Да/Нет: ")
                    if user_input_3.lower() == "да":
                        filtered_transactions = get_transaction_amount_rub(transactions)
                        print(filtered_transactions)
                    else:
                        print(filtered_transactions)
                elif user_input_1.lower() == "нет":
                    user_input_2 = input("Отсортировать по возрастанию/убыванию?: ")
                    if user_input_2.lower() == "убыванию":
                        filtered_transactions = sort_by_date(filtered, reverse=reverse_sort)
                        print(filtered_transactions)
                    else:
                        filtered_transactions = sort_by_date(filtered)
                        print(filtered_transactions)
            elif choice == "3":
                print("\nДля обработки выбран XLSX-файл")
                transactions = read_transactions_from_excel()
                filtered = filter_transactions_by_user_input(transactions)
                user_input_3_1 = input("Отсортировать операции по дате? Да/Нет: ")
                if user_input_3_1.lower() == "да":
                    user_input_3_2 = input("Отсортировать по возрастанию/убыванию?: ")
                    reverse_sort = user_input_3_2.lower() == "убыванию"
                    filtered_transactions = sort_by_date(filtered, reverse=reverse_sort)
                    print(filtered_transactions)
            else:
                print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")
                break
        except FileNotFoundError:
            print("Ошибка: файл не найден. Проверьте наличие файлов в папке data/")
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            break
        break


if __name__ == "__main__":
    main()


