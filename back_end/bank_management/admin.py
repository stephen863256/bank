from django.contrib import admin
from .models import User, Branch, Department, Employee, Client, SavingsAccount, CreditAccount, Loan, Repayment, Transaction,CreditTransaction

admin.site.site_header = '银行管理系统'

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password','avatar')
    list_display_links = ('username',)
    list_per_page = 50

class BranchAdmin(admin.ModelAdmin):
    list_display = ('branchCode', 'branchName', 'location', 'totalAssets',)
    list_display_links = ('branchCode',)
    list_per_page = 50

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('departmentId', 'departmentName', 'branchId', 'manager',)
    list_display_links = ('departmentId',)
    list_per_page = 50

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employeeId', 'idCard', 'name', 'gender', 'phoneNumber', 'address', 'salary', 'hireDate', 'position', 'departmentId', 'branchId',)
    list_display_links = ('employeeId',)
    list_per_page = 50

class ClientAdmin(admin.ModelAdmin):
    list_display = ('idNumber', 'name', 'phoneNumber', 'address',)
    list_display_links = ('idNumber',)
    list_per_page = 50

class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ('accountId', 'password', 'openDate', 'balance', 'interestRate','branchCode', 'idNumber',)
    list_display_links = ('accountId',)
    list_per_page = 50

class CreditAccountAdmin(admin.ModelAdmin):
    list_display = ('accountId', 'password', 'openDate', 'creditBalance', 'creditLimit', 'lastRepaymentDate',  'interestRate', 'interest','branchCode', 'idNumber',)
    list_display_links = ('accountId',)
    list_per_page = 50

class LoanAdmin(admin.ModelAdmin):
    list_display = ('loanId', 'repaymentAmount', 'amount', 'interestRate', 'loanDate','loanDays','loanStatus', 'branchIssued', 'clientId',)
    list_display_links = ('loanId',)
    list_per_page = 50

class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('repaymentId', 'repaymentAmount', 'repaymentDate', 'loanId',)
    list_display_links = ('repaymentId',)
    list_per_page = 50

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transactionId', 'transactionDate', 'transactionType', 'amount', 'savingsAccount',)
    list_display_links = ('transactionId',)
    list_per_page = 50

class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('transactionId', 'transactionDate', 'transactionType', 'amount', 'creditAccount',)
    list_display_links = ('transactionId',)
    list_per_page = 50


admin.site.register(User, UserAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(SavingsAccount, SavingsAccountAdmin)
admin.site.register(CreditAccount, CreditAccountAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Repayment, RepaymentAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CreditTransaction, CreditTransactionAdmin)