from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm
from .models import UserProfile
from checkout.models import Order  
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout



def user_profile(request):
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile:
        messages.error(request, "User profile not found.")
        return redirect('home')  

    order_history = Order.objects.filter(user_profile=user_profile).order_by('-date')

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile:user_profile')
    else:
        user_profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_profile_form': user_profile_form,
        'order_history': order_history,
    }

    return render(request, 'user_profile/user_profile.html', context)


@login_required
def order_info(request, order_id):
    # Get the user's profile
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile:
        messages.error(request, "User profile not found.")
        return redirect('home')

    # Get the order or return a 404 if it doesn't exist
    order = get_object_or_404(Order, id=order_id, user_profile=user_profile)

    context = {
        'order': order,
    }

    return render(request, 'user_profile/order_info.html', context)



# def user_profile(request):
    
#     user_profile = request.user.userprofile
#     order_history = Order.objects.filter(user_profile=user_profile).order_by('-date')  
    
#     if request.method == 'POST':
#         user_profile_form = UserProfileForm(request.POST, instance=user_profile)
#         if user_profile_form.is_valid():
#             user_profile_form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('user_profile:user_profile')  
#     else:
#         user_profile_form = UserProfileForm(instance=user_profile)
    
#     context = {
#         'user_profile_form': user_profile_form,
#         'order_history': order_history,
#     }

#     return render(request, 'user_profile/user_profile.html', context)


@login_required
def get_user_profile_info(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        country_code = user_profile.default_country.code if user_profile.default_country else ""
        
        # Prepare profile data for the response
        profile_data = {
            "first_name": user_profile.default_first_name,
            "last_name": user_profile.default_last_name,
            "email": user_profile.default_email,
            "phone_number": user_profile.default_phone_number,
            "address_1": user_profile.default_address_1,
            "address_2": user_profile.default_address_2,
            "town": user_profile.default_town,
            "county": user_profile.default_county,
            "postcode": user_profile.default_postcode,
            "country": country_code,  # Ensure the country code is an empty string if not set
        }
        return JsonResponse(profile_data)

    except UserProfile.DoesNotExist:
        # Handle case where user profile does not exist
        return JsonResponse({"error": "User profile does not exist."}, status=400)
    except Exception as e:
        # Handle any other unexpected errors
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)
    


@login_required
def delete_user_profile(request):
    try:
        # Get the user object
        user = request.user
        # Delete the user (this will trigger the signal and delete the profile)
        user.delete()

        # Log the user out after deleting
        logout(request)  # Allauth provides the logout functionality

        # Provide feedback that the profile has been deleted
        messages.success(request, "Your profile and account have been deleted successfully.")

        # Redirect to the signup page
        return redirect('account_signup')

    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('account_signup')





