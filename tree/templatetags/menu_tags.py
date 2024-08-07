from django import template
from django.template.base import TemplateSyntaxError, Node

from tree.models import MenuItem

register = template.Library()


@register.tag
def draw_menu(parser, token):
    try:
        _, menu_name = token.split_contents()
        menu_name = menu_name.strip("'")
    except ValueError:
        raise TemplateSyntaxError("draw_menu tag requires a single argument")
    return MenuNode(menu_name)


class MenuNode(Node):
    def __init__(self, menu_name):
        self.menu_name = menu_name

    def render(self, context):
        request = context['request']
        current_url = context.get('current_url', request.path)
        menu_items = MenuItem.objects.prefetch_related('children').filter(menu__name=self.menu_name)
        active_item, parents = self.get_active_item_and_parents(menu_items, current_url)
        return self.build_menu(menu_items, active_item, parents, current_url)

    def get_active_item_and_parents(self, menu_items, current_url):
        active_item = None
        parents = []
        for item in menu_items:
            if item.get_absolute_url() == current_url:
                active_item = item
                break

        if active_item:
            parent = active_item.parent
            while parent:
                parents.append(parent)
                parent = parent.parent

        return active_item, parents

    def build_menu(self, menu_items, active_item, parents, current_url):
        menu = []
        for item in menu_items:
            if item.parent is None:
                menu.append(self.build_menu_item(item, active_item, parents, current_url))
        return ''.join(menu)

    def build_menu_item(self, item, active_item, parents, current_url):
        url = item.get_absolute_url()
        classes = 'active' if current_url == url else ''
        is_parent = item in parents
        is_active = item == active_item

        expanded = is_active or is_parent

        menu_item = f'<li><a href="{url}" class="{classes}">{item.name}</a>'
        children = item.children.all()

        if children and expanded:
            menu_item += '<ul>'
            for child in children:
                menu_item += self.build_menu_item(child, active_item, parents, current_url)
            menu_item += '</ul>'

        menu_item += '</li>'
        return menu_item
