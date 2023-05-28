from datetime import datetime

from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession
from django.db import transaction
from django.db.models import QuerySet


def create_order(
        tickets: list[dict],
        username: datetime,
        date: datetime = None
) -> None:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            ticket = Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )
            ticket.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
