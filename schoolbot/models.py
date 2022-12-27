from django.db import models


class TelegramUser(models.Model):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
    )
    user_id = models.BigIntegerField(unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_bot = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    bun = models.BooleanField(default=False)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='user')
    description = models.CharField(max_length=300, null=True, blank=True)
    


    def __str__(self):
        if self.username:
            return f'{self.username}'
        else:
            return f'{self.user_id}'

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
        ordering = ['username']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Grade(models.Model):
    grade = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.grade}'

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['grade']


class Subject(models.Model):
    subject = models.CharField(max_length=255, unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['grade']


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('done', 'Выполнен'),
        ('canceled', 'Отменен'),
        ('in_progress', 'В процессе'),
    )
    PAYMENT_CHOICES = (
        ('paid', 'Оплачен'),
        ('not_paid', 'Не оплачен'),
    )
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='orders')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='new')
    payment = models.CharField(max_length=255, choices=PAYMENT_CHOICES, default='not_paid')
    photo = models.CharField(max_length=700,null=True, blank=True)
    order = models.TextField(null=True, blank=True)
    date_to_complete = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class OrderProcess(models.Model):
    STATUS_CHOICES = (
        ('done', 'Выполнен'),
        ('canceled', 'Отменен'),
        ('in_progress', 'В процессе'),
        ('dispute', 'Спор'),
        ('on_check', 'На проверке')
    )

    PAYMENT_CHOICES = (
        ('paid', 'Оплачен'),
        ('not_paid', 'Не оплачен'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_process')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='in_progress')
    payment = models.CharField(max_length=255, choices=PAYMENT_CHOICES, default='not_paid')
    doer = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='order_doer')
    photo = models.CharField(max_length=500, null=True, blank=True)
    order_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Процесс заказа'
        verbose_name_plural = 'Процессы заказов'
        ordering = ['-created_at']

#ЗДЕСЬ МЫ СОЗДАЕМ МОДЕЛЬКУ УЧЕНИКА 
class Student(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='students') #уникальное айди пользователя в системе, счетчик регистраций, аналогично таблице user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    stud_comment = models.CharField(max_length=300, null=True, blank=True ) #прописывается арбитражником, для указания причины полного бана, либо просто комментарий к пользователю
    stud_tasks_add = models.IntegerField(null=True, blank=True) #счетчик количества добавленных в систему заданий
    stud_tasks_paid = models.IntegerField(null=True, blank=True) #счетчик оплаченных заданий
    stud_tasks_pass = models.IntegerField(null=True, blank=True) #счетчик оплаченных заданий, которые учитель в итоге не смог решить и нажал кнопку - не могу решить
    stud_tasks_solved = models.IntegerField(null=True, blank=True) #счетчик оплаченных заданий, которые учитель решил и скинул решение
    stud_tasks_not_paid = models.IntegerField(null=True, blank=True) #счетчик не оплаченных заданий ( учитель согласился решать, а оплата не прошла)
    stud_tasks_ban = models.IntegerField(null=True, blank=True) #добавлена запрещенная картинка или текст
    stud_tasks_arbitration = models.IntegerField(null=True, blank=True) #задание некоректно, не хватает данных, или ошибочно выбран предмет или класс
    stud_tasks_arbitration_incorrect = models.IntegerField(null=True, blank=True) #при нажатии на кнопку - решение с ошибкой прибавляем + 1 к счетчику
    tasks_arbitration_correctstud = models.IntegerField(null=True, blank=True) #при отказе в арбитраже ( решение правильное)  прибавляем + 1 к счетчику
    stud_amount = models.IntegerField(null=True, blank=True) #сумма оплаченных решений. прибавляем когда учитель нажал на кнопку "оплата получена"
    stud_level = models.IntegerField(default = 1) 
    stud_calc_value = models.IntegerField(null=True, blank=True)







    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['user']

class Teacher(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='teachers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=300, null=True, blank=True) 
    teacher_comment = models.CharField(max_length=300, null=True, blank=True ) #прописывается арбитражником, для указания причины полного бана, либо просто комментарий к учителю
    teacher_tasks_ban = models.BooleanField(default=False) #добавлена запрещенная картинка или текст. учитель отметил задание как бан
    teach_tasks_paid = models.IntegerField(null=True, blank=True) #счетчик оплаченных заданий( учитель согласился решать, и пришла оплата)
    teach_tasks_not_paid = models.IntegerField(null=True, blank=True) #счетчик не оплаченных заданий ( учитель согласился решать, а оплата не прошла)
    teach_tasks_solved = models.IntegerField(null=True, blank=True) #счетчик решенных заданий ( учитель согласился решать, пришла оплата, учитель добавил в бота решение)
    teach_tasks_pass = models.IntegerField(null=True, blank=True) #счетчик решенных заданий ( учитель согласился решать, пришла оплата, учитель нажал кнопку "не могу решить" )
    teach_tasks_not_solved_in_time = models.IntegerField(null=True, blank=True) #счетчик решенных заданий ( учитель согласился решать, пришла оплата, но учитель добавил решение после окончания допустимого времени )
    teach_tasks_arbitration = models.IntegerField(null=True, blank=True)  #при нажатии на кнопку - решение с ошибкой прибавляем + 1 к счетчику
    teach_tasks_arbitration_incorrect = models.IntegerField(null=True, blank=True) #при отказе в арбитраже ( решение правильное)  прибавляем + 1 к счетчику
    tasks_arbitration_correctteach = models.IntegerField(null=True, blank=True) #при подтверждении в арбитраже ( решение не правильное)  прибавляем + 1 к счетчику
    teach_amount = models.IntegerField(null=True, blank=True) #сумма оплаченных решений. прибавляем когда учитель нажал на кнопку "оплата получена"
    teach_fee = models.IntegerField(null=True, blank=True) #прибавляем штраф в случае нерешенного, просроченного или решения с ошибкой(подтвержденное арбитражником)
    teach_comission = models.IntegerField(null=True, blank=True)  #прибавляем task_comission
    teach_total_sum_to_pay = models.IntegerField(null=True, blank=True) #teach_fee + teach_total_sum_to_pay
    teach_paid = models.IntegerField(null=True, blank=True) #сумма оплаченных комиссий и штрафов
    teach_level = models.IntegerField(default = 1)
    teach_calc_value = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ['user']
        

