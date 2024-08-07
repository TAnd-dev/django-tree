# django-tree

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/TAnd-dev/django-tree.git
    cd django-tree
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install django
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

### Upload ready data

1. Run the following command to load the prepared data into the database:
   ```bash
    python manage.py loaddata tree.json 
    ```
2. When you open `http://127.0.0.1:8000/` you will see 2 trees

### Admin Interface

1. Open the admin interface at `http://127.0.0.1:8000/admin/` and log in with your superuser account.
2. Add a new `Menu` and `MenuItem` through the admin interface.

### Template Tag

To render a menu on a page, load the custom template tag and use the `draw_menu` tag in your template:

```html
{% load menu_tags %}

{% draw_menu 'main_menu' %}
'''

