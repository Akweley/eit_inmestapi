from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View


from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from main.models import *
from main.serializers import *
from datetime import *


# Create your views here.
# SELECT * FROM main_course ORDER BY name ASC

@api_view(["GET"])
def fetch_class_schedules(request):
    # 1. Retrieve from db all class schedules
    queryset = ClassSchedule.objects.all()

    # 2. Return queryset result as response
    # 2b. Transform/serialize the queryset result to json and send as response

    serializer = ClassScheduleSerializer(queryset, many=True)

    # 3. Response to the request
    return Response({"data": serializer.data}, status.HTTP_200_OK)

@api_view(["POST"])
def create_class_schedule(request):
    # 4. Receiving data from frontend
    title = request.data.get("title")
    description = request.data.get("description")
    start_date_and_time = request.data.get("start_date_and_time")
    end_date_and_time = request.data.get("end_date_and_time")
    cohort_id = request.data.get("cohort_id")
    venue = request.data.get("venue")
    facilitator_id = request.data.get("facilitator_id")
    is_repeated = request.data.get("is_repeated")
    repeat_frequency = request.data.get("repeat_frequency")
    course_id = request.data.get("course_id")
    meeting_type = request.data.get("meeting_type")

    # performing validations
    if not title:
        return Response({"message":"My friend, send me title"}, status.HTTP_400_BAD_REQUEST)

    cohort = None
    facilitator = None
    course = None

    # Validating the existence of records

    try:
        cohort = Cohort.object.get(id=cohort_id)
    except Cohort.DoesNotExist:
        return Response({"message": "Massaa, this cohort does not exist"}, status.HTTP_400_BAD_REQUEST)

    try:
        facilitator = IMUser.object.get(id=facilitator_id)
    except IMUser.DoesNotExist:
        return Response({"message": "Massaa, this facilitator does not exist"}, status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.object.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"message": "Massaa, this course does not exist"}, status.HTTP_400_BAD_REQUEST)

    class_schedule = ClassSchedule.objects.create(
        title=title,
        description=description,
        venue=venue,
        is_repeated=is_repeated,
        repeat_frequency=repeat_frequency,
        facilitator=facilitator,
        start_date_and_time=datetime.daytime.now(),
        end_date_and_time=datetime.daytime.now(),
        cohort=cohort,
        course=course,
        organizer=facilitator
    )
    class_schedule.save()

    serializer = ClassScheduleSerializer(class_schedule, many=False)
    return Response({"message": "Schedule successfully created", "data": serializer.data}, status.HTTP_201_CREATED)




class QueryModelViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=["post"])
    def raise_query(self, request):
        title = request.data.get("title", None)
        description = request.data.get("description", None)
        query_type = request.data.get("query_type", None)
        assignee = None
        
        query = Query.objects.create(
            title=title,
            description=description,
            query_type=query_type,
            submitted_by=request.user
            # author=request.user
        )
        query.save()
        # send email to the assignee
        return Response({"message": "Query successfully submitted"})