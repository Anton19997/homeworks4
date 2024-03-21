class EmailAlreadyExists(Exception):
    pass


class Employee:
    def __init__(self, name: str, day_salary: int, email: str) -> None:
        self.name = name
        self.day_salary = day_salary
        self.email = self.save_email(email)

    def work(self):
        return 'I come to the office'

    def __str__(self) -> str:
        return f'Employees: {self.name}'

    def __eq__(self, other):
        return self.day_salary == other.day_salary

    def check_salary(self, days):
        today = datetime.date.today()
        month_start = today.replace(day=1)
        work_days = 0

        while month_start <= today:
            if month_start.weekday() < 5:  # Перевірка, чи не є день вихідним
                work_days += 1
            month_start += datetime.timedelta(days=1)

        return work_days * self.day_salary
    
    def save_email(self, email: str) -> str:
        result = self.validate_email(email)
        if result:
            self.email = email
            with open('emails.csv', 'a') as f:
                f.write(email + ' ')
                return self.email
    
    def validate_email(self, email: str) -> None:
        try:
            with open('emails.csv', 'r') as f:
                content = f.read()
                word_array = content.split()
                if email in word_array:
                    raise EmailAlreadyExists
                return True
        except EmailAlreadyExists:
            return False


class Recruiter(Employee):
    def work(self):
        return 'I come to the office and start to hiring'

    def __str__(self) -> str:
        return f'Recruiter: {self.name}'


class Developer(Employee):
    def __init__(self, name, day_salary, tech_stack):
        super().__init__(name, day_salary)
        self.tech_stack = tech_stack

    def __eq__(self, other):
        return len(self.tech_stack) == len(other.tech_stack)

    def work(self):
        return 'I come to the office and start to coding'

    def __str__(self) -> str:
        return f'Developer: {self.name}'

    def __add__(self, other):
        new_name = self.name + ' ' + other.name
        new_tech_stack = list(set(self.tech_stack + other.tech_stack))
        new_salary = max(self.day_salary, other.day_salary)
        return Developer(new_name, new_salary, new_tech_stack)


def compare_salary(employee1, employee2):
    if employee1.day_salary == employee2.day_salary:
        return 'Both employees have the same salary'
    elif employee1.day_salary > employee2.day_salary:
        return f'{employee1.name} has a higher salary'
    else:
        return f'{employee2.name} has a higher salary'


developer1 = Developer("John", 100, ["Python", "JavaScript"], 'john@gmail.com')
developer2 = Developer("Jane", 150, ["Python", "JavaScript", "HTML", "CSS"], 'jane@gmail.com')

new_developer = developer1 + developer2

print(new_developer.name)  # "John Jane"
print(new_developer.tech_stack)  # ["Python", "JavaScript", "HTML", "CSS"]
print(new_developer.day_salary)  # 150, бо це більша зарплата

