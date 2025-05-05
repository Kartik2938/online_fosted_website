from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Job, SavedJobs, JobApplication
from .forms import JobForm
from users.forms import CustomUserCreationForm
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json




def register_user(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_type = request.POST.get('user_type', 'job_seeker')
            company_name = request.POST.get('company_name') if user_type == 'employer' else None

            data = {
                'name': name,
                'email': email,
                'password': password,
                'user_type': user_type,
                'company_name': company_name
            }

            response = requests.post('http://127.0.0.1:5000/api/register', json=data)

            if response.status_code == 201:
                messages.success(request, 'User registered successfully!')
                return redirect('login')
            else:
                error_message = response.json().get('message', 'Registration failed')
                messages.error(request, error_message)
        except requests.exceptions.ConnectionError:
            messages.error(request, 'Could not connect to the registration service')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'register.html')

# Login user via Flask API
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        response = requests.post('http://127.0.0.1:5000/api/login', json={
            'email': email,
            'password': password
        })
        

        try:
            data = response.json()
        except ValueError:
            return render(request, 'login.html', {'error': 'Invalid response from API.'})

        

        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            request.session['access_token'] = token  # Make sure token is saved in session
            request.session['user_type'] = data.get('user_type')
            if data.get('user_type') == 'employer':
                return redirect('view_employer_jobs')
            else:
                return redirect('view_all_jobs')
        else:
            error_message = data.get('message', 'Login failed.')
            return render(request, 'login.html', {'error': error_message})

    return render(request, 'login.html')



# View for employer to see their jobs
def manage_employer_jobs(request):
    token = request.session.get('access_token')

    if not token:
        messages.error(request, 'You must be logged in to manage your jobs.')
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    # Handle job addition
    if request.method == 'POST' and 'add_job' in request.POST:
        job_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'location': request.POST.get('location'),
            'salary': request.POST.get('salary')
        }
        add_response = requests.post('http://127.0.0.1:5000/employer/job', headers=headers, json=job_data)
        if add_response.status_code == 201:
            messages.success(request, 'Job added successfully.')
        else:
            messages.error(request, f"Failed to add job: {add_response.json().get('message', 'Error')}")

    # Handle job update
    elif request.method == 'POST' and 'update_job' in request.POST:
        job_id = request.POST.get('job_id')
        updated_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'location': request.POST.get('location'),
            'salary': request.POST.get('salary')
        }
        update_response = requests.put(f'http://127.0.0.1:5000/employer/job/{job_id}', headers=headers, json=updated_data)
        if update_response.status_code == 200:
            messages.success(request, 'Job updated successfully.')
        else:
            messages.error(request, f"Failed to update job: {update_response.json().get('message', 'Error')}")

    # Handle job deletion
    elif request.method == 'POST' and 'delete_job' in request.POST:
        job_id = request.POST.get('job_id')
        delete_response = requests.delete(f'http://127.0.0.1:5000/employer/job/{job_id}', headers=headers)
        if delete_response.status_code == 200:
            messages.success(request, 'Job deleted successfully.')
        else:
            messages.error(request, f"Failed to delete job: {delete_response.json().get('message', 'Error')}")

    # Fetch updated job list
    try:
        jobs_response = requests.get('http://127.0.0.1:5000/employer/jobs', headers=headers)
        if jobs_response.status_code == 200:
            jobs = jobs_response.json().get('jobs', [])
            return render(request, 'employer_jobs.html', {'jobs': jobs})
        else:
            messages.error(request, jobs_response.json().get('message', 'Could not fetch jobs'))
            return redirect('dashboard')
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Error fetching jobs: {str(e)}')
        return redirect('dashboard')



# View for job seekers to see all available jobs
# View for job seekers to see all available jobs
def view_all_jobs(request):
    token = request.session.get('access_token')

    if not token:
        messages.error(request, 'You must be logged in to view jobs.')
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    try:
        # Update the URL to the correct Flask API endpoint for job seekers
        response = requests.get('http://127.0.0.1:5000/api/all_jobs', headers=headers)

        if response.status_code == 200:
            jobs = response.json().get('jobs', [])
            if jobs:
                return render(request, 'user_jobs.html', {'jobs': jobs})
            else:
                messages.warning(request, 'No jobs available.')
                return render(request, 'user_jobs.html', {'jobs': []})
        else:
            messages.error(request, f"Failed to fetch jobs. API returned status: {response.status_code}. Error: {response.text}")
            return render(request, 'error.html', {'error': 'Failed to fetch jobs from the API.'})
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Error fetching jobs: {str(e)}')
        return render(request, 'error.html', {'error': f'Error fetching jobs: {str(e)}'})



# views.py
@login_required
def update_job(request, job_id):
    # Ensure the user is an employer
    if request.user.user_type == 'job_seeker':
        messages.error(request, 'You must be an employer to update jobs.')
        return redirect('shop')  # Redirect to the home page or any other page
    
    # Change the field from 'id' to 'job_id' in the query
    job = get_object_or_404(Job, job_id=job_id)

    
    if request.method == 'POST':
        # Get the updated job details from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        salary = request.POST.get('salary')

        # Validation
        if not title or not description or not location or not salary:
            messages.error(request, 'All fields are required.')
            return redirect('update_job', job_id=job_id)  # Re-render the form with error message

        # Update the job details
        job.job_title = title
        job.job_description = description
        job.location = location
        job.salary = salary
        job.save()

        messages.success(request, 'Job updated successfully!')
        return redirect('view_employer_jobs')  # Redirect to the list of jobs
    
    return render(request, 'update_job.html', {'job': job})



# Apply to Job

def apply_for_job(request, job_id):
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'You must be logged in to apply for a job.')
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(f'http://127.0.0.1:5000/api/apply/{job_id}', headers=headers)
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Error connecting to API: {str(e)}')
        return redirect('view_all_jobs')

    if response.status_code == 201:
        messages.success(request, 'Application submitted successfully!')
    else:
        error_msg = response.json().get('message', 'Failed to apply for job.')
        messages.error(request, error_msg)

    return redirect('view_all_jobs')

# Add Job (Employer)
def add_job(request):
    if request.method == 'POST':
        token = request.session.get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'title': request.POST['title'],
            'description': request.POST['description'],
            'location': request.POST['location'],
            'salary': request.POST['salary']
        }
        response = requests.post('http://localhost:5000/employer/job', json=data, headers=headers)

        if response.status_code == 201:
            messages.success(request, 'Job posted successfully!')
            return redirect('view_employer_jobs')
        else:
            try:
            # Try to parse the response as JSON
                response_data = response.json()
                messages.error(request, response_data.get('message', 'Failed to add job'))
            except ValueError:
        # If response is not valid JSON, handle the error
                messages.error(request, 'Invalid response from the server. Please try again later.')



# Delete Job (Employer)
def delete_job(request, job_id):
    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f'http://localhost:5000/employer/job/{job_id}', headers=headers)

    if response.status_code == 200:
        messages.success(request, 'Job deleted successfully!')
    else:
        messages.error(request, response.json().get('message', 'Could not delete job'))

    return redirect('view_employer_jobs')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def worksync_profile(request):
    token = request.session.get('access_token')
    if not token:
        messages.error(request, 'You must be logged in to access your profile.')
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get('http://localhost:5000/api/profile', headers=headers)
        if response.status_code == 200:
            user_type = response.json().get('user_type')
            return redirect('manage_employer_jobs' if user_type == 'employer' else 'view_all_jobs')
        else:
            messages.error(request, 'Failed to fetch profile info.')
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Error: {str(e)}')

    return redirect('login')

def dashboard(request):
    return render(request, 'dashboard.html')

# Admin Dashboard - View All Applications
@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    orders = JobApplication.objects.all().order_by('-applied_at')
    return render(request, 'admin_dashboard.html', {'orders': orders})


def jobs_list(request):
    page = request.GET.get("page", 1)
    jobs = Job.objects.all().order_by('-pub_date')
    paginator = Paginator(jobs, 5)  # Adjust per scroll load

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        jobs_page = paginator.get_page(page)
        html = render_to_string('partials/job_cards.html', {'jobs': jobs_page}, request=request)
        return JsonResponse({'html': html})

    jobs_page = paginator.get_page(1)
    return render(request, 'job_listing.html', {'jobs': jobs_page})

# User Dashboard - List All Jobs
@login_required
def dashboard(request):
    jobs = Job.objects.all()
    categories = Job.CATEGORY_CHOICES
    return render(request, 'product.html', {'jobs': jobs, 'category_choices': categories})


# Public Job Listings (Homepage)
def shop(request):
    jobs = Job.objects.all()
    categories = Job.CATEGORY_CHOICES
    return render(request, 'shop.html', {'jobs': jobs, 'category_choices': categories})


# Job Detail Page
def jobs_detail(request, job_id):
    job = get_object_or_404(Job, job_id=job_id)
    return render(request, 'product_detail.html', {'job': job})

def load_more_jobs(request):
    page = request.GET.get("page")
    jobs = Job.objects.all()
    paginator = Paginator(jobs, 10)  # load 10 jobs at a time
    try:
        jobs_page = paginator.page(page)
    except:
        return JsonResponse({'jobs_html': '', 'has_next': False})
    
    return JsonResponse({
        'jobs_html': render_to_string('partials/job_cards.html', {'jobs': jobs_page}),
        'has_next': jobs_page.has_next()
    })

# All Jobs Page
def jobs(request):
    jobs = Job.objects.all()
    return render(request, 'jobs.html', {'jobs': jobs})


# Admin View - Manage All Applications
@login_required
def manage_orders(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can manage applications.")
    
    orders = JobApplication.objects.all().order_by('-applied_at')
    return render(request, 'manage_orders.html', {
        'orders': orders,
        'status_choices': JobApplication.STATUS_CHOICES,
    })







# Save Job to Cart
@login_required
def add_to_cart(request, job_id):
    job = get_object_or_404(Job, job_id=job_id)
    cart, _ = SavedJobs.objects.get_or_create(user=request.user)
    cart.jobs.add(job)
    messages.success(request, f"{job.job_title} added to your saved jobs.")
    return redirect('dashboard')


# View Saved Jobs (Cart)
@login_required
def view_cart(request):
    cart, _ = SavedJobs.objects.get_or_create(user=request.user)
    print(cart.jobs.all())  # Optional: for debug
    return render(request, 'cart.html', {'cart': cart})


# Remove Job from Saved
@login_required
def remove_from_cart(request, job_id):
    cart = get_object_or_404(SavedJobs, user=request.user)
    job = get_object_or_404(Job, job_id=job_id)
    cart.jobs.remove(job)
    messages.success(request, f"{job.job_title} removed from saved jobs.")
    return redirect('view_cart')


# Apply to All Saved Jobs (Cart → Applications)
@login_required
def place_order(request):
    cart = get_object_or_404(SavedJobs, user=request.user)
    if cart.jobs.exists():
        for job in cart.jobs.all():
            JobApplication.objects.get_or_create(user=request.user, job=job)
        cart.jobs.clear()
        messages.success(request, "You have successfully applied to selected jobs!")
        return redirect('order_list')
    else:
        messages.warning(request, "You haven't saved any jobs!")
        return redirect('dashboard')


# User View - My Applications
@login_required
def order_list(request):
    orders = JobApplication.objects.filter(user=request.user).order_by('-applied_at')
    return render(request, 'order_list.html', {'orders': orders})


# Admin Action - Update Application Status
@require_POST
@login_required
def update_order_status(request, order_id):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can update job application status.")
    
    order = get_object_or_404(JobApplication, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(JobApplication.STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, f"Application #{order.id} status updated to {new_status}.")
    else:
        messages.error(request, "Invalid status value.")
    return HttpResponseRedirect(reverse('manage_orders'))


# Filter Jobs by Category
def category_filter(request, category_slug):
    filtered_jobs = Job.objects.filter(category=category_slug)
    categories = Job.CATEGORY_CHOICES
    return render(request, 'category_jobs.html', {
        'jobs': filtered_jobs,
        'category_name': dict(Job.CATEGORY_CHOICES).get(category_slug, category_slug),
        'category_choices': categories,
    })


# List jobs for admin
@login_required
def admin_job_list(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can manage jobs.")
    
    jobs = Job.objects.all().order_by('-pub_date')
    return render(request, 'admin_jobs.html', {'jobs': jobs})


@login_required
def edit_job(request, job_id):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can edit jobs.")

    job = get_object_or_404(Job, job_id=job_id)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"{job.job_title} has been updated.")
            return redirect('admin_job_list')
    else:
        form = JobForm(instance=job)

    return render(request, 'edit_job.html', {'form': form, 'job': job})


@login_required
def delete_job(request, job_id):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can delete jobs.")

    job = get_object_or_404(Job, job_id=job_id)

    if request.method == 'POST':
        job_title = job.job_title
        job.delete()
        messages.success(request, f"{job_title} was deleted successfully.")
        return redirect('admin_job_list')

    return render(request, 'confirm_delete.html', {'job': job})


@login_required
def admin_user_list(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can access this page.")
    
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_user_list.html', {'users': users})