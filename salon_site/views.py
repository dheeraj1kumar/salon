
from django.contrib.auth.views import PasswordResetView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class AjaxPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.txt'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        
        response = super().form_valid(form)
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
           self.request.headers.get('Accept', '').startswith('application/json'):
            return JsonResponse({"success": True})
        return response

    def form_invalid(self, form):
        errors = form.errors.get_json_data()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
           self.request.headers.get('Accept', '').startswith('application/json'):
            
            message = "Please enter a valid email."
            
            try:
                email_errors = errors.get('email', [])
                if email_errors:
                    message = email_errors[0].get('message', message)
            except Exception:
                pass
            return JsonResponse({"success": False, "error": message}, status=400)
        return super().form_invalid(form)
    
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context).strip()
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(body, "text/html") 
        email_message.send()

