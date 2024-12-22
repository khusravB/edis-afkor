from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, mixins, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from openai import OpenAI
from rest_framework.parsers import JSONParser
import google.generativeai as genai
import requests as rqs
import json
import re


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class PersonalCourseListView(generics.ListAPIView):
    serializer_class = PersonalCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the PersonalCourses
        for the currently authenticated user.
        """
        user = self.request.user
        return PersonalCourse.objects.filter(author=user)


@permission_classes([IsAuthenticated])
class BrainBytesViewSet(viewsets.ModelViewSet):
    queryset = BrainBytes.objects.all()
    serializer_class = BrainBytesSerializer


class CommentsBViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsBSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Получаем комментарии только для конкретного видео
        video_pk = self.kwargs.get('video_pk')
        return CommentsB.objects.filter(video_id=video_pk).order_by('-created_at')

    def perform_create(self, serializer):
        # Устанавливаем автора и видео автоматически
        video_pk = self.kwargs.get('video_pk')
        video = BrainBytes.objects.get(pk=video_pk)
        serializer.save(video=video)


@permission_classes([IsAuthenticated])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@permission_classes([IsAuthenticated])
class ResearchViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer


@permission_classes([IsAuthenticated])
class CooperationViewSet(viewsets.ModelViewSet):
    queryset = Cooperation.objects.all()
    serializer_class = CooperationSerializer


class CommentsCViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsCSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Получаем комментарии только для конкретного видео
        video_pk = self.kwargs.get('video_pk')
        return CommentsC.objects.filter(video_id=video_pk).order_by('-created_at')

    def perform_create(self, serializer):
        # Устанавливаем автора и видео автоматически
        video_pk = self.kwargs.get('video_pk')
        video = Post.objects.get(pk=video_pk)
        serializer.save(video=video)


class LikeBrainBytesView(APIView):
    def post(self, request, pk):
        try:
            brain_byte = BrainBytes.objects.get(pk=pk)
            brain_byte.likes += 1
            brain_byte.save()
            return Response({"likes": brain_byte.likes}, status=status.HTTP_200_OK)
        except BrainBytes.DoesNotExist:
            return Response({"error": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)


class ShareBrainBytesView(APIView):
    def post(self, request, pk):
        try:
            brain_byte = BrainBytes.objects.get(pk=pk)
            brain_byte.shares += 1
            brain_byte.save()
            return Response({"shares": brain_byte.shares}, status=status.HTTP_200_OK)
        except BrainBytes.DoesNotExist:
            return Response({"error": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)


YOUR_API_KEY = "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"
client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")


class ChatAPIView(APIView):
    def post(self, request):
        # Получаем сообщение пользователя
        user_message = request.data.get("content")
        if not user_message:
            return Response(
                {"error": "Message content is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Формируем историю общения
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ]

        try:
            # Запрос к OpenAI
            response = client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages,
            )


            return Response(
                {
                    "user_message": user_message,
                    "response": response,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Обработка ошибок
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        
genai.configure(api_key="AIzaSyCx_cztl-UXI0GTQmhYUrROPNOlaASB5WE")
model = genai.GenerativeModel("gemini-2.0-flash-exp")  # Указываем нужную модель Gemini


class AdaptCoursePlanAPIView(APIView):
    def post(self, request, pk):
        try:
            # Получаем курс по pk
            course = Course.objects.get(pk=pk)
            course_plan = course.plan

            # Получаем результаты теста текущего пользователя для данного курса
            try:
                test_result = TestResult.objects.get(author=request.user, course=course)
            except TestResult.DoesNotExist:
                return Response(
                    {"error": "Test results for this course are not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Получаем предпочтения пользователя
            try:
                user_preference = UserPreference.objects.get(author=request.user)
                preferred_type = user_preference.preferred_type_of_studying
            except UserPreference.DoesNotExist:
                return Response(
                    {"error": "User preferences not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Формируем запрос для модели Gemini
            gemini_request = f"""
                Adapt this course plan based on the following test results and user preferences. Do not change plan structure you have only permission to delete lessons if test results show that someone already knows this lesson:
                Course plan: {course_plan.description}
                Test results: {test_result.result}
                User's preferred type of studying: {preferred_type}
            """

            # Запрашиваем адаптированный курс у модели Gemini
            response = model.generate_content(gemini_request)

            # Извлекаем адаптированный план из ответа
            adapted_plan = response.text

            # Создаем персональный курс с типом из предпочтений пользователя
            personal_course = PersonalCourse.objects.create(
                course=course,
                author=request.user,
                plan=adapted_plan,
                type=preferred_type  # Присваиваем тип из предпочтений
            )

            # Возвращаем данные персонального курса
            serializer = PersonalCourseSerializer(personal_course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


perplexity_api_key = "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"


class GenerateAllLessonsAPIView(APIView):
    def post(self, request, pk):
        try:
            # Получаем персональный курс
            personal_course = get_object_or_404(PersonalCourse, pk=pk)
            plan = personal_course.plan

            # Проверяем, является ли план строкой (например, JSON)
            if isinstance(plan, str):
                try:
                    plan = json.loads(plan)  # Преобразуем строку JSON в Python-объект
                except json.JSONDecodeError:
                    return Response({"error": "Invalid plan format. Must be valid JSON."}, status=status.HTTP_400_BAD_REQUEST)

            # Инициализация списка уроков
            lessons = []

            # Разбиваем план на уроки
            for lesson in plan.get("lessons", []):
                lesson_title = lesson.get("title", "Untitled Lesson")
                topics = lesson.get("topics", [])
                description = lesson.get("description", "")
                lesson_content = ", ".join(topics) if topics else description

                # Генерация текста для урока через Gemini
                try:
                    model = genai.GenerativeModel("gemini-2.0-flash-exp")
                    text_response = model.generate_content("Generate detailed lesson but ignore quiz and exercise. Only text of lesson. Do not add any additional text, only lesson "+lesson_content)
                    lesson_text = text_response.text
                except Exception as genai_error:
                    lesson_text = "Could not generate lesson content."

                # Поиск видео через Perplexity
                try:
                    video_prompt = f"Find YouTube videos related to: {lesson_content}. Respond only with a list of links."
                    perplexity_response = client.chat.completions.create(
                        model="llama-3.1-sonar-large-128k-online",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": video_prompt},
                        ],
                    )

                    str_response = str(perplexity_response)
                    video_links = re.findall(r'https?://[^\s,\'"]+', str_response)
                    print(video_links)
                    # Объединяем ссылки в строку

                except Exception as perplexity_error:
                    video_links = "Could not retrieve video links."

                # Сохранение урока
                lesson_obj = Lesson.objects.create(
                    personal_course=personal_course,
                    title=lesson_title,
                    text=lesson_text,
                    video_links=video_links,
                )
                lessons.append(lesson_obj)

            # Возвращаем все уроки
            return Response(LessonSerializer(lessons, many=True).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetLessonsByCourseAPIView(APIView):
    def get(self, request, pk):
        """
        Получает все уроки, связанные с указанным персональным курсом.
        """
        try:
            # Получаем персональный курс по его ID
            personal_course = get_object_or_404(PersonalCourse, pk=pk)

            # Получаем уроки, связанные с этим курсом
            lessons = Lesson.objects.filter(personal_course=personal_course)

            # Сериализуем данные
            serializer = LessonSerializer(lessons, many=True)

            # Возвращаем данные
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # В случае ошибки возвращаем сообщение об ошибке
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)