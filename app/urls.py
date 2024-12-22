from django.urls import path, include, re_path
from .views import *
from rest_framework import routers


categories = routers.DefaultRouter()
categories.register(r'categories', CategoriesViewSet)

brain_bytes = routers.DefaultRouter()
brain_bytes.register(r'brain-bytes', BrainBytesViewSet)

post = routers.DefaultRouter()
post.register(r'post', PostViewSet)

research = routers.DefaultRouter()
research.register(r'research', ResearchViewSet)

cooperation = routers.DefaultRouter()
cooperation.register(r'cooperation', CooperationViewSet)


course = routers.DefaultRouter()
course.register(r'courses', CoursesViewSet)


urlpatterns = [
    path('', include(categories.urls)),
    path('', include(brain_bytes.urls)),
    path('', include(post.urls)),
    path('', include(research.urls)),
    path('', include(cooperation.urls)),
    path('', include(course.urls)),

    path('brain-bytes/<int:video_pk>/comments/', CommentsBViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('brain-bytes/<int:video_pk>/comments/<int:pk>/', CommentsBViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('brain-bytes/<int:pk>/share/', ShareBrainBytesView.as_view(), name='share_brain_bytes'),
    path('brain-bytes/<int:pk>/like/', LikeBrainBytesView.as_view(), name='like_brain_bytes'),
    path('post/<int:video_pk>/comments/', CommentsCViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('post/<int:video_pk>/comments/<int:pk>/',
         CommentsCViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path("chat/", ChatAPIView.as_view(), name="chat-api"),
    path("courses/<int:pk>/adapt-plan/", AdaptCoursePlanAPIView.as_view(), name="adapt-course-plan"),
    path('personal_courses/<int:pk>/generate-all-lessons/', GenerateAllLessonsAPIView.as_view(), name='generate-all-lessons'),
    path('personal-courses/<int:pk>/lessons/', GetLessonsByCourseAPIView.as_view(), name='get-lessons-by-course'),
    path('personal-courses/', PersonalCourseListView.as_view(), name='personal-course-list'),



]
