from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Profile, Resource, EmergencyContact,Alert, ResourceRequest, ForumPost, Comment #Post
from .forms import UserRegistrationForm,  ResourceForm, AlertForm, ProfileForm,  ResourceRequestForm, ForumPostForm,  CommentForm,FormComment, EditProfileForm, PasswordChangingForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.views import generic
# from django.contrib.auth.forms import UserCreationForm
# from .forms import CustomUserCreationForm

 
# Create your views here.

class HomeView( LoginRequiredMixin, TemplateView):
    # model = Profile
    template_name = 'App/home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alerts'] = Alert.objects.all()
        context['resources'] = Resource.objects.all()
        
        if self.request.user.is_authenticated:
            try:
                context['profile'] = self.request.user.profile
            except Profile.DoesNotExist:
                context['profile'] = None
        
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class ResourceListView(ListView):
    model = Resource
    template_name = 'App/resource_list.html'
    context_object_name = 'resources'



class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'App/resource_form.html'
    success_url = reverse_lazy('resource_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'App/resource_form.html'
    success_url = reverse_lazy('resource_list')


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = 'App/resource_confirm_delete.html'
    success_url = reverse_lazy('resource_list')


class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'App/resource_detail.html' 
    context_object_name = 'resource'


class EmergencyContactListView(ListView):
    model = EmergencyContact
    template_name = 'App/contact_list.html'
    context_object_name = 'contacts'
    

class ProfileDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Profile
    form_class = ProfileForm
    template_name = 'App/profile_detail.html'
    success_url = reverse_lazy('profile_detail')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Profile updated successfully.")
        return redirect(self.get_success_url())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form) 
        

class AlertListView(ListView):
    model = Alert
    template_name = 'App/alert_list.html'
    content_object_name = 'alerts'

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile-detail', kwargs={'pk': profile.pk}))
        else:
            # Handle form errors or render the form with errors
            context = self.get_context_data(object=profile, form=form)
            return self.render_to_response(context)

    
class AlertCreateView(CreateView):
    model = Alert
    form_class = AlertForm
    template_name = 'App/alert_form.html'
    success_url = reverse_lazy('alert_list')

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class AlertUpdateView(UpdateView):
    model = Alert
    form_class = AlertForm
    template_name = 'App/alert_form.html'
    success_url = reverse_lazy('alert_list')

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)  

        
class LatestAlertsView(ListView):
    model = Alert
    template_name = 'App/latest_alerts.html'  
    context_object_name = 'alerts'

    def get_queryset(self):
        return Alert.objects.order_by('-date_created')[:10] 

   

class AlertDetailView(DetailView):
    model = Alert
    template_name = 'App/alert_detail.html'
    context_object_name = 'alert'

@login_required
def remove_profile_picture(request):
    profile = request.user.profile
    profile.profile_picture.delete()
    profile.save()
    return redirect('profile_detail')


class ResourceRequestCreateView(CreateView):
    model = ResourceRequest
    form_class = ResourceRequestForm
    template_name = 'App/request_resource.html'
    success_url = reverse_lazy('resource_requests')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ResourceRequestListView(LoginRequiredMixin,ListView):
    model = ResourceRequest
    template_name = 'App/resource_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return ResourceRequest.objects.filter(user=self.request.user)

class UseRegisterView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        profile_instance = form.save(commit=False)
        profile_instance.save()
        return super().form_valid(form)


class ForumPostListView(ListView):
    model = ForumPost
    template_name = 'App/forum_post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    form_class = ForumPostForm
   
class ForumPostCreateView(LoginRequiredMixin, CreateView):
    model = ForumPost
    form_class = ForumPostForm
    template_name = 'App/forum_post_create.html'
    success_url = reverse_lazy('forum_post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ForumPostDetailView(DetailView):
    model = ForumPost
    template_name = 'App/forum_post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class AddCommentView(CreateView):
    model = Comment
    form_class = FormComment
    template_name = 'App/add_comment.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']

        return super().form_valid(form)
    success_url = reverse_lazy('home')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    login_url = 'login'
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, "registration/password_change_success.html")



class profile(LoginRequiredMixin, generic.View):
    model = User
    login_url = 'login'
    template_name = "App/profile.html"

    def get(self, request, user_name):
        user_related_data = User.objects.filter(author__username=user_name)[:6]
        user_profile_data = Profile.objects.get(user=request.user.id)
        context = {
            "user_related_data": user_related_data,
            'user_profile_data': user_profile_data
        }
        return render(request, self.template_name, context)



