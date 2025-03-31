import pytest
from model_bakery import baker

from rest_framework.test import APIClient

from students.models import Course, Student

URL_COURSES = '/api/v1/courses/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
# проверка получения первого курса
def test_retrieve_course(client, course_factory):
    # создаём курс через фабрику
    course = course_factory(_quantity=1)
    # делаем запрос через тестовый клиент
    response = client.get(URL_COURSES)
    # проверяем, что вернулся именно тот курс, который запрашивали
    data = response.json()
    assert data[0]['name'] == course[0].name
    assert response.status_code == 200


@pytest.mark.django_db
# проверка получения списка курсов
def test_get_list_courses(client, course_factory):
    # создаём несколько курсов через фабрику
    courses = course_factory(_quantity=15)
    # делаем запрос через тестовый клиент
    response = client.get(URL_COURSES)
    # проверяем, что вернулись именно те курсы, которые запрашивали
    data = response.json()
    for i, c in enumerate(data):
        assert data[i]['name'] == courses[i].name
    assert response.status_code == 200


@pytest.mark.django_db
# проверка фильтрации списка курсов по id
def test_filter_courses_by_id(client, course_factory):
    # создаём несколько курсов через фабрику
    courses = course_factory(_quantity=15)
    # получаем id последнего курса
    course_ids = [course.id for course in courses]
    course_id = course_ids[-1]
    # передаём id полученного курса в фильтр
    response = client.get(f'{URL_COURSES}?id={course_id}')
    # проверяем результат запроса с фильтром
    data = response.json()
    assert len(data) == 1
    assert data[-1]['id'] == course_id
    assert response.status_code == 200


@pytest.mark.django_db
# проверка фильтрации списка курсов по name
def test_filter_courses_by_name(client, course_factory):
    # создаём несколько курсов через фабрику
    courses = course_factory(_quantity=15)
    # получаем название последнего курса
    course_names = [course.name for course in courses]
    course_name = course_names[-1]
    # передаём название полученного курса в фильтр
    response = client.get(f'{URL_COURSES}?name={course_name}')
    # проверяем результат запроса с фильтром
    data = response.json()
    assert data[-1]['name'] == course_name
    assert response.status_code == 200


@pytest.mark.django_db
# тест успешного создания курса
def test_create_course(client):
    # подготовка данных
    data_course = {"name": "математика"}
    count = Course.objects.count()
    # делаем запрос
    response = client.post(URL_COURSES, data=data_course)
    # проверяем результат запроса
    data = response.json()
    assert data_course['name'] == data['name']
    assert Course.objects.count() == count + 1
    assert response.status_code == 201


@pytest.mark.django_db
# тест успешного обновления курса
def test_update_course(client, course_factory):
    # создаём несколько курсов через фабрику
    courses = course_factory(_quantity=15)
    # получаем id первого курса
    course = courses[0]
    course_id = course.id
    # создаём данные для обновления
    data_course = {"name": "test name"}
    count = Course.objects.count()
    # обновляем название одного из курса
    response = client.put(f'{URL_COURSES}{course_id}/', data=data_course)
    # проверяем результат запроса
    data = response.json()
    assert data_course['name'] == data['name']
    assert Course.objects.count() == count
    assert response.status_code == 200


@pytest.mark.django_db
# тест успешного удаления курса
def test_delete_course(client, course_factory):
    # создаём несколько курсов через фабрику
    courses = course_factory(_quantity=15)
    # получаем id и названия курса, к-рый удалим
    course = courses[-1]
    course_id = course.id
    # получаем количество курсов
    count = Course.objects.count()
    # делаем запрос
    response = client.delete(f'{URL_COURSES}{course_id}/')
    # проверяем результат запроса
    assert response.status_code == 204
    assert Course.objects.count() == count - 1
    assert course_id not in [course.id for course in Course.objects.all()]


@pytest.mark.parametrize(
    ['max_students', 'count_students', 'expected_status'],
    ((5, 4, 201),
     (5, 5, 201),
     (5, 6, 400))
)
@pytest.mark.django_db
# проверка ограничения количество студентов на курсе
def test_limit_students_settings(settings, client, max_students,
                                 count_students, expected_status, student_factory):
    settings.MAX_STUDENTS_PER_COURSE = max_students
    students = student_factory(_quantity=count_students)
    data_course = {'name': 'test name',
                   'students': [student.id for student in students]}
    response = client.post('/api/v1/courses/', data=data_course)
    assert response.status_code == expected_status
