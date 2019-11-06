from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from .models import Comment
from posts.models import Post
from .forms import CommentForm


class CreateCommentView(UpdateView):
  queryset = Comment.objects.all()
  form_class = CommentForm
  template_name = 'comments/comment_create.html'

  def get_object(self, *args, **kwargs):
    return get_object_or_404(
      Post,
      pk=self.kwargs.get('id')
    )

  def form_valid(self, form):
    print(form.instance)
    if self.get_object():
      form.instance.post = self.get_object()
      form.instance.owner = self.request.user
      return super().form_valid(form)

  def get_context_data(self, *args, **kwargs):
    context = super(
      CreateCommentView, self
    ).get_context_data(*args, **kwargs)
    context['title'] = 'Comment Create'
    context['post'] = self.get_object()
    return context

  def get_success_url(self, *args, **kwargs):
    messages.success(self.request, 'Comment has been added!')
    return redirect(self.get_object().get_absolute_url())
  
