import django_filters.rest_framework
from random import choice
from rest_framework import viewsets, response, status, generics

from .models import TelegramUser, Grade, Subject, Order, OrderProcess, Student, Teacher
from .serializers import TelegramUserSerializer, GradeSerializer, SubjectSerializer, OrderSerializer, \
    OrderProcessSerializer, OrderListSerializer, OrderDetailSerializer, OrderProcessCreateSerializer, StudentSerializer, TeacherSerializer, \
        OrderProcessUpdateSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('role', 'user_id')

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('user__user_id',)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('user__user_id',)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('grade__grade',)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def list(self, request, *args, **kwargs):
        print(request.data)
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # print(serializer.validated_data)
        try: 
            user = TelegramUser.objects.get(user_id=serializer.validated_data['user'])
            subject = Subject.objects.get(subject=serializer.validated_data['subject'])

            order = Order.objects.create(
                user=user,
                price=serializer.validated_data['price'],
                subject=subject,
                photo=serializer.validated_data['photo']
                
            )
            return response.Response({'order_id': order.id}, status=status.HTTP_201_CREATED)
        except:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('user__user_id', 'order_process__status',)
    
    
    

    
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class OrderRetrieveView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    slug = 'subject'


    def get_object(self, subject):
        pks = Order.objects.filter(subject__subject=subject, status='new').values_list('id', flat=True)
        if pks:
            random_pk = choice(pks)
            return Order.objects.get(pk=random_pk)
        else:
            return None


    def retrieve(self, request, *args, **kwargs):
        if kwargs['subject']:
            order = self.get_object(kwargs['subject'])
            if order:
                serializer = OrderDetailSerializer(order)
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return response.Response({'message': 'No orders'}, status=status.HTTP_404_NOT_FOUND)


class OrderProcessViewSet(viewsets.ModelViewSet):
    queryset = OrderProcess.objects.all()
    serializer_class = OrderProcessSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = []
    

    def create(self, request, *args, **kwargs):
        serializer = OrderProcessCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try: 
            doer = TelegramUser.objects.get(user_id=serializer.validated_data['doer'])
            order = Order.objects.get(id=serializer.validated_data['order'])
            
            order.status = 'in_progress'
            order.save()

            order = OrderProcess.objects.create(
                doer=doer,
                order=order
            )
            return response.Response({'ok': 'ok'}, status=status.HTTP_201_CREATED)
        except:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        serializer = OrderProcessUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.filter(id=serializer.validated_data['order_id'])[0]
        print(order)
        order_process = OrderProcess.objects.filter(order=order)[0]
        print(order_process)
        if request.data.get('status'):
            order_process.status = serializer.validated_data['status']
        if request.data.get('payment'):
            order_process.payment = serializer.validated_data['payment']
        if request.data.get('photo'):
            order_process.photo = serializer._validated_data['photo']
        
        order_process.save()
        return response.Response({'order_process_id': order_process.id, 'order_user_id': order.user.user_id}, status=status.HTTP_202_ACCEPTED)
        

    

        

    

