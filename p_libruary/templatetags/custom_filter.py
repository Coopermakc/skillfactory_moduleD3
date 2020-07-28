from django import template

register = template.Library()


def devide(value):
    return int(value) % 3 == 0


register.filter('devide', devide)