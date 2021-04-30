from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "index.htm")

def about(request):
    return render(request, "about.htm")

@login_required(login_url="user:login")
def dashboard(request):
    allarticles = Article.objects.filter(author=request.user)
    context = {
        "allarticles": allarticles
    }
    return render(request, "dashboard.htm", context)

@login_required(login_url="user:login")
def addarticle(request):
    formobj = ArticleForm(request.POST or None, request.FILES or None)
    if formobj.is_valid():
        article = formobj.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarı ile oluşturuldu.")
        return redirect("article:dashboard")
    return render(request, "addarticle.htm", {"form": formobj})

def detail(request, id):
    # article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    return render(request, "detail.htm", {"article":article, "comments":comments})

@login_required(login_url="user:login")
def updatearticle(request, id):
    article = get_object_or_404(Article, id=id)
    formobj = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if formobj.is_valid():
        article = formobj.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarı ile güncellendi.")
        return redirect("article:dashboard")
    return render(request, "update.htm", {"form": formobj})

@login_required(login_url="user:login")
def deletearticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.warning(request, "Makale silindi.")
    return redirect("article:dashboard")

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        allarticles = Article.objects.filter(title__contains=keyword) 
        return render(request, "articles.htm", {"allarticles": allarticles})
    allarticles = Article.objects.all()
    return render(request, "articles.htm", {"allarticles": allarticles})

def addcomment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newcomment = Comment(comment_author=comment_author, comment_content=comment_content)
        newcomment.article = article
        newcomment.save()
    return redirect(reverse("article:detail", kwargs={"id":id}))
