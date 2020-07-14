from rest_framework import serializers

from grouplearning.models import Group
from sop.models import Course


# create group course
class GroupCourseSerializer(serializers.Serializer):
    new_course_id_list = serializers.ListField(child=serializers.IntegerField())

    def validate_new_course_id_list(self, value):
        for i in value:
            if not Course.objects.filter(pk=i).exists():
                raise serializers.ValidationError("{0} is not a valid Course id.".format(i))
        return value
