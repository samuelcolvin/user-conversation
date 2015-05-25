from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import TemplateView, DetailView, ListView, FormView

from .models import Conversation, Customer
from .forms import StartConversation


def get_ws_url(request):
    # always import site for reliability
    prefix = 'https://' if request.is_secure() else 'http://'
    ws_url = prefix + request.get_host() + '/ws/'
    return settings.WS_URL or ws_url


class IndexView(ListView):
    template_name = 'index.jinja'
    model = Conversation

    def get_context_data(self, **kwargs):
        kwargs.update(
            title='User Chat'
        )
        return super(IndexView, self).get_context_data(**kwargs)


# index = login_required(IndexView.as_view())
index_view = IndexView.as_view()


class CustomerIndexView(FormView):
    template_name = 'customer_index.jinja'
    form_class = StartConversation

    def get_context_data(self, **kwargs):
        kwargs.update(
            title='User Chat'
        )
        return super(CustomerIndexView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        customer, _ = Customer.objects.get_or_create(name=data['name'], email=data['email'])
        new_con = Conversation.objects.create(customer=customer)
        return redirect('customer-conversation', pk=new_con.id)

# index = login_required(IndexView.as_view())
customer_index_view = CustomerIndexView.as_view()


class OperatorConversationView(DetailView):
    template_name = 'conversation.jinja'
    model = Conversation

    def get_context_data(self, **kwargs):
        kwargs.update(
            title=self.get_object(),
            ws_url=get_ws_url(self.request),
        )
        return super(OperatorConversationView, self).get_context_data(**kwargs)

operator_conversation_view = OperatorConversationView.as_view()

# FIXME
customer_conversation_view = OperatorConversationView.as_view()
