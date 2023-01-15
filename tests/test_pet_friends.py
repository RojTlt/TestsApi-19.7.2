from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# Тесты для задания 19.7.2

# 1
def test_get_api_kay_invalid_user(email = 'invalidemail@gmail.com', password = '01230'):
    '''Проверяем ответ от сервера при попытке получить API ключ с невалидными значениями email и password'''

    status, result = pf.get_api_key(email, password)
    assert status == 403

# 2
def test_get_list_of_pets_invalid_api_key(filter = ''):
    '''Проверяем ответ от сервера при попытке получить список питомцев при невалидном значении API ключа'''

    auth_key = {'key': "1230987475829029"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

# 3
def test_add_new_pet_invalid_data(name = '', animal_type = '', age = '', pet_photo = 'images\pet.png' ):
    '''Проверяем ответ от сервера при попытке создать питомца с пустыми полями имени, вида и возраста'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

    # Баг. Сервер не должен создавать карточку питомца и присылать код 200 при пустых входных данных.#

# 4
def test_add_new_pet_invalid_age_data(name = 'Рекс', animal_type = 'Собака', age = '-20', pet_photo = 'images\pet.png' ):
    '''Проверяем ответ от сервера при попытке создать питомца с отрицательным числом в поле возраста'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

    # Баг. Сервер не должен создавать карточку питомца и присылать код 200 при отрицательном значении поля возраста.#

# 5
def test_add_new_pet_invalid_age_data2(name = 'Рекс', animal_type = 'Собака', age = ':%!??авп', pet_photo = 'images\pet.png' ):
    '''Проверяем ответ от сервера при попытке создать питомца с нечисловым значением в поле возраста'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    # Баг. Сервер не должен создавать карточку питомца и присылать код 200 при нечисловом значении поля возраста.#

# 6
def test_add_new_pet_invalid_age_data2(name = 'Рекс', animal_type = '123', age = '12', pet_photo = 'images\pet.png' ):
    '''Проверяем ответ от сервера при попытке создать питомца с числовым значением в поля породы'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    # Баг. Сервер не должен создавать карточку питомца и присылать код 200 при числовом значении поля породы.#

# 7
def test_delete_stranger_pet():
    '''Проверяем ответ от сервера при попытке удалить чужого питомца'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, filter='')
    pet_id = pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, pets = pf.get_list_of_pets(auth_key, filter='')

    assert status == 200
    assert pet_id not in pets.values()

    # Баг. Сервер не должен выполнять функцию удаления питомца и присылать код 200 при попытке удалить чужого питомца.#

# 8
def test_update_stranger_pet(name = 'buu', animal_type = 'frog', age = '2'):
    '''Проверяем ответ от сервера при попытке отредактировать чужого питомца'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, filter='')
    status, result = pf.update_pet_info(auth_key, pets['pets'][0]['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name

    # Баг. Сервер не должен выполнять функцию изменения карточки питомца и присылать код 200 при попытке отркдактировать чужого питомца.#


# 9
def test_update_photo_exist_pet(pet_photo = 'images\pet2.jpg'):
    '''Проверяем ответ от сервера при попытке изменить фотографию существующего питомца'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        old_photo = my_pets['pets'][0]['pet_photo']
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] != old_photo
    else:
        raise Exception("Список питомцев пуст")

# 10
def test_add_new_pet_simple_valid_data(name = 'shuu', animal_type = 'dog', age = '10'):
    '''Проверяем ответ от сервера при попытке создать питомца без фото'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_without_photo(auth_key, name, animal_type, age,)

    assert status == 200
    assert result['name'] == name




# Тесты из лекции

def test_get_api_key_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

def test_get_list_of_pets(filter = ""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_valid_data(name = 'shu', animal_type = 'dog', age = '10', pet_photo = 'images\pet.png' ):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_delete_exist_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_exist_pet(name = 'buu', animal_type = 'frog', age = '2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

