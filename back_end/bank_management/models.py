from django.db import models
import secrets

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

    def check_password(self, password):
        return self.password == password
  
    
class Branch(models.Model):
    branchCode = models.AutoField(primary_key=True)
    branchName = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    totalAssets = models.DecimalField(max_digits=12, decimal_places=2)

class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=100)
   # departmentType = models.CharField(max_length=100)
    branchId = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branchCode')
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, db_column='employeeId')

class Employee(models.Model):
    employeeId = models.AutoField(primary_key=True)
    idCard = models.CharField(max_length=18)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hireDate = models.DateField()
    position = models.CharField(max_length=100)
    departmentId = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='departmentId')
    branchId = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branchCode')

class Client(models.Model):
    idNumber = models.CharField(max_length=18, primary_key=True)
    name = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=11)
    address = models.CharField(max_length=200)

class SavingsAccount(models.Model):
    accountId = models.AutoField(primary_key=True)
    password = models.CharField(max_length=100)
    openDate = models.DateField()
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,null=True)
    interestRate = models.DecimalField(max_digits=5, decimal_places=4)
    idNumber = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='idNumber',null=True)
    branchCode = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branchCode',null=True)

    def __str__(self):
        return f'{self.accountId} {self.balance} {self.interestRate} {self.idNumber} {self.branchCode}' 
    
class CreditAccount(models.Model):
    accountId = models.AutoField(primary_key=True)
    password = models.CharField(max_length=100)
    openDate = models.DateField()
    creditBalance = models.DecimalField(max_digits=12, decimal_places=2)
    creditLimit = models.DecimalField(max_digits=12, decimal_places=2)
    lastRepaymentDate = models.DateField()
   # lastUseDate = models.DateField()
    interestRate = models.DecimalField(max_digits=5, decimal_places=4)
    interest = models.DecimalField(max_digits=12, decimal_places=2)
    idNumber = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='idNumber',null=True)
    branchCode = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branchCode',null=True)

class Loan(models.Model):
    LOAN_STATUS = [
        ('NOT_ISSUED', '未发放'),
        ('ISSUED', '已发放'),
        ('PAID_OFF', '已还清'),
        ('OVERDUE', '逾期')
    ]

    loanId = models.AutoField(primary_key=True)
    repaymentAmount = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    interestRate = models.DecimalField(max_digits=5, decimal_places=4)
    loanDate = models.DateField(null=True)
    loanDays = models.IntegerField(null=True)
    loanStatus = models.CharField(max_length=10, choices=LOAN_STATUS, default='NOT_ISSUED')
    branchIssued = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branchCode')
    clientId = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='idCard')

class Repayment(models.Model):
    repaymentId = models.AutoField(primary_key=True)
    repaymentAmount = models.DecimalField(max_digits=12, decimal_places=2)
    repaymentDate = models.DateField()
    loanId = models.ForeignKey(Loan, on_delete=models.CASCADE, db_column='loanId')

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', '存款'),
        ('WITHDRAWAL', '取款'),
        ('TRANSFER', '转账'),
        ('INCOME','收入')
    ]

    transactionId = models.AutoField(primary_key=True)
    transactionDate = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transactionType = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    savingsAccount = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE,db_column='accountId')

    def __str__(self):
        return f'{self.transactionType} of {self.amount} on {self.transactionDate}'
    
class CreditTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('CONSUME', '消费'),
        ('PAYMENT', '还款'),
    ]

    transactionId = models.AutoField(primary_key=True)
    transactionDate = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transactionType = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    creditAccount = models.ForeignKey(CreditAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.transactionType} of {self.amount} on {self.transactionDate}'
