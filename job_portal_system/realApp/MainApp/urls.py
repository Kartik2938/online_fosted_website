from django.urls import path
from . import views

urlpatterns = [
    # General Access
    path('', views.shop, name='shop'),  # Public job listings (Homepage)
    path('dashboard/', views.dashboard, name='dashboard'),  # User dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard

    # Jobs & Applications
    path('jobs/', views.jobs, name='jobs'),  # All jobs page
    path('add-job/', views.add_job, name='add_job'),  # Admin: Add job
    path('manage-orders/', views.manage_orders, name='manage_orders'),  # Admin: Manage applications
    path('place-order/', views.place_order, name='place_order'),  # Apply to saved jobs
    path('orders/', views.order_list, name='order_list'),  # View user's applications
    path('job/<int:job_id>/', views.jobs_detail, name='jobs_detail'),  # Job detail page
    path('category/<slug:category_slug>/', views.category_filter, name='category_filter'),  # Filter by category

    # Saved Jobs (Cart)
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:job_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:job_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Admin - Update Application Status
    path('order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),

    # Authentication
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_view, name='logout'),



    path('employer/jobs/', views.manage_employer_jobs, name='view_employer_jobs'),
    path('user/jobs/', views.view_all_jobs, name='view_all_jobs'),
    path('job/add/', views.add_job, name='add_job'),
    path('job/delete/<int:job_id>/', views.delete_job, name='delete_job'),



    path('job/update/<int:job_id>/', views.update_job, name='update_job'),


    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('dashboard/', views.dashboard, name='dashboard'),


        # ... your other URLs
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('load-more-jobs/', views.load_more_jobs, name='load_more_jobs'),

    path('admin/jobs/', views.admin_job_list, name='admin_job_list'),
    path('admin/jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('admin/jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('admin/users/', views.admin_user_list, name='admin_user_list'),





    path('worksync_profile/', views.worksync_profile, name='worksync_profile'),
]
