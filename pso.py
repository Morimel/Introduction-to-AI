import numpy as np
from pyswarm import pso

# Исходные данные
days = 5  # Учебная неделя
slots_per_day = 4  # Количество пар в день
courseNum = 7
teacherNum = 6
roomNum = 4
groupNum = 4

# Курсы и преподаватели
courses = [
    ("Data Structure and Algorithms", "Askarov K.R"),
    ("English", "Абакирова Э.А"),
    ("Introduction to AI", "Beishenalieva A."),
    ("Advanced Python", "Prof. Daechul Park"),
    ("География Кыргызстана", "Жумалиев Н.Э."),
    ("История Кыргызстана", "Молошев А.И."),
    ("Манасоведение", "Бегалиев Э.С.")
]

# Количество слотов в неделе
total_slots = days * slots_per_day

# Количество частиц (возможных расписаний)
num_particles = 30


# Функция для проверки корректности расписания
def fitness_function(schedule):
    schedule = schedule.reshape((days, slots_per_day, groupNum))  # Преобразуем в матрицу расписания
    penalty = 0  # Штраф за конфликты

    # Проверяем конфликты преподавателей (не могут вести 2 пары одновременно)
    teacher_slots = {}

    for day in range(days):
        for slot in range(slots_per_day):
            teachers_on_this_slot = set()
            for group in range(groupNum):
                course_index = int(schedule[day, slot, group])  # Индекс курса
                if course_index < len(courses):  # Проверяем, что индекс корректный
                    teacher = courses[course_index][1]  # Преподаватель курса
                    if teacher in teachers_on_this_slot:
                        penalty += 1  # Штраф за конфликт
                    teachers_on_this_slot.add(teacher)

    return penalty


# Ограничения: курсы должны быть в диапазоне [0, courseNum - 1]
lb = np.zeros(total_slots * groupNum)  # Нижняя граница (курс 0)
ub = np.full(total_slots * groupNum, courseNum - 1)  # Верхняя граница (курс 6)

# Запуск PSO
best_schedule, best_fitness = pso(fitness_function, lb, ub, swarmsize=num_particles, maxiter=100)

# Вывод расписания
best_schedule = best_schedule.reshape((days, slots_per_day, groupNum))

print("\nОптимизированное расписание:")
for day in range(days):
    print(f"\nДень {day + 1}:")
    for slot in range(slots_per_day):
        print(f"  {slot + 1}-я пара:")
        for group in range(groupNum):
            course_index = int(best_schedule[day, slot, group])
            if course_index < len(courses):
                course_name, teacher = courses[course_index]
                print(f"    Группа {group + 1}: {course_name} ({teacher})")
