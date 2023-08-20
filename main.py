"""
Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне.
Додамо функціонал роботи з Birthday у клас Record, а саме функцію days_to_birthday, 
   яка повертає кількість днів до наступного дня народження.
Додамо функціонал перевірки на правильність наведених значень для полів Phone, Birthday.
Додамо пагінацію (посторінковий висновок) для AddressBook для ситуацій, коли книга дуже велика 
   і треба показати вміст частинами, а не все одразу. Реалізуємо це через створення ітератора за записами.
Критерії прийому:
AddressBook реалізує метод iterator, який повертає генератор за записами AddressBook 
   і за одну ітерацію повертає уявлення для N записів.
Клас Record приймає ще один додатковий (опціональний) аргумент класу Birthday
Клас Record реалізує метод days_to_birthday, який повертає кількість днів до наступного дня народження контакту, 
   якщо день народження заданий.
setter та getter логіку для атрибутів value спадкоємців Field.
Перевірку на коректність веденого номера телефону setter для value класу Phone.
Перевірку на коректність веденого дня народження setter для value класу Birthday.
"""

from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.value.isdigit():
            raise ValueError("Invalid phone format. Please use only '0123456789'.")
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.__value.isdigit():
            raise ValueError("Invalid phone format. Please use only '0123456789'.")

    def is_valid_phone(self):
        pass        

class Email(Field):
    def is_valid_email(self):
        pass

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strtime(value, '%d-%m-%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Please use 'DD-MM-YYYY'.")
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value == datetime.strptime(new_value, '%d-%m-%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Please use 'DD-MM-YYYY'.")

class Record:
    def __init__(self, name: str, phones: list, emails: list, birthday: str = None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]
        self.emails = [Email(email) for email in emails]
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None        

    def delete_phone(self, value):
        phone_to_delete = self.find_phone(value)
        if phone_to_delete:
            self.phones.remove(phone_to_delete)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone

    def add_email(self, email):
        email_addr = Email(email)
        if email_addr not in self.emails:
            self.emails.append(email_addr)

    def find_email(self, value):
        for email in self.emails:
            if email.value == value:
                return email
        return None        

    def delete_email(self, value):
        email_to_delete = self.find_email(value)
        if email_to_delete:
            self.pemails.remove(email_to_delete)

    def edit_email(self, old_email, new_email):
        email_to_edit = self.find_email(old_email)
        if email_to_edit:
            email_to_edit.value = new_email

    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        return None             

class AddressBook(UserDict):
    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < len(self.data):
            key = list(self.data.keys())[self._iter_index]    
            value = self.data[key]
            self._iter_index += 1
            return (key, value)
        else:
            raise StopIteration

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)    

def add_handler(address_book, data):
    name = data[0].title()
    phone = data[1]
    email = data[2]
    birthday = data[3]
    record = address_book.find_record(name)
    if record:
        if phone: 
            record.add_phone(phone)
            return f"Phone {phone} was added to contact {name}"
        if email:
            record.add_email(email)
            return f"Email {email} was added to contact {name}"            
    else:
        record = Record(name, [phone], [email], birthday)
        address_book.add_record(record)
        return f"Contact {name} - {birthday} with phone {phone} and email {email} was saved"

def change_handler(address_book, data):
    name = data[0].title()
    phone = data[1]
    email = data[2]
    record = address_book.find_record(name)
    if record:
        if phone: 
            record.edit_phone(phone, phone)
            return f"Phone number for contact {name} was changed to {phone}"
        if email: 
            record.edit_email(email, email)
            return f"Email number for contact {name} was changed to {email}"
    else:
        return "Contact not found"

def phone_handler(address_book, data):
    name = data[0].title()
    record = address_book.find_record(name)
    if record:
        phones = ", ".join([phone.value for phone in record.phones])
        emails = ", ".join([email.value for email in record.emails])
        return f"{name} has phones: {phones} and emails {emails}"
    else:
        return "Contact not found"

def show_all_handler(address_book, *args):
    if not address_book.data:
        return "The address book is empty"
    for name, record in address_book.data.items():
        contacts = "\n".join([f"{name} - {record.birthday}: "                        + \
                                {' '.join([phone.value for phone in record.phones])} + \
                                {' '.join([email.value for email in record.emails])} + \
                            " "])
    return contacts

def hello_handler(address_book, *args):
    return "How can I help you?"

def exit_handler(address_book, *args):
    return "Good bye!"

def command_parser(raw_str: str):  # Парсер команд
    elements = raw_str.split()
    for func, cmd_list in COMMANDS.items():
        for cmd in cmd_list:
            if elements[0].lower() == cmd:
                return func, elements[1:]
    return None, None

COMMANDS = {
    add_handler: ["add"],
    change_handler: ["change"],
    phone_handler: ["phone"],
    show_all_handler: ["show all"],
    exit_handler: ["good bye", "close", "exit"],
    hello_handler: ["hello"]
}

def main():
    address_book = AddressBook()

    while True:
        user_input = input(">>> ")
        if not user_input:
            continue
        func, data = command_parser(user_input)
        if not func:
            print("Unknown command. Type 'hello' for available commands.")
        else:
            result = func(address_book, data)
            print(result)
            if func == exit_handler:
                break

if __name__ == "__main__":
    main()
