from django.shortcuts import render,redirect, get_object_or_404
from . forms import Commentform,DepositForm
from  . models import Books,Comment,Borrow,User,Category
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from . constants import DEPOSIT
from django.contrib.auth import logout,login
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from Books.models import UserAccount
import datetime


def send_email_to_user(subject, user, template_name, context={}):
    message = render_to_string(template_name, context)
    send_mail = EmailMultiAlternatives(subject, "", to=[user.email])
    send_mail.attach_alternative(message, 'text/html')
    send_mail.send()






def home(request,brand_slug=None):
    data=Books.objects.all()
    if brand_slug is not None:
         category=Category.objects.get(slug=brand_slug)
         data=Books.objects.filter(category=category)
    category=Category.objects.all()
    return render(request,'home.html',{'data' : data,'category':category})





class Details(DetailView):
    model = Books
    pk_url_kwarg='pk'
    template_name = 'view_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = context['object']
        context['category']=Category()
        post=self.object
        comments=post.comments.all()
        comment_form=Commentform()
        context['comments']=comments
        context['comment_form']=comment_form
        # context['comment_count'] = Comment.objects.filter(
        #     car__id=self.kwargs.get('pk')).count()
        return context
    


    def post(self, request, *args, **kwargs):
        book_id = self.kwargs.get('pk')
        logged_in_user = self.request.user

        books = Books.objects.get(pk=book_id)
        user = User.objects.get(username=logged_in_user)

        order = Borrow(user=user, book=books)
        order.save()

        # books.quentity = books.quentity - 1
        # book.save()

        comment_form=Commentform(data=self.request.POST)
        post=self.get_object()
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()

        return self.get(self.request,*args,**kwargs)
    



# class ProfileView(LoginRequiredMixin, ListView):
#     template_name = 'profile.html'
#     model = Borrow
#     context_object_name = 'borrowed_books'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["user"] = self.request.user
#         context["borrowed_books"] = self.get_queryset()  
#         return context

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = Borrow.objects.filter(
#             user=self.request.user).order_by('timestamp')
#         return queryset

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    model = Borrow
    context_object_name = 'borrowed_books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["borrowed_books"] = self.get_queryset()  

        
        print("User:", self.request.user)
        print("Borrowed Books:", context["borrowed_books"])

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Borrow.objects.filter(
            user=self.request.user
        ).order_by('timestamp')

        
        print("Queryset Data:", queryset)

        return queryset


# class ReturnBorrowedBook(LoginRequiredMixin, View):
#     def post(self, request, slug):
#         book = Books.objects.get(slug=slug)
#         user = self.request.user
#         user_account = user.user_account

#         user_account.balance += book.price
#         user_account.save(update_fields=['balance'])

#         borrowed_book = Borrow.objects.get(user=user, book=book)
#         borrowed_book.status = 'returned'
#         borrowed_book.save(update_fields=['status'])

#         messages.success(self.request, f"{book.name} is returned")
#         send_email_to_user("Returned a book", user, 'return_book_mail.html', {
#             'username': user.username,
#             'bookname': book.name,
#             'price': book.price,
#             'time': datetime.datetime.now()
#         })

#         return redirect("profile")


# class ReturnBorrowedBook(LoginRequiredMixin, View):
#     def post(self, request, slug):
#         book = Books.objects.get(slug=slug)
#         user = self.request.user
#         user_account = user.user_account

#         user_account.balance += book.price
#         user_account.save(update_fields=['balance'])

#         borrowed_book = Borrow.objects.get(user=user, book=book)
#         borrowed_book.status = 'returned'
#         borrowed_book.save(update_fields=['status'])

#         messages.success(self.request, f"{book.name} is returned")
#         send_email_to_user("Returned a book", user, 'return_book_mail.html', {
#             'username': user.username,
#             'bookname': book.name,
#             'price': book.price,
#             'time': datetime.datetime.now()
#         })

#         return redirect("profile")


class ReturnBorrowedBook(LoginRequiredMixin, View):
    def post(self, request, slug):
        print(f"Received slug: {slug}")  # Debugging
        
        book = Books.objects.filter(slug=slug).first()
        if not book:
            messages.error(request, "Book not found.")
            return redirect("profile")  # বা অন্য error handling
        
        user = self.request.user
        user_account = user.user_account

        user_account.balance += book.price
        user_account.save(update_fields=['balance'])

        borrowed_book = Borrow.objects.get(user=user, book=book)
        borrowed_book.status = 'returned'
        borrowed_book.save(update_fields=['status'])

        messages.success(self.request, f"{book.name} is returned")
        send_email_to_user("Returned a book", user, 'return_book_mail.html', {
            'username': user.username,
            'bookname': book.name,
            'price': book.price,
            'time': datetime.datetime.now()
        })

        return redirect("profile")





class Deposite_View(LoginRequiredMixin, FormView, ):
    template_name = 'transaction_form.html'
    success_url = reverse_lazy("homepage")
    form_class = DepositForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Deposit"
        return context

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]

        user = self.request.user
        user_account = user.user_account
        user_account.balance += amount
        user_account.save(update_fields=['balance'])

        messages.success(self.request, f"{amount}tk deposited to your account")
        send_email_to_user("Deposit", user, 'deposit_email.html', {
            'user': user,
            'amount': amount,
            'current_time': datetime.datetime.now()
        })

        return super().form_valid(form)
    



class BorrowBook(LoginRequiredMixin, View):
      
    def post(self, request, slug):
        book = Books.objects.get(slug=slug)
        user = request.user
        user_account = request.user.user_account
        book_price = book.price

        isAvailable = Borrow.objects.filter(
            user=user, book=book).exists()

        if isAvailable:
            messages.success(
                self.request, f"Already borrowed this book!!")
        elif user_account.balance < book_price:
            messages.success(
                self.request, f"not enough balance to borrow this book")
        else:
            user_account.balance -= book_price
            user_account.save(update_fields=['balance'])

            Borrow.objects.create(user=user, book=book)

            messages.success(
                self.request, f"Successfully borrowed this book")
            send_email_to_user("Book borrowed notification", self.request.user, 'borrow_book_email.html', {
                'user': self.request.user,
                'book': book
            })
        return redirect("book_details", slug=slug)