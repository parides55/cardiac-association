import requests
import uuid
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import BasketForm, DonationForm, ShippingDetailForm
from .models import Product, Basket, ShippingDetail, Donation

# Create your views here.

# JCC API integration for Donations

def process_payment_donation(amount, orderId, description):
    url = "https://gateway-test.jcc.com.cy/payment/rest/register.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Convert amount to cents
    amount_in_cents = int(float(amount) * 100)

    # Append a random 8-character string to the orderId to make it unique
    unique_order_number = f"{orderId}-{uuid.uuid4().hex[:8]}"

    data = {
        "amount": amount_in_cents,
        "currency": "978",  # EUR currency code
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "returnUrl": f"https://pediheart.org.cy/shop/payment_success_donation/{orderId}/",
        "failUrl": f"https://pediheart.org.cy/shop/payment_failed_donation/{orderId}/",
        "description": description,
        "language": "en",
        "orderNumber": unique_order_number
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


def payment_success_donation(request, orderId):
    try:
        donation = Donation.objects.get(id=orderId)
        donation.is_paid = True
        donation.save()
        messages.success(request, f"Thank you for your donation! Your payment was successful.")
        return redirect('donations')

    except Donation.DoesNotExist:
        messages.error(request, "Donation not found.")
        return redirect('donations')

    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return redirect('home')


def payment_failed_donation(request, orderId):
    try:
        donation = Donation.objects.get(id=orderId)
        donation.delete()
        messages.error(request, "Payment failed. Please try again.")
        return redirect('donations')

    except Donation.DoesNotExist:
        messages.error(request, "Donation not found.")
        return redirect('donations')

    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return redirect('home')


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
                # Check the type of donation to set status and save the donation
                donation = donation_form.save(commit=False)
                if donation.donation_type == 'One-Off Payment':
                    donation.status = 'one-off'
                    donation.save()
                else:
                    donation.status = 'active'
                    donation.save()

                # messages.success(request, "Thank you for your donation! We appreciate your support.")
                # return redirect('donations')
                
                description = 'Donation to The Association of Parents and Friends of Children with Heart Disease.'
                # Process payment
                try:
                    payment_url = process_payment_donation(donation.donation_amount, donation.id, description)
                    return redirect(payment_url)  # Redirect user to JCC payment page
                except Exception as e:
                    messages.error(request, f"Payment failed: {e}")
                    return redirect('donation')
            else:
                print(donation_form.errors)
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('donation')

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


# JCC API integration for Shop

def process_payment_shop(amount, orderId, description):
    url = "https://gateway-test.jcc.com.cy/payment/rest/register.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Convert amount to cents
    amount_in_cents = int(float(amount) * 100)

    # Append a random 8-character string to the orderId to make it unique
    unique_order_number = f"{orderId}-{uuid.uuid4().hex[:8]}"

    data = {
        "amount": amount_in_cents,
        "currency": "978",  # EUR currency code
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "returnUrl": f"https://pediheart.org.cy/shop/payment_success_shop/{orderId}/",
        "failUrl": f"https://pediheart.org.cy/shop/payment_failed_shop/{orderId}/",
        "description": description,
        "language": "en",
        "orderNumber": unique_order_number
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


def payment_success_shop(request, orderId):
    try:
        shipping_details = ShippingDetail.objects.get(id=orderId)
        shipping_details.is_paid = True
        shipping_details.save()
        messages.success(request, f"Thank you for your order! Your payment was successful.")
        return redirect('basket')

    except ShippingDetail.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('basket')

    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return redirect('home')


def payment_failed_shop(request, orderId):
    try:
        shipping_details = ShippingDetail.objects.get(id=orderId)
        shipping_details.delete()
        messages.error(request, "Payment failed. Please try again.")
        return redirect('basket')

    except ShippingDetail.DoesNotExist:
        messages.error(request, "Donation not found.")
        return redirect('basket')

    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return redirect('home')

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
                description = "Online purchase from The Association of Parents and Friends of Children with Heart Disease."
                # Process payment
                try:
                    payment_url = process_payment_shop(shipping_detail.total_amount, shipping_detail.id, description)
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