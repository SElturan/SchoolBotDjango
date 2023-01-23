from .models import TelegramUser, Grade, Subject, Order, OrderProcess, Student, Teacher

from rest_framework import serializers


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class OrderProcessForOrderList(serializers.ModelSerializer):
    class Meta:
        model = OrderProcess
        fields = ('id', 'created_at', 'updated_at', 'status', 'payment', 'photo', )

class OrderListSerializer(serializers.ModelSerializer):
    user = TelegramUserSerializer()
    subject = SubjectSerializer()
    order_process = OrderProcessForOrderList(many=True, read_only=True)


    class Meta:
        model = Order
        fields = ('id', 'user', 'subject', 'status','photo', 'order', 'date_to_complete', 'price', 'order_process', )



class OrderDetailSerializer(serializers.ModelSerializer):
    user = TelegramUserSerializer() 
    subject = SubjectSerializer()
    class Meta:
        model = Order
        fields = ('id', 'user' ,'subject', 'status', 'photo', 'order', 'date_to_complete', 'price', )


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField()
    price = serializers.IntegerField()
    subject = serializers.CharField(max_length=255)
    photo = serializers.CharField()



    # def create(self, validated_data):
    #     validated_data['user'] = TelegramUser.objects.get(user_id=validated_data['user']).id
    #     print(validated_data)
    #     return Order.objects.create(**validated_data)


class OrderProcessSerializer(serializers.ModelSerializer):
    doer = TelegramUserSerializer()
    order = OrderDetailSerializer()


    class Meta:
        model = OrderProcess
        fields = ('order', 'created_at', 'updated_at', 'status', 'payment',  'doer', 'photo', )



class OrderProcessCreateSerializer(serializers.Serializer):
    order = serializers.IntegerField()
    doer = serializers.IntegerField()




class OrderProcessUpdateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    photo = serializers.CharField(required = False)
    status = serializers.CharField(max_length=255, required=False)
    payment = serializers.CharField(max_length=255, required=False)
    




    



        
