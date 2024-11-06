from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import TemplateDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from django.urls import reverse


APP_NAME = "auctions"


def get_current_user(request):
    return request.user


def is_new_listing(listing):
    return timezone.now() - listing.created_at < timedelta(hours=24)


def is_owner(request, obj, user_field=None):
    current_user = get_current_user(request)
    return current_user == getattr(obj, user_field)


def redirect_to(path_name, args=None):
    if not args:
        return redirect(reverse(f"{APP_NAME}:{path_name}", args=(args)))

    return redirect(reverse(f"{APP_NAME}:{path_name}", args=(args,)))


def render_template(request, template, context=None):
    try:
        template_name = f"{APP_NAME}/{template}.html"
        return render(request, template_name, context)

    except TemplateDoesNotExist:
        raise Http404()


def handle_form_errors(request, template, message):
    return render_template(request, template, {"message": message})


def is_empty(value):
    if value is None:
        return True
    if isinstance(value, (list, dict, set, str)):
        return len(value) == 0
    return False


def paginate_queryset(request, queryset, per_page=1):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(queryset, per_page)

    try:
        paginated_queryset = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Se a página não é um número, exibe a primeira página
        paginated_queryset = paginator.get_page(1)
    except EmptyPage:
        # Se a página está fora do intervalo, exibe a última página
        paginated_queryset = paginator.get_page(paginator.num_pages)

    return [paginated_queryset, per_page]
