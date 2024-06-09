from django.db import models


from django.conf import settings

class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    employee_id = models.CharField(max_length=100, default="")
    pub_key = models.CharField(max_length=256, default="")
    priv_key = models.CharField(max_length=256, default="")
    priv_key_2 = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.first_name

class Administrator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    employee_id = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.first_name

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="example@example.com")
    employee_id = models.CharField(max_length=100, default="")
    
    def __str__(self):
        return self.first_name

class Medicine(models.Model):
    manager_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=500, default=None)
    # timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Component(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=500, default=None)
    cost = models.CharField(max_length=500, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Details(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=500, default=None)
    cost = models.CharField(max_length=500, default=None)
    # timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
