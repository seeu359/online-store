from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Represent of main page
    """

    template_name = 'index.html'
    extra_context = {
        'title': 'Welcome to Store',
    }
