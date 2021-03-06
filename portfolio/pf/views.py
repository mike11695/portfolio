from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views import generic

from pf.models import Catagory, Blog, Message, User
from pf.forms import BlogForm

# View for the ndex page aka home page
def index(request):
    # Render the HTML template index.html
    return render(request, 'index.html')

#Method to send a email from the contact form
def send_email(request, id=None):
    if request.method == 'POST':
        sender_name = request.POST.get('fullname')
        sender_email = request.POST.get('email')
        email_subject = request.POST.get('subject')
        email_content = request.POST.get('content') + "<br><br> E-mail from " + sender_email

        #Create the email and send it
        try:
            validate_email(sender_email)
            email = EmailMessage(
                email_subject,
                email_content,
                sender_email,
                ['malopez1195@gmail.com'])
            email.content_subtype = "html"

            try:
                email.send()

                #redirect to index page
                return redirect('index')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        except ValidationError:
            return HttpResponse('Invalid e-mail address given')
    else:
        return HttpResponse('Something went wrong!', status=404)

#page for projects that I've finished
def projects(request):
    # Render the HTML template projects.html
    return render(request, 'projects/projects.html')

#page for practice projects and exercises
def practice(request):
    # Render the HTML template practice.html
    return render(request, 'practice/practice.html')

#page for blogs, change to ListView once models and forms are implemented
class BlogListView(generic.ListView):
    model = Blog
    context_object_name = 'blogs'
    template_name = "blogs/blogs.html"
    paginate_by = 5

    #Obtains all created blogs
    def get_queryset(self):
        return Blog.objects.all().order_by('id')

#Form view to create a new blog
@login_required(login_url='/accounts/login/')
def create_blog(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            if form.is_valid():
                created_blog = form.save()

                #add the catagories from the form to image
                clean_catagories = form.cleaned_data.get('catagories')
                for cat in clean_catagories:
                    created_blog.catagories.add(cat)

                #Redirect to blog list view
                return redirect('blogs')
        else:
            form = BlogForm()
        return render(request, 'blogs/create_blog.html', {'form': form})
    else:
        return redirect('index')

#Detailed view for a blog that shows messages related to blog
class BlogDetailView(generic.DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = "blogs/blog.html"

    #Retrieve messages related to blog
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['messages'] = Message.objects.filter(blog=obj)

        return context
