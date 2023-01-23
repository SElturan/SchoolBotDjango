from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.admin import display
from django.db.models import Sum


from .models import TelegramUser, Grade, Subject, Order, OrderProcess, Student, Teacher

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'username', 'role', 'first_name', 'last_name', 'is_bot', 'phone_number', 'bun', 'description', 'view_orders', 'view_completed_orders', 'view_arbitrage_orders', 'view_payment_orders', 'view_not_paid_orders',)
    list_display_links = ('id', 'user_id', 'username',)
    list_filter = ('is_bot', 'bun', 'role')
    search_fields = ('id', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('id',)

    #ЗДЕСЬ МЫ ПОЛУЧИМ ВСЮ СТАТИСТИКУ УЧИТЕЛЯ, СКОЛЬКО ОН ЗАКАЗОВ СДЕЛАЛ , СКОЛЬКО ЗАРАБОТАЛ
    @display(description='Все заказы')
    def view_orders(self, obj):
        if obj.role == TelegramUser.ROLE_CHOICES[2][0]:
            order_process_count = OrderProcess.objects.filter(doer=obj).count()

            url = (
                reverse("admin:schoolbot_orderprocess_changelist")
                + "?"
                + urlencode({"doer__id": f"{obj.id}"})
            )
            return format_html('<a href="{}">{} заказов</a>', url, order_process_count)
        elif obj.role == TelegramUser.ROLE_CHOICES[1][0]:
            order_count = Order.objects.filter(user=obj).count()

            url = (
                reverse("admin:schoolbot_order_changelist")
                + "?"
                + urlencode({"user__id": f"{obj.id}"})
            )
            return format_html('<a href="{}">{} заказов размещено</a>', url, order_count)
        return format_html('<b>Анонимный пользователь</b>')

        
    #ЗДЕСЬ МЫ ПОЛУЧИМ КОЛИЧЕСТВО ВЫПОЛНЕННЫХ ЗАКАЗОВ СО СТАТУСОМ ВЫПОЛНЕНО ИЗ ПРОЦЕССОВ ЗАКАЗА
    @display(description='Количество выполненных заказов ')
    def view_completed_orders(self, obj):
        order_count = OrderProcess.objects.filter(doer=obj, status='done').count()
        url = (
            reverse("admin:schoolbot_orderprocess_changelist")
            + "?"
            + urlencode({"doer__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} заказов</a>', url, order_count)

    #ЗДЕСЬ МЫ ПОЛУЧИМ ВСЕ ЗАКАЗЫ УЧИТЕЛЯ СО СТАТУСОМ АРБИТРАЖ
    @display(description='Заказы на арбитраже')
    def view_arbitrage_orders(self, obj):
        order_count = OrderProcess.objects.filter(doer=obj, status='dispute').count()
        url = (
            reverse("admin:schoolbot_orderprocess_changelist")
            + "?"
            + urlencode({"doer__id": f"{obj.id}"})
        
        )
        return format_html('<a href="{}">{} заказов</a>', url, order_count)
    

    @display(description='Заработано')
    def view_payment_orders(self, obj):
        order_process_sum = OrderProcess.objects.filter(doer=obj).aggregate(Sum('order__price'))
        url = (
            reverse("admin:schoolbot_orderprocess_changelist")
            + "?"
            + urlencode({"doer__id": f"{obj.id}"})
        )
        sum = order_process_sum['order__price__sum'] if order_process_sum['order__price__sum'] else 0
        return format_html('<a href="{}">{} тенге</a>', url, sum)

    @display(description='Не оплаченные задания')
    def view_not_paid_orders(self, obj):
        order_process_count = OrderProcess.objects.filter(doer=obj, payment='not_paid').count()
        url = (
            reverse("admin:schoolbot_orderprocess_changelist")
            + "?"
            + urlencode({"doer__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} заказов</a>', url, order_process_count)

 


    



class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade',)
    ordering = ('id',)

    


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'grade')
    ordering = ('id',)
    list_filter = ('grade',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'user', 'subject', 'photo', 'order',
                    'date_to_complete', 'price', )
    list_display_links = ('id', 'created_at',)
    list_filter = ('status', 'subject', 'created_at', 'updated_at', 'date_to_complete', )
    search_fields = ('user__username', 'telegram_user__first_name', 'telegram_user__last_name',
                     'user__phone_number')
    ordering = ('id',)



class OrderProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'order', 'updated_at', 'status', 'payment' ,  'doer', 'photo', )
    list_display_links = ('id', 'created_at',) 
    list_filter = ('status', 'created_at', 'updated_at', )
    search_fields = ('order__user__username', 'order__user__first_name', 'order__telegram_user__last_name',
                     'order__user__phone_number', 'doer__username', 'doer__first_name', 'doer__last_name',
                     'doer__phone_number')
    ordering = ('id',)

    

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at','pay_number', 'description', 'stud_comment', 'stud_tasks_ban', 'stud_level', 'stud_calc_value', )
    list_display_links = ('id', 'user')
    list_filter = ('created_at', 'updated_at', )
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                        'user__phone_number')
    ordering = ('id',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'created_at', 'updated_at', 'phone_number', 'pay_number', 'description', 'teacher_comment', 'teacher_tasks_ban', 'teach_paid', 'teach_level', 'teach_calc_value', )
    list_display_links = ('id', 'user')
    list_filter = ('created_at', 'updated_at', )
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                        'user__phone_number')
    ordering = ('id',)




admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProcess, OrderProcessAdmin)

