import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    title_product = f'{instance.course}'
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get('id')


def create_stripe_price(summ, stripe_product_id):
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(summ * 100),
        product=stripe_product_id
    )


def create_stripe_session(summ, pk):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        success_url=f'http://127.0.0.1:8000/student/confirm_subscription/{pk}',
        line_items=[{"price": summ.get('id'), "quantity": 1}],
        mode="payment",
        cancel_url='http://127.0.0.1:8000/student/course_list/',
    )
    return session.get('id'), session.get('url')
