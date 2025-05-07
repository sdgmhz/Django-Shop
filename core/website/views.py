from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import ContactModelForm


class IndexView(TemplateView):
    """View for rendering the homepage."""

    template_name = "website/index.html"


class ContactView(CreateView):
    """View for handling contact form submissions."""

    template_name = "website/contact.html"
    form_class = ContactModelForm
    success_url = reverse_lazy("website:contact")

    def form_valid(self, form):
        """Handles valid form submission and displays a success message."""
        messages.success(self.request, "Ticket submitted successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handles invalid form submission and displays an error message."""
        messages.error(self.request, "Something is wrong")
        return self.render_to_response(self.get_context_data(form=form))


class AboutView(TemplateView):
    """View for rendering the about page."""

    template_name = "website/about.html"
