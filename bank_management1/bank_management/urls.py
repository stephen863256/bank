from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BranchViewSet, DepartmentViewSet, EmployeeViewSet, ClientViewSet, SavingsAccountViewSet, CreditAccountViewSet, LoanViewSet, RepaymentViewSet,login, TransactionViewSet, CreditTransactionViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'savingsaccounts', SavingsAccountViewSet)
router.register(r'creditaccounts', CreditAccountViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'repayments', RepaymentViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'credittransactions', CreditTransactionViewSet)

urlpatterns = [
    path('login', login, name='login'),
    path('', include(router.urls)),
]

