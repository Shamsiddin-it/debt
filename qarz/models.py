from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# class CustomUser(AbstractUser):

#     pass

class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    customer_name = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    chat_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now=True)
    duration_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.customer_name    

    def payback(self, amount_paid):
        """Method to reduce the debt amount after a partial or full payment."""
        if self.is_active and amount_paid > 0:
            self.amount -= amount_paid
            self.save()  
            if self.amount <= 0:
                self.is_active = False  
                self.save()
            return self.amount
        return None


class ReturnDebt(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)

    def payback(self):
        """Record the payment and update the debt balance."""
        if self.debt.payback(self.amount) is not None:
            return True  
        return False



