import django.views.generic

class Home(django.views.generic.TemplateView):
    template_name = "home.html"
home = Home.as_view()


class About(django.views.generic.TemplateView):
    template_name = "about.html"
about = About.as_view()


class Docs(django.views.generic.TemplateView):
    template_name = "docs.html"
docs = Docs.as_view()
