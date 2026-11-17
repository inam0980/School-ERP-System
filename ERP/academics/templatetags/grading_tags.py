from django import template

register = template.Library()

_TIERS = {
    'green':  {'A+', 'A*', 'A'},
    'blue':   {'B+', 'B'},
    'yellow': {'C+', 'C'},
    'orange': {'D', 'E'},
    'red':    {'F', 'U'},
}


@register.filter
def grade_css(label):
    """Badge colour for any scale: American A+…F, British A*…U, French 'x/20'."""
    label = str(label or '')
    colour = 'slate'
    if label.endswith('/20'):
        try:
            mark = float(label[:-3])
            colour = 'green' if mark >= 14 else 'blue' if mark >= 12 else 'yellow' if mark >= 10 else 'red'
        except ValueError:
            pass
    else:
        colour = next((c for c, labels in _TIERS.items() if label in labels), 'slate')
    return f'bg-{colour}-100 text-{colour}-700'
