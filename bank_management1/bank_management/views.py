from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import User, Branch, Department, Employee, Client, SavingsAccount, CreditAccount, Loan, Repayment,Transaction,CreditTransaction
from .serializers import UserSerializer, BranchSerializer, DepartmentSerializer, EmployeeSerializer, ClientSerializer, SavingsAccountSerializer, CreditAccountSerializer, LoanSerializer, RepaymentSerializer, TransactionSerializer, CreditTransactionSerializer
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
import jwt
from django.conf import settings
import json
from django.core.paginator import Paginator
import datetime
from decimal import Decimal
from datetime import datetime
import os
def authenticate(request, username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
        else:
            return None
    except User.DoesNotExist:
        return None

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 登录成功，生成 token 并返回成功的响应
            payload = {
                'id': user.id,
                'username': user.username,
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            print(token)
            avatar_url = request.build_absolute_uri(user.avatar.url)
            print(settings.MEDIA_ROOT)
            print(avatar_url)
            return JsonResponse({'message': 'Login successful', 'token': token, 'avatar': avatar_url})
        else:
            # 登录失败，返回失败的响应
            return JsonResponse({'message': 'Login failed','code':'401'}, status=401)
    else:
        # 不正确的请求方法，返回错误的响应
        return JsonResponse({'message': 'Invalid request method','code':'405'}, status=405)

def validate_id_card(id_card):
    if len(id_card) != 18:
        return False
    if not id_card[0:17].isdigit():
        return False
    if not id_card[17].isdigit() and id_card[17] != 'X':
        return False
    # 加权因子
    weight_factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码映射
    check_code_dict = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
    # 计算校验位
    sum = 0
    for i in range(0, len(id_card) - 1):
        sum += int(id_card[i]) * weight_factor[i]
    # 比较校验位
    return check_code_dict[sum % 11] == id_card[-1].upper()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    from django.core.paginator import Paginator

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'username' in search_form:
            if search_form['username'] == '':
                user = User.objects.all().order_by('id')
            else:
                username = search_form['username']
                user = User.objects.filter(username=username)
        #else:
         #   user = User.objects.all()
        if user is None:
            return JsonResponse({'code': 400, 'message': 'User not found'})
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(user, size)

        # 获取当前页的数据
        user_page = paginator.get_page(page)

        serializer = UserSerializer(user_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})

    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def edit(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'User not found'})

        user.password = data['password']
        user.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            username = data['username']
            password = data['password']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})

        if(User.objects.filter(username=username).exists()):
            return JsonResponse({'code': 400, 'message': 'User already exists'})

        user = User(username=username, password=password)
        user.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['delete'])
    @transaction.atomic
    def delete(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        user = User.objects.get(username=data['username'])
        user.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def avatar(self, request):
        token = request.META.get('HTTP_TOKEN')
        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})
        data = request.data

        try:
            username = data['username']
            avatar_file = request.FILES.get('file')
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})
        

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'User not found'})

        # 检查用户当前的头像是否是默认头像
        if user.avatar.name != 'avatars/default.png':
            # 如果不是默认头像，删除旧的头像文件
            old_avatar_path = os.path.join(settings.MEDIA_ROOT, user.avatar.name)
            if os.path.isfile(old_avatar_path):
                os.remove(old_avatar_path)

        user.avatar.save(avatar_file.name, avatar_file)
        user.save()
        avatar_url = request.build_absolute_uri(user.avatar.url)
        return JsonResponse({'code': 200, 'message': 'success', 'avatar': avatar_url})        

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'branchName' in search_form:
            if search_form['branchName'] == '':
                branch = Branch.objects.all()
            else:
                branchName = search_form['branchName']
                branch = Branch.objects.filter(branchName=branchName)
        #else:
         #   branch = Branch.objects.all()
        if branch is None:
            return JsonResponse({'code': 400, 'message': 'Branch not found'})
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(branch, size)

        # 获取当前页的数据
        branch_page = paginator.get_page(page)

        serializer = BranchSerializer(branch_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})
    

    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def edit(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data

        
        try:
            branch = Branch.objects.get(branchCode = data['branchCode'])
        except Branch.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Branch not found'})

        if data['branchName'] != branch.branchName:
            branch.branchName = data['branchName']
        if data['location'] != branch.location:
            branch.location = data['location']
        if data['totalAssets'] != branch.totalAssets:
            branch.totalAssets = data['totalAssets']
        branch.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            branchName = data['branchName']
            location = data['location']
            totalAssets = data['totalAssets']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})

        if(Branch.objects.filter(branchName=branchName).exists()):
            return JsonResponse({'code': 400, 'message': 'Branch already exists'})

        branch = Branch(branchName=branchName, location=location, totalAssets=totalAssets)
        branch.save()
        return JsonResponse({'code': 200, 'message': 'success'})

    @csrf_exempt
    @action(detail=False, methods=['delete'])
    @transaction.atomic
    def delete(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            branchName = data['branchName']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})

        try:
            branch = Branch.objects.get(branchName=branchName)
        except Branch.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Branch not found'})

        branch.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'branchId' in search_form:
            if search_form['branchId'] == '':
                department = Department.objects.all()
            else:
                branchId = search_form['branchId']
                branch = Branch.objects.get(branchCode=branchId)
                department = Department.objects.filter(branchId=branch)
        #else:
         #   department = Department.objects.all()
        if department is None:
            return JsonResponse({'code': 400, 'message': 'Department not found'})
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(department, size)

        # 获取当前页的数据
        department_page = paginator.get_page(page)

        serializer = DepartmentSerializer(department_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def edit(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            departmentId = data['departmentId']
            departmentName = data['departmentName']
            branchId = data['branchId']
            manager = data['manager']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})

        try:
            department = Department.objects.get(departmentId=departmentId)
        except Department.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Department not found'})

        if departmentName != department.departmentName:
            department.departmentName = departmentName

        if branchId != department.branchId.branchCode:
            try:
                branch = Branch.objects.get(branchCode=branchId)
            except Branch.DoesNotExist:
                return JsonResponse({'code': 404, 'message': 'Branch not found'})
            department.branchId = branch
        
        #print(department.manager.employeeId)
        if department.manager == None or manager != department.manager.employeeId  :
            try:
                manager = Employee.objects.get(employeeId=manager)
            except Employee.DoesNotExist:
                return JsonResponse({'code': 404, 'message': 'Employee not found'})
            
            if manager.position == 'Manager':
                return JsonResponse({'code': 400, 'message': 'No two departments can have the same manager'})
            
            if department.manager != None:
                department.manager.salary = department.manager.salary - 3000
                department.manager.position = 'Employee'
                department.manager.save()

            department.manager = manager
            manager.departmentId = department
            manager.salary = manager.salary + 3000
            manager.position = 'Manager'
            manager.save()

        department.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            departmentId = data['departmentId']
            departmentName = data['departmentName']
            branchId = data['branchId']
            managerId = data['manager']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})

        if Department.objects.filter(departmentId=departmentId).exists():
            return JsonResponse({'code': 400, 'message': 'Department already exists'})

        try:
            branch = Branch.objects.get(branchCode=branchId)
        except Branch.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Branch not found'})

        if(managerId == ''):
            manager = None
        else:
            try:
                manager = Employee.objects.get(employeeId=managerId)
            except Employee.DoesNotExist:
                return JsonResponse({'code': 404, 'message': 'Employee not found'})

        if manager != None:
            manager.position = 'Manager'
            manager.departmentId = department
            manager.salary = manager.salary + 3000
            manager.save()

        department = Department(departmentId=departmentId, departmentName=departmentName, branchId=branch, manager=manager)
        department.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    

    @csrf_exempt
    @action(detail=False, methods=['delete'])
    @transaction.atomic
    def delete(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            departmentId = data['departmentId']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})

        try:
            department = Department.objects.get(departmentId=departmentId)
        except Department.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Department not found'})

        employees = Employee.objects.filter(departmentId=department)
        if employees.exists():
            return JsonResponse({'code': 400, 'message': 'Department has employees'})

        department.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'employeeId' in search_form:
            if search_form['employeeId'] == '':
                employee = Employee.objects.all()
            else:
                employeeId = search_form['employeeId']
                employee = Employee.objects.filter(employeeId=employeeId)
        #else:
         #   employee = Employee.objects.all()
        if employee is None:
            return JsonResponse({'code': 400, 'message': 'Employee not found'})
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(employee, size)

        # 获取当前页的数据
        employee_page = paginator.get_page(page)

        serializer = EmployeeSerializer(employee_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})


    @csrf_exempt
    @action(detail=False, methods=['put'])
    def edit(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        employee = Employee.objects.get(employeeId=data['employeeId'])

        if data['name'] != employee.name:
            with transaction.atomic():
                employee.name = data['name']
                employee.save()

        if data['phoneNumber'] != employee.phoneNumber:
            with transaction.atomic():
                if len(data['phoneNumber']) != 11:
                    return JsonResponse({'code': 400, 'message': 'Phone number length must be 11'})
                if data['phoneNumber'][0] != '1':
                    return JsonResponse({'code': 400, 'message': 'Phone number must start with 1'})
                if not data['phoneNumber'][1:].isdigit():
                    return JsonResponse({'code': 400, 'message': 'Phone number must contain only digits after the first character'})
                if data['phoneNumber'][1] not in ['3', '4', '5', '7', '8']:
                    return JsonResponse({'code': 400, 'message': 'The second digit of the phone number must be 3, 4, 5, 7, or 8'})
                employee.phoneNumber = data['phoneNumber']
                employee.save()

        if data['address'] != employee.address:
            with transaction.atomic():
                employee.address = data['address']
                employee.save()

        if data['salary'] != employee.salary:
            with transaction.atomic():
                if Decimal(data['salary']) < 0:
                    return JsonResponse({'code': 400, 'message': 'Wrong Salary'})
                if Decimal(data['salary']) - employee.salary > 3000 or Decimal(data['salary']) - employee.salary < -3000:
                    return JsonResponse({'code': 400, 'message': 'Salary increase must be less than 3000 and salary decrease must be less than 3000'})
                employee.salary = float(data['salary'])
                employee.save()

        if data['departmentId'] != employee.departmentId.departmentId:
            with transaction.atomic():
                department = Department.objects.get(departmentId=data['departmentId'])
                if department == None:
                    return JsonResponse({'code': 400, 'message': 'Department not found'})
                pre_department = Department.objects.get(departmentId=employee.departmentId.departmentId)
                
                if pre_department.manager == employee:
                    return JsonResponse({'code': 400, 'message': 'Manager cannot be changed'})

                employee.departmentId = department
                branch = Branch.objects.get(branchCode=department.branchId.branchCode)

                
                if data['branchId'] != branch.branchCode:
                    employee.branchId = branch
                employee.save()

        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def add(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data

        with transaction.atomic():
            if not validate_id_card(data['idCard']):
                return JsonResponse({'code': 400, 'message': 'Wrong ID Card'})
            if Employee.objects.filter(idCard=data['idCard']).exists():
                return JsonResponse({'code': 400, 'message': 'Employee already exists'})
            if data['gender'] not in ['Male','Female']:
                return JsonResponse({'code': 400, 'message': 'Wrong Gender'})

            if len(data['phoneNumber']) != 11:
                return JsonResponse({'code': 400, 'message': 'Phone number length must be 11'})

            if data['phoneNumber'][0] != '1':
                return JsonResponse({'code': 400, 'message': 'Phone number must start with 1'})

            if not data['phoneNumber'][1:].isdigit():
                return JsonResponse({'code': 400, 'message': 'Phone number must contain only digits after the first character'})

            if data['phoneNumber'][1] not in ['3', '4', '5', '7', '8']:
                return JsonResponse({'code': 400, 'message': 'The second digit of the phone number must be 3, 4, 5, 7, or 8'})

            if(not data['salary'].isdigit() or float(data['salary']) < 0):
                return JsonResponse({'code': 400, 'message': 'Wrong Salary'})

            if(data['position'] not in ['Manager','Employee']):
                return JsonResponse({'code': 400, 'message': 'Wrong Position'})

            department = Department.objects.get(departmentId=data['departmentId'])
            if department == None:
                return JsonResponse({'code': 400, 'message': 'Department not found'})

            branch = Branch.objects.get(branchCode=department.branchId.branchCode)

            hireDate = datetime.strptime(data['hireDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
            employee = Employee(idCard=data['idCard'], name=data['name'], gender = data['gender'], phoneNumber=data['phoneNumber'], address=data['address'], salary=data['salary'], hireDate=hireDate, position=data['position'], departmentId=department, branchId=branch)   
            employee.save() 

        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['delete'])
    @transaction.atomic
    def delete(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            employee = Employee.objects.get(employeeId=data['employeeId'])
        except Employee.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Employee not found'})

        if employee.position == 'Manager':
            department = Department.objects.get(manager=employee)
            department.manager = None
            department.save()

        employee.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'idNumber' in search_form:
            if search_form['idNumber'] == '':
                client = Client.objects.all()
            else:
                idNumber = search_form['idNumber']
                if not validate_id_card(idNumber):
                    return JsonResponse({'code': 400, 'message': 'Wrong ID Card'})
                client = Client.objects.filter(idNumber=idNumber)
        #else:
         #   client = Client.objects.all()
        if client is None:
            return JsonResponse({'code': 400, 'message': 'Client not found'})
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(client, size)

        # 获取当前页的数据
        client_page = paginator.get_page(page)

        serializer = ClientSerializer(client_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def edit(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            client = Client.objects.get(idNumber=data['idNumber'])
        except Client.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Client not found'})
        
        if(data['name'] != client.name):
            with transaction.atomic():
                client.name = data['name']
                client.save()

        if(data['phoneNumber'] != client.phoneNumber):
            with transaction.atomic():
                if len(data['phoneNumber']) != 11:
                    return JsonResponse({'code': 400, 'message': 'Phone number length must be 11'})
                if data['phoneNumber'][0] != '1':
                    return JsonResponse({'code': 400, 'message': 'Phone number must start with 1'})
                if not data['phoneNumber'][1:].isdigit():
                    return JsonResponse({'code': 400, 'message': 'Phone number must contain only digits after the first character'})
                if data['phoneNumber'][1] not in ['3', '4', '5', '7', '8']:
                    return JsonResponse({'code': 400, 'message': 'The second digit of the phone number must be 3, 4, 5, 7, or 8'})
                client.phoneNumber = data['phoneNumber']
                client.save()

        if(data['address'] != client.address):
            with transaction.atomic():
                client.address = data['address']
                client.save()
        #client.name = data['name']
        #client.phoneNumber = data['phoneNumber']
        #client.address = data['address']
        client.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            idNumber = data['idNumber']
            name = data['name']
            phoneNumber = data['phoneNumber']
            address = data['address']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})

        if(Client.objects.filter(idNumber=idNumber).exists()):
            return JsonResponse({'code': 400, 'message': 'Client already exists'})
        if not validate_id_card(idNumber):
            return JsonResponse({'code': 400, 'message': 'Wrong ID Card'})
        if Client.objects.filter(idNumber=idNumber).exists():
            return JsonResponse({'code': 400, 'message': 'Client already exists'})
        if len(phoneNumber) != 11:
            return JsonResponse({'code': 400, 'message': 'Phone number length must be 11'})
        if phoneNumber[0] != '1':
            return JsonResponse({'code': 400, 'message': 'Phone number must start with 1'})
        if not phoneNumber[1:].isdigit():
            return JsonResponse({'code': 400, 'message': 'Phone number must contain only digits after the first character'})
        if phoneNumber[1] not in ['3', '4', '5', '7', '8']:
            return JsonResponse({'code': 400, 'message': 'The second digit of the phone number must be 3, 4, 5, 7, or 8'})
        
        client = Client(idNumber=idNumber, name=name, phoneNumber=phoneNumber, address=address)
        client.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['delete'])
    @transaction.atomic
    def delete(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try :
            client = Client.objects.get(idNumber=data['idNumber'])
        except Client.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Client not found'})
        #client = Client.objects.get(idNumber=data['idNumber'])
        client.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    
class SavingsAccountViewSet(viewsets.ModelViewSet):
    queryset = SavingsAccount.objects.all()
    serializer_class = SavingsAccountSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'accountId' in search_form:
            if search_form['accountId'] == '':
                savingsAccount = SavingsAccount.objects.all()
            else:
                accountId = search_form['accountId']
                savingsAccount = SavingsAccount.objects.filter(accountId=accountId)

        if savingsAccount is None:
            return JsonResponse({'code': 400, 'message': 'SavingsAccount not found'})
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(savingsAccount, size)

        # 获取当前页的数据
        savingsAccount_page = paginator.get_page(page)

        serializer = SavingsAccountSerializer(savingsAccount_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})

    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def edit(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            savingsAccount = SavingsAccount.objects.get(accountId=data['accountId'])
        except SavingsAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'SavingsAccount not found'})

        if len(data['password']) != 6:
            return JsonResponse({'code': 400, 'message': 'Password length must be 6'})
        if not data['password'].isdigit():
            return JsonResponse({'code': 400, 'message': 'Password must contain only digits'})

        if(data['password'] != savingsAccount.password):
            with transaction.atomic():
                savingsAccount.password = data['password']
                savingsAccount.save()

        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            branchCode = data['branchCode']
            idNumber = data['idNumber']
            password = data['password']
            openingDate = datetime.strptime(data['openingDate'],  '%Y-%m-%dT%H:%M:%S.%fZ')
           # openingDate = openingDate.date()
            balance = Decimal(data['balance'])
            interestRate = Decimal(data['interestRate'])
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})
        
       # if SavingsAccount.objects.filter(idNumber=idNumber).exists():
        #    return JsonResponse({'code': 400, 'message': 'SavingsAccount already exists'})
        if len(password) != 6:
            return JsonResponse({'code': 400, 'message': 'Password length must be 6'})
        
        if not validate_id_card(idNumber):
            return JsonResponse({'code': 400, 'message': 'Wrong ID Card'})
        
        try:
            client = Client.objects.get(idNumber=idNumber)
        except Client.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Client not found'})
        
        try:
            branch = Branch.objects.get(branchCode=branchCode)
        except Branch.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Branch not found'})
        
        days = (datetime.now() - openingDate).days  # 时间，以天为单位
        interest = balance * (1 + interestRate) ** days - balance
        interest = Decimal(interest)
        balance += interest
        savingsAccount = SavingsAccount(branchCode=branch, idNumber=client, password=password, openDate=openingDate, balance=balance, interestRate=interestRate)
        savingsAccount.save()

        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['delete'])
    @transaction.atomic
    def delete(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            savingsAccount = SavingsAccount.objects.get(accountId=data['accountId'])
        except SavingsAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'SavingsAccount not found'})
        
        if savingsAccount.balance != 0:
            return JsonResponse({'code': 400, 'message': 'Balance must be 0'})
        
        savingsAccount.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def deposit(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            savingsAccount = SavingsAccount.objects.get(accountId=data['accountId'])
        except SavingsAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'SavingsAccount not found'})
        
        if Decimal(data['amount']) <= 0:
            return JsonResponse({'code': 400, 'message': 'Amount must be greater than 0'})
        
       # savingsAccount.balance += Decimal(data['amount'])
       # savingsAccount.save()
        transaction = Transaction(savingsAccount=savingsAccount,
                                 # transactionDate=data['transactionDate'],
                                  transactionType='DEPOSIT', 
                                  amount=Decimal(data['amount']))
        transaction.save()
        #savingsAccount.lastTransaction = transaction
       # savingsAccount.save()
        return JsonResponse({'code': 200, 'message': 'success'})       
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def withdraw(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            savingsAccount = SavingsAccount.objects.get(accountId=data['accountId'])
        except SavingsAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'SavingsAccount not found'})
        
        if Decimal(data['amount']) <= 0:
            return JsonResponse({'code': 400, 'message': 'Amount must be greater than 0'})
        
        print(savingsAccount.balance)
        if Decimal(data['amount']) > savingsAccount.balance:
            return JsonResponse({'code': 400, 'message': 'Insufficient balance'})
        
        print(savingsAccount)
        transaction = Transaction(savingsAccount=savingsAccount,
                                  #transactionDate=data['transactionDate'],
                                  transactionType='WITHDRAWAL', 
                                  amount=Decimal(data['amount']))
        transaction.save()

        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def transfer(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            savingsAccount = SavingsAccount.objects.get(accountId=data['accountId'])
        except SavingsAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'SavingsAccount not found'})
        
        if Decimal(data['amount']) <= 0:
            return JsonResponse({'code': 400, 'message': 'Amount must be greater than 0'})
        
        if Decimal(data['amount']) > savingsAccount.balance:
            return JsonResponse({'code': 400, 'message': 'Insufficient balance'})
        
        try:
            targetSavingsAccount = SavingsAccount.objects.get(accountId=data['targetAccountId'])
        except SavingsAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Target SavingsAccount not found'})
        
       # savingsAccount.balance -= Decimal(data['amount'])
       # savingsAccount.save()
        
        #targetSavingsAccount.balance += Decimal(data['amount'])
       # targetSavingsAccount.save()

        transaction = Transaction(savingsAccount=savingsAccount,transactionDate=data['transactionDate'], transactionType='Transfer', amount=data['amount'])
        transaction.save()
       # savingsAccount.lastTransaction = transaction
       # savingsAccount.save()

        transaction = Transaction(savingsAccount=targetSavingsAccount,transactionDate=data['transactionDate'], transactionType='Income', amount=data['amount'])
        transaction.save()
      #  targetSavingsAccount.lastTransaction = transaction
      #  targetSavingsAccount.save()

        print("success")
        return JsonResponse({'code': 200, 'message': 'success'})
    
class CreditAccountViewSet(viewsets.ModelViewSet):
    queryset = CreditAccount.objects.all()
    serializer_class = CreditAccountSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'accountId' in search_form:
            if search_form['accountId'] == '':
                creditAccount = CreditAccount.objects.all()
            else:
                accountId = search_form['accountId']
                creditAccount = CreditAccount.objects.filter(accountId=accountId)

        if creditAccount is None:
            return JsonResponse({'code': 400, 'message': 'CreditAccount not found'})
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(creditAccount, size)

        # 获取当前页的数据
        creditAccount_page = paginator.get_page(page)

        serializer = CreditAccountSerializer(creditAccount_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    @transaction.atomic
    def edit(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            creditAccount = CreditAccount.objects.get(accountId=data['accountId'])
        except CreditAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'CreditAccount not found'})

        if(data['password'] != creditAccount.password):
            with transaction.atomic():
                creditAccount.password = data['password']
                creditAccount.save()

        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            branchCode = data['branchCode']
            idNumber = data['idNumber']
            password = data['password']
            openingDate = datetime.strptime(data['openingDate'],  '%Y-%m-%dT%H:%M:%S.%fZ')
            #balance = Decimal(data['balance'])
            creditLimit = Decimal(data['creditLimit'])
            interestRate = Decimal(data['interestRate'])
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})
        
        if len(password) != 6:
            return JsonResponse({'code': 400, 'message': 'Password length must be 6'})
        
        if not validate_id_card(idNumber):
            return JsonResponse({'code': 400, 'message': 'Wrong ID Card'})
        
        try:
            client = Client.objects.get(idNumber=idNumber)
        except Client.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Client not found'})
        
        try:
            branch = Branch.objects.get(branchCode=branchCode)
        except Branch.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Branch not found'})
        # 将日期的日部分替换为10
        next_month_date = openingDate.replace(day=10)

        # 如果新的日期在开户日期之前或等于开户日期，那么将月份加1
        if next_month_date <= openingDate:
            # 如果当前月份是12月，那么将年份加1，月份变为1月
            if next_month_date.month == 12:
                next_month_date = next_month_date.replace(year=next_month_date.year + 1, month=1)
            else:
                next_month_date = next_month_date.replace(month=next_month_date.month + 1)

        lastRepaymentDate = next_month_date

        creditAccount = CreditAccount(branchCode=branch, idNumber=client, password=password, openDate=openingDate, interest =Decimal(0),lastRepaymentDate=lastRepaymentDate,creditBalance=creditLimit, creditLimit=creditLimit, interestRate=interestRate)
        creditAccount.save()

        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['delete'])
    @transaction.atomic
    def delete(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            creditAccount = CreditAccount.objects.get(accountId=data['accountId'])
        except CreditAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'CreditAccount not found'})
        
        if creditAccount.creditBalance != creditAccount.creditLimit:
            return JsonResponse({'code': 400, 'message': 'Must repay before closing account'})
        
        creditAccount.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    def repay(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            creditAccount = CreditAccount.objects.get(accountId=data['accountId'])
        except CreditAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'CreditAccount not found'})
        
        if Decimal(data['amount']) <= 0:
            return JsonResponse({'code': 400, 'message': 'Amount must be greater than 0'})
        
        if Decimal(data['amount']) + creditAccount.creditBalance  > creditAccount.creditLimit + creditAccount.interest:
            return JsonResponse({'code': 400, 'message': 'Exceed credit limit'})
        
        if creditAccount.creditBalance + Decimal(data['amount']) <= creditAccount.creditLimit:
            creditAccount.creditBalance += Decimal(data['amount'])
        else:
            creditAccount.interest -= creditAccount.creditBalance + Decimal(data['amount']) - creditAccount.creditLimit
            creditAccount.creditBalance = creditAccount.creditLimit
        
        if creditAccount.creditBalance == creditAccount.creditLimit and creditAccount.interest == 0:
            creditAccount.lastRepaymentDate = datetime.now()
            
        creditAccount.save()
        
        CreditTransaction.objects.create(creditAccount=creditAccount, transactionType='REPAYMENT', amount=Decimal(data['amount']),transactionDate=data['repaymentDate'])
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    def consume(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        data = request.data
        try:
            creditAccount = CreditAccount.objects.get(accountId=data['accountId'])
        except CreditAccount.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'CreditAccount not found'})
        
        if Decimal(data['amount']) <= 0:
            return JsonResponse({'code': 400, 'message': 'Amount must be greater than 0'})
        
        if creditAccount.interest > 0:
            return JsonResponse({'code': 400, 'message': 'Must repay before consuming'})

        if Decimal(data['amount']) > creditAccount.creditBalance:
            return JsonResponse({'code': 400, 'message': 'Exceed credit limit'})

        if creditAccount.creditBalance == creditAccount.creditLimit and creditAccount.interest == 0:
            creditAccount.lastRepaymentDate = datetime.now()
            
        creditAccount.creditBalance -= Decimal(data['amount'])
        creditAccount.save()

        CreditTransaction.objects.create(creditAccount=creditAccount, transactionType='CONSUME', amount=Decimal(data['amount']),transactionDate=data['useDate'])
        return JsonResponse({'code': 200, 'message': 'success'})

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'idNumber' in search_form:
            if search_form['idNumber'] == '':
                loan = Loan.objects.all()
            else:
                idNumber = search_form['idNumber']
                client = Client.objects.get(idNumber=idNumber)
                loan = Loan.objects.filter(client=client)
        
        if loan is None:
            return JsonResponse({'code': 400, 'message': 'Loan not found'})
        
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(loan, size)

        # 获取当前页的数据
        loan_page = paginator.get_page(page)
        serializer = LoanSerializer(loan_page, many=True)

        data = {
            'data': serializer.data,
            'count': paginator.count
        }

        return Response({'code': 200, 'message': 'success', 'data': data})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add(self, request):
        token = request.META.get('HTTP_TOKEN')
        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})
        data = request.data
        try:
            idNumber = data['idNumber']
            amount = Decimal(data['amount'])
            interestRate = Decimal(data['interestRate'])
            loanDays = data['loanDays']
           #loanStatus = data['loanStatus']
            branchCode = data['branchIssued']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})
        
        if amount <= 0:
            return JsonResponse({'code': 400, 'message': 'Amount must be greater than 0'})
        
        if interestRate <= 0:
            return JsonResponse({'code': 400, 'message': 'Interest rate must be greater than 0'})
        
        if not validate_id_card(idNumber):
            return JsonResponse({'code': 400, 'message': 'Wrong ID Card'})
        
        if not loanDays.isdigit() or int(loanDays) <= 0:
            return JsonResponse({'code': 400, 'message': 'Wrong loan days'})
        
        try:
            client = Client.objects.get(idNumber=idNumber)
        except Client.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Client not found'})
        
        try:
            branch = Branch.objects.get(branchCode=branchCode)
        except Branch.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Branch not found'})
        
        interest = amount * interestRate * Decimal(loanDays) 

        loan = Loan(clientId=client, repaymentAmount=Decimal(0),interest=interest,amount=amount,loanDays=loanDays,interestRate=interestRate, loanStatus='NOT_ISSUED', branchIssued=branch)
        loan.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def updatestatus(self, request):
        token = request.META.get('HTTP_TOKEN')
        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})
        data = request.data
        try:
            loan = Loan.objects.get(loanId=data['loanId'])
        except Loan.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Loan not found'})
        
        try:
            loanId = data['loanId']
            newStatus = data['newStatus']
            loanDate = data['loanDate']
        except KeyError:
            return JsonResponse({'code': 400, 'message': 'Missing data'})
        
        try:
            loan = Loan.objects.get(loanId=loanId)
        except Loan.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Loan not found'})

        if loan.loanStatus != 'NOT_ISSUED':
            return JsonResponse({'code': 400, 'message': 'Loan has been issued'})
        
        loanDate = datetime.strptime(loanDate,  '%Y-%m-%dT%H:%M:%S.%fZ')
        loan.loanStatus = newStatus
        loan.loanDate = loanDate.date()
        loan.save()

        return JsonResponse({'code': 200, 'message': 'success'})
    
    @csrf_exempt
    @action(detail=False, methods=['put'])
    def repay(self, request):
        token = request.META.get('HTTP_TOKEN')
        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})
        
        data = request.data

        try:
            loan = Loan.objects.get(loanId=data['loanId'])
        except Loan.DoesNotExist:
            return JsonResponse({'code': 404, 'message': 'Loan not found'})
        
        if(loan.loanStatus == 'PAID_OFF'):
            return JsonResponse({'code': 400, 'message': 'Loan has been paid off'})
        
        if(loan.loanStatus == 'NOT_ISSUED'):
            return JsonResponse({'code': 400, 'message': 'Loan has not been issued'})
        
        if Decimal(data['amount']) <= 0:
            return JsonResponse({'code': 400, 'message': 'Amount must be greater than 0'})
        
        if Decimal(data['amount']) > loan.amount - loan.repaymentAmount + loan.interest:
            return JsonResponse({'code': 400, 'message': 'Exceed repayment amount'})
        
        loan.repaymentAmount += Decimal(data['amount'])
        if(loan.repaymentAmount == loan.amount + loan.interest):
            loan.loanStatus = 'PAID_OFF'
        loan.save()
        repaymentDate = datetime.strptime(data['repaymentDate'],  '%Y-%m-%dT%H:%M:%S.%fZ').date()
        repayment = Repayment(loanId=loan, repaymentAmount=Decimal(data['amount']), repaymentDate=repaymentDate)
        repayment.save()

        return JsonResponse({'code': 200, 'message': 'success'})
    

class RepaymentViewSet(viewsets.ModelViewSet):
    queryset = Repayment.objects.all()
    serializer_class = RepaymentSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})
        search_form = request.data
        if 'idNumber' in search_form:
            if search_form['idNumber'] == '':
                repayment = Repayment.objects.all()
            else:
                loan = Loan.objects.get(loanId=search_form['loanId'])
                repayment = Repayment.objects.filter(loanId=loan)
        if repayment is None:
            return JsonResponse({'code': 400, 'message': 'Repayment not found'})
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)
        # 创建 Paginator 对象
        paginator = Paginator(repayment, size)
        # 获取当前页的数据
        repayment_page = paginator.get_page(page)
        serializer = RepaymentSerializer(repayment_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }

        return Response({'code': 200, 'message': 'success', 'data': data})
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'savingsAccount' in search_form:
            if search_form['savingsAccount'] == '':
                transaction = Transaction.objects.all()
            else:
                savingsAccount = SavingsAccount.objects.get(accountId=search_form['savingsAccount'])
                transaction = Transaction.objects.filter(savingsAccount=savingsAccount)

        if transaction is None:
            return JsonResponse({'code': 400, 'message': 'Transaction not found'})
        
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(transaction, size)
        # 获取当前页的数据
        transaction_page = paginator.get_page(page)
        serializer = TransactionSerializer(transaction_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})
    
class CreditTransactionViewSet(viewsets.ModelViewSet):
    queryset = CreditTransaction.objects.all()
    serializer_class = CreditTransactionSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        try:
            pay_load = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'message': 'Token expired'})

        search_form = request.data
        if 'creditAccount' in search_form:
            if search_form['creditAccount'] == '':
                creditTransaction = CreditTransaction.objects.all()
            else:
                creditAccount = CreditAccount.objects.get(accountId=search_form['creditAccount'])
                creditTransaction = CreditTransaction.objects.filter(creditAccount=creditAccount)

        if creditTransaction is None:
            return JsonResponse({'code': 400, 'message': 'CreditTransaction not found'})
        
        # 获取分页参数
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        # 创建 Paginator 对象
        paginator = Paginator(creditTransaction, size)
        # 获取当前页的数据
        creditTransaction_page = paginator.get_page(page)
        serializer = CreditTransactionSerializer(creditTransaction_page, many=True)
        data = {
            'data': serializer.data,
            'count': paginator.count
        }
        return Response({'code': 200, 'message': 'success', 'data': data})

