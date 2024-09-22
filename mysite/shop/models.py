from django.db import models

status_point = {'gold':0.75,'silver':0.50,'bronze':0.25,'simple':0}


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    age = models.PositiveSmallIntegerField(null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    phono_number = models.IntegerField(null=True,blank=True)
    date_registered = models.DateField(auto_now= True ,null=True,blank=True)
    STATUS_CHOICES = (
        ('gold','Gold'),
        ('silver','Silver'),
        ('bronze','Bronze'),
        ('simple','Simple'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple' )


    def __str__(self):
        return self.first_name




class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    active =  models.BooleanField(default=True)
    video = models.FileField(verbose_name='Видео',upload_to='videos/' , null=True , blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists:
            return 0
        return 0


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product,related_name='product', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')

class Rating(models.Model):
    product = models.ForeignKey(Product,related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1,6) ], verbose_name='оценка')

    def __str__(self):
        return f'{self.user} - {self.product} - {self.stars} stars'

class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews',on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.author} - {self.text}'

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE,related_name='cart')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.data}'



class CarItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):

        return self.product.price * self.quantity

