import requests
from flask import render_template, request
from app import app


@app.route('/dog-breeds', methods=['GET', 'POST'])
def dog_breeds():
    dog_breeds = []
    is_dog_breeds_with_img = False
    if request.method == 'POST' and 'dog_breeds_option' in request.form:
        option = request.form.get('dog_breeds_option')
        dog_breeds = get_dog_breeds()
        if option == 'breeds_with_image':
            dog_breeds = get_dog_breed_images(dog_breeds[1])
            is_dog_breeds_with_img = True
    return render_template('dog_breeds.html', dog_breeds=dog_breeds, is_dog_breeds_with_img=is_dog_breeds_with_img)


def get_dog_breeds():
    r = requests.get("https://dog.ceo/api/breeds/list/all")
    if not r.ok:
        return 0, []

    dog_breeds = []
    breeds_data = r.json()
    for item in breeds_data['message'].keys():
        dog_breeds.append(item)
    return len(dog_breeds), dog_breeds


def get_dog_breed_images(breeds):
    breeds_data_img = []
    for item in breeds:
        breeds_data_img.append((item, get_dog_breed_image(item)))
    return len(breeds_data_img), breeds_data_img


def get_dog_breed_image(breed):
    r = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
    if not r.ok:
        return 0, []

    breed_data = r.json()
    breed_img = breed_data['message']
    return breed_img
