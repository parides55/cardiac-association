import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import BasketForm, DonationForm, ShippingDetailForm
from .models import Product, Basket, ShippingDetail, Donation

# Create your views here.


def process_payment(amount, orderId):
    url = "https://gateway-test.jcc.com.cy/payment/rest/register.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Convert amount to cents
    amount_in_cents = int(float(amount) * 100)  

    data = {
        "amount": amount_in_cents,
        "currency": "978",  # EUR currency code
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "returnUrl": f"https://pediheart.org.cy/shop/payment_success/{orderId}/",
        "failUrl": f"https://pediheart.org.cy/shop/payment_failed/{orderId}/",
        "description": "Donation to the Cyprus Association of Children with Heart Disease",
        "language": "en",
        "orderNumber": orderId
    }

    try:
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            response_data = response.json()
            if "formUrl" in response_data:
                return response_data["formUrl"]  # Redirect user to JCC payment page
            else:
                raise Exception(f"JCC Error: {response_data.get('errorMessage', 'Unknown error')}")
        else:
            raise Exception(f"JCC API Request Failed: {response.status_code}, {response.text}")
    except Exception as e:
        raise Exception(f"The response from the JCC API failed: {e}")

def payment_success(request, orderId):
    try:
        # Mark order as paid in the database
        shipping_detail = ShippingDetail.objects.get(id=orderId)
        shipping_detail.is_paid = True
        shipping_detail.save()

        # Clear the basket
        Basket.objects.filter(session_key=request.session.session_key).delete()

        messages.success(request, "Thank you for your order! Your payment was successful.")
        return redirect('basket')

    except ShippingDetail.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('basket')


def payment_failed(request, orderId):
    messages.error(request, "Payment failed. Please try again.")
    return redirect('basket')


# Donation views

def donations(request):
    return render(request, "shop/donations.html")


def donation_checkout(request):
    try:
        donation_type = request.GET.get('donation_type')
        donation_amount = request.GET.get('donation_amount')
        other_amount = request.GET.get('other_amount', None)

        if request.method == 'POST':
            # Make a mutable copy of POST data to manipulate it
            post_data = request.POST.copy()
            # If donation_amount is "other", replace it with the actual numeric other_amount
            if post_data.get('donation_amount') == 'other':
                post_data['donation_amount'] = other_amount
                # if not post_data.get('other_amount'):
                #     messages.error(request, "Please enter an amount for your donation.")
                #     return redirect('donation_checkout')

            # Pass the modified data to the form
            donation_form = DonationForm(data=post_data)

            if donation_form.is_valid():
                # Save the donation
                donation = donation_form.save()
                messages.success(request, "Thank you for your donation! We appreciate your support.")
                return redirect('donations')
            else:
                print(donation_form.errors)
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('donation_checkout')

        context = {
            'donation_type': donation_type,
            'donation_amount': donation_amount,
            'other_amount': other_amount,
        }

        return render(request, 'shop/donation_checkout.html', context)

    except Exception as e:
        print(e)
        messages.error(request, f"The following error occurred: {e}")
        return redirect('donations')


# Shop views

def online_shop(request):

    products = Product.objects.filter(available=True).order_by('-created_at')
    basket_form = BasketForm()
    
    context = {
        'products': products,
        'basket_form': basket_form,
    }
    return render(request, "shop/online_shop.html", context)


def add_to_basket(request, product_id):

    try:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        # Get the product
        product = get_object_or_404(Product, id=product_id)
        
        if request.method == 'POST':
            basket_form = BasketForm(data=request.POST)
            if basket_form.is_valid():
                quantity = basket_form.cleaned_data['quantity']
                # Save to the database
                basket_item, created = Basket.objects.get_or_create(
                    session_key=session_key,
                    product=product,
                    defaults={'quantity': quantity}
                )

                if not created:
                    # Update quantity if the product is already in the basket
                    basket_item.quantity += quantity
                    basket_item.save()

                messages.success(
                    request, f"{product.name} has been added to your basket!"
                )
            else:
                messages.error(request, "Something went wrong. Please try again.")

        # Redirect to the basket page
        return redirect('basket')

    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return redirect('online_shop')


def view_basket(request):
    
    try:
        # Ensure session key is set
        session_key = request.session.session_key

        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        # Query basket items for the current session
        basket_items = Basket.objects.filter(session_key=session_key)

        # Calculate the total amount
        total = sum(item.quantity * item.product.price for item in basket_items)

        # Pass the items and total to the template
        context = {
            'basket_items': basket_items,
            'total': total,
        }
        return render(request, 'shop/basket.html', context)

    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return redirect('online_shop')


def remove_from_basket(request, product_id):
    
    try:
        # Ensure session key is set
        session_key = request.session.session_key

        if not session_key:
            request.session.create()
        session_key = request.session.session_key

        # Get the basket item
        basket_item = get_object_or_404(Basket, session_key=session_key, product_id=product_id)

        # Delete the item
        basket_item.delete()

        messages.success(request, f"{basket_item.product.name} has been removed from your basket.")
        return HttpResponseRedirect(reverse('basket'))
    
    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return redirect('basket')


def basket_checkout(request):
    
    try:
        if request.method == "POST":
            shipping_detail_form = ShippingDetailForm(data=request.POST)
            print(request.POST)
            if shipping_detail_form.is_valid():
                shipping_detail = shipping_detail_form.save(commit=False)
                shipping_detail.total_amount = request.POST.get('total')
                shipping_detail.save() # Save the shipping detail first to get the ID

                # Set the many-to-many relationship
                basket_items = Basket.objects.filter(session_key=request.session.session_key)
                shipping_detail.basket_items.set(basket_items)
                shipping_detail.save()  # Save again to update the relationship
                
                # Process payment
                try:
                    payment_url = process_payment(shipping_detail.total_amount, shipping_detail.id)
                    return redirect(payment_url)  # Redirect user to JCC payment page
                except Exception as e:
                    messages.error(request, f"Payment failed: {e}")
                    return redirect('basket')

            else:
                messages.error(request, "Something went wrong. Please fill in your details and try again.")
                return redirect('basket')

    except Exception as e:
        messages.error(request, f"The order was not completed due to the following error occurred: {e}")
        return redirect('basket')