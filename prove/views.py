from django.shortcuts import render
from rest_framework import status, viewsets
from .models import Person, History
from .serializers import PersonSerializer, HistorySerializer
from django.shortcuts import get_object_or_404
from account.permissions import IsStaffUser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

class PersonViewSet(viewsets.ViewSet):

    def list(self, request): # [GET] lấy danh sách các đối tượng
        queryset = Person.objects.all()
        serializer = PersonSerializer(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request): # [POST] tạo mới một đối tượng
        try:
            data = request.data # Dữ liệu gửi qua body JSON
            uid = data.get('uid', None)
            if uid:
                # Kiểm tra xem có đối tượng nào với uid này trong cơ sở dữ liệu không
                if Person.objects.filter(uid=uid).exists():
                    return Response(
                        {"status": "fail", "message": "UID already exists."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    # Tạo mới đối tượng Person nếu uid không tồn tại
                    serializer = PersonSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             return Response(
                {"status": "fail", "message": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def retrieve(self, request, pk=None): # [GET] lấy chi tiết một đối tượng cụ thể
        person = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None): # [PATCH] cập nhật một phần đối tượng
        person = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None): # [DELETE] xóa một đối tượng
        person = get_object_or_404(Person, pk=pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoryViewSet(viewsets.ViewSet):
    lookup_field = 'date'  # Tùy chỉnh lookup_field

    def retrieve(self, request, date=None):
        """
        Tìm các bản ghi lịch sử dựa trên ngày.
        """
        try:
            # Chuyển đổi ngày thành datetime.date
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Lọc các đối tượng theo ngày
            histories = History.objects.filter(timeline__date=date_obj)
            
            # Serialize và trả về kết quả
            serializer = HistorySerializer(histories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    
class RFID1ViewSet(viewsets.ViewSet):   
    @csrf_exempt
    def retrieve(self, request, pk=None):
        # Kiểm tra xem person có tồn tại hay không
        person = get_object_or_404(Person, pk=pk)

        # Tạo bản ghi history nếu person tồn tại
        if person.activate:
            History.objects.create(
                gate=True,
                person=person
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Nếu person không tồn tại, trả về lỗi 404
            return Response(status=status.HTTP_404_NOT_FOUND)

class RFID2ViewSet(viewsets.ViewSet):   
    @csrf_exempt
    def retrieve(self, request, pk=None):
        # Kiểm tra xem person có tồn tại hay không
        person = get_object_or_404(Person, pk=pk)

        # Tạo bản ghi history nếu person tồn tại
        if person.activate:
            History.objects.create(
                gate=False,
                person=person
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Nếu person không tồn tại, trả về lỗi 404
            return Response(status=status.HTTP_404_NOT_FOUND)
