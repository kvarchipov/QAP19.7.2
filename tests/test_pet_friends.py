# Новые тесты начинаются с: 90 - 2 не рассмотренных теста, 130 - 10 дополнительных тестов
import os.path

from api import PetFriends
from settings import valid_email, valid_password, valid_email2, valid_password2


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    #отправка запроса и сохраниние: полученного ответа с кодом статуса в status,а самого ответа в result

    assert status == 200
    assert 'key' in result
    #проверка полученного результата


def test_get_all_pets_with_valid_key(filter=""):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) > 0


def test_post_add_information_about_new_pet_valid_data(name='Котовских', animal_type='дворовый',
                                     age='6', pet_photo='images/cat.jpg'):
    """Проверяем что можно добавить питомца с корректными параметрами"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    #полный путь до изображения теперь в переменной pet_photo

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    #добавление питомца

    assert status == 200
    assert result["name"] == name

def test_delete_information_about_pet_from_database_valid():
    """Проверка возможности удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получение ключа и списка своих питомцев

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        # Проверка - если список пуст то добавляем питомца и запрашиваем новый список своих питомцев

    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pets(auth_key, "my_pets")
    #Используем id первого питомца из списка, для его удаления

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_put_information_about_pet_from_database_valid(name='Мурзик', animal_type='Котэ', age="5"):
    # Проверка возможности обновления информации о питомце
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получение ключа и списка своих питомцев

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.put_pets(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
#######################################################################################################################
#Не рассмотренные ранее 2 примера


def test_post_add_new_pet_without_photo_valid_data(name='Котовских', animal_type='дворовый', age='8'):
    """Проверяем что можно добавить питомца с корректными параметрами без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # добавление питомца

    assert status == 200
    assert result["name"] == name


def test_post_add_pet_photo_valid(pet_photo='images/wrg.jpg'):
    """Проверяем что можно добавить фотографию питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    #полный путь до изображения теперь в переменной pet_photo

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получение ключа и списка своих питомцев

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        # Проверка - если список пуст то добавляем питомца и запрашиваем новый список своих питомцев

    pet_id = my_pets["pets"][0]["id"]

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
    #добавление питомца

    assert status == 200
    assert result["pet_photo"] != ""


# 10 дополнительных тестов---------------------------------------------------------------------------------------
def test_get_api_key_for_no_valid_user(email=valid_email, password=valid_password+"t"):
    """ Проверяем что не верный запрос api ключа возвращает статус 403 и в результате не содержится слово key"""

    status, result = pf.get_api_key(email, password)
    #отправка запроса и сохраниние: полученного ответа с кодом статуса в status,а самого ответа в result

    assert status == 403
    assert 'key' not in result
    #проверка полученного результата

#2
def test_get_all_pets_with_no_valid_key(filter=""):
    """ Проверяем что запрос всех питомцев не происходит, когда auth_key не верен """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key["key"] = "no_auth_key"
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert "auth_key" in result
    assert "pets" not in result

#3
def test_get_all_pets_with_no_valid2_key(filter=""):
    """ Проверяем что запрос всех питомцев не происходит, когда auth_key 'True' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key["key"] = "True"
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert "auth_key" in result
    assert "pets" not in result

#4
def test_post_add_information_about_new_pet_no_valid_data(name='', animal_type='',
                                     age='', pet_photo='images/cat.jpg'):
    """Проверяем что нельзя добавить питомца с пустыми параметрами, вставив только картинку"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    #полный путь до изображения теперь в переменной pet_photo

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    #добавление питомца

    assert status == 400
    assert result["name"] == name

#5
def test_post_add_information_about_new_pet_valid_data_png(name='Гари', animal_type='Орангутанг',
                                     age='1', pet_photo='images/abbs.png'):
    """Проверяем что можно добавить питомца с фотографией формата png"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    #полный путь до изображения теперь в переменной pet_photo

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    #добавление питомца

    assert status == 200
    assert result["name"] == name

#6
def test_delete_stranger_pet_from_database_no_valid(filter=""):
    """Проверка возможности удаления чужого питомца"""

    _, auth_key = pf.get_api_key(valid_email2, valid_password2)

    pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat.jpg")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, _ = pf.get_list_of_pets(auth_key, filter)
    status, _ = pf.delete_pets(auth_key, "")
    #Используем id первого питомца из списка, для его удаления

    _, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 404
    assert pet_id not in result

#7
def test_post_add_new_pet_without_photo_valid_no_data(name='Котовских'*100, animal_type='дворовый'*100, age='11'):
    """Проверяем что нельзя добавить питомца со слишком длинными параметрами"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # добавление питомца

    assert status == 400
    assert result["name"] == name


def test_post_add_pet_photo_valid_png(pet_photo='images/abbs.png'):
    """Проверяем что можно добавить фотографию питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    #полный путь до изображения теперь в переменной pet_photo

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получение ключа и списка своих питомцев

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        # Проверка - если список пуст то добавляем питомца и запрашиваем новый список своих питомцев

    pet_id = my_pets["pets"][0]["id"]

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
    #добавление питомца

    assert status == 200
    assert result["pet_photo"] != ""

#9
def test_put_stranger_information_about_pet_no_valid(name='Мурзик', animal_type='Котэ', age="5"):
    """Проверка возможности обновления информации о чужом питомце"""
    _, auth_key = pf.get_api_key(valid_email2, valid_password2)
    pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "")
    # Получение ключа и списка питомцев

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.put_pets(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 404
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#10
def test_post_add_new_pet_without_photo_valid_no_data2(name=';"%№"№;!><', animal_type='!"№У;%:', age='один'):
    """Проверка введения спец символов"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # добавление питомца

    assert status == 403
    assert result["name"] == name

