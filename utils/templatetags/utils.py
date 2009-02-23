from django.template import Library, Node, loader, TemplateSyntaxError, resolve_variable
from django.template.context import Context

register = Library()

class RenderPartialNode(Node):
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def render(self, context):
        for k,v in self.params.items():
            self.params[k] = resolve_variable(v, context)
        template = loader.get_template(self.name)
        template_context = Context(self.params)
        return template.render(template_context)

@register.tag
def render_partial(parser, token):
    """
        render_partial template tag.
        Two parameters are needed to correctly display the right partial template:
          * controller:controller_name
          * view:view_name
        The final path for the view will be controller/templates/_view_name.html
        Only HTML partial are authorized, until partials into xml templates are totally useless.
    """
    items = token.split_contents()
    if len(items) < 3: raise TemplateSyntaxError('Missing template tag parameters')
    tpl_name = items[1]
    params = {}
    for item in items[2:]:
        k,v = item.split(':')
        params[k] = v
    for k in ['controller', 'view']:
        if k not in params.keys():
            raise TemplateSyntaxError('Parameters "controller" and "view" are required.')
    return RenderPartialNode(tpl_name, params)
