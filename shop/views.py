from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import BasketForm, DonationForm
from .models import Product, Basket

# Create your views here.
def donations(request):
    return render(request, "shop/donations.html")


def donation_checkout(request):
    
    try:
        donation_type = request.GET.get('donation_type')
        donation_amount = request.GET.get('donation_amount')
        other_amount = request.GET.get('other_amount')
        
        if request.method == 'POST':
            donation_form = DonationForm(data=request.POST)
            if donation_form.is_valid():
                full_name = donation_form.cleaned_data['full_name']
                email = donation_form.cleaned_data['email']
                phone_number = donation_form.cleaned_data['phone_number']
                address = donation_form.cleaned_data['address']
                address2 = donation_form.cleaned_data['address2']
                state = donation_form.cleaned_data['state']
                city = donation_form.cleaned_data['city']
                postcode = donation_form.cleaned_data['zip']
                donation_amount = donation_form.cleaned_data['donation_amount']
                donation_type = donation_form.cleaned_data['donation_type']
                other_amount = donation_form.cleaned_data['other_amount']
                donation_form.save()
                
                messages.success(request, "Thank you for your donation! We appreciate your support.")
                
                return redirect('donations')
            
            else:
                print(request.POST)
                print(donation_form.errors)
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('donations')
        
        if donation_amount == 'other':
            donation_amount = other_amount

            context = {
                'donation_type': donation_type,
                'donation_amount': donation_amount,
                'other_amount': other_amount,
            }

            return render(request, 'shop/donation_checkout.html', context)
        
        else:
            context = {
                'donation_type': donation_type,
                'donation_amount': donation_amount,
            }
            return render(request, 'shop/donation_checkout.html', context)
    
    except Exception as e:
        print(request.POST)
        print(e)
        messages.error(request, f"The following error occurred: {e}")
        return redirect('donations')


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
        return redirect('basket')
    
    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return redirect('basket')