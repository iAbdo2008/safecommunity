from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView

class PostListView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		posts = Post.objects.all().order_by('-created_on')
		form = PostForm()

		context = {
			'post_list': posts,
			'form': form,
		}

		return render(request, 'Social/post_list.html', context)
	def post(self, request, *args, **kwargs):
		posts = Post.objects.all().order_by('-created_on')
		form = form = PostForm(request.POST, request.FILES) 

		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

		context = {
			'post_list': posts,
			'form': form,
		 } 

		return render(request, 'Social/post_list.html', context)

class PostDetailView(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form  = CommentForm()
		comments =  Comment.objects.filter(post=post).order_by('-created_on')
		context = {

			'post':  post,
			'form':form,
			'comments': comments,
		}

		return render(request, 'Social/post_detail.html', context)
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form  = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.post = post
			new_comment.save()

		comments =  Comment.objects.filter(post=post).order_by('-created_on')
		context = {

			'post':  post,
			'form':form,
			'comments': comments,
		}

		return render(request, 'Social/post_detail.html', context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields  = ['body','image']
	template_name = 'Social/post_edit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('post-detail', kwargs={'pk': pk})

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model  = Post
	template_name =  'Social/post_delete.html'
	success_url = reverse_lazy('post-list')
	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'Social/comment_delete.html'
	success_url = reverse_lazy('post-list')
	comment = model
	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class ProfileView(View):
	def get(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		user = profile.user
		posts = Post.objects.filter(author=user).order_by('-created_on')

		followers = profile.followers.all()

		if len(followers) == 0:
			is_following = False
		for follower in followers:
			if follower == request.user:
				is_following = True
				break
			else:
				is_following = False
		number_of_followers = len(followers)

		context = {
			'user': user,
			'profile': profile,
			'posts': posts,
			'number_of_followers': number_of_followers,
			'is_following': is_following,
		}
		return render(request, 'Social/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = UserProfile
	fields = ['name', 'bio', 'birth_date', 'location', 'picture']
	template_name = 'Social/profile_edit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('profile', kwargs={'pk': pk})

	def test_func(self):
		profile = self.get_object()
		return self.request.user == profile.user


class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		profile.followers.add(request.user)

		return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin,  View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		profile.followers.remove(request.user)

		return redirect('profile', pk=profile.pk)


class AddLike(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)



		is_dislike = False

		for dislike in post.dislikes.all():
			if dislike == request.user:
				is_dislike = True
				break 

		if is_dislike:
			post.dislikes.remove(request.user)
		is_like = False
		for like in post.likes.all():
			if like == request.user:
				is_like = True
				break

		if not is_like:
			post.likes.add(request.user)

		if is_like:
			post.likes.remove(request.user)


		next  = request.POST.get('next', '/')
		return HttpResponseRedirect(next)
class Dislike(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)



		is_like = False
		for like in post.likes.all():
			if like == request.user:
				is_like = True
				break
		if is_like:
			post.likes.remove(request.user)

		is_dislike = False

		for dislike in post.dislikes.all():
			if dislike == request.user:
				is_dislike = True
				break 

		if not is_dislike:
			post.dislikes.add(request.user)

		if is_dislike:
			post.dislikes.remove(request.user)

		next  = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

class UserSearch(View):
	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('query')
		profile_list = UserProfile.objects.filter(
			Q(user__username__icontains=query)
		)

		context = {
			'profile_list': profile_list,
		}
		return render(request, 'Social/search.html', context)


class Love(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)

		is_love = False
		for love in post.loves.all():
			if love == request.user:
				is_love = True
				break

		if not is_love:
			post.loves.add(request.user)

		if is_love:
			post.loves.remove(request.user)


		next  = request.POST.get('next', '/')
		return HttpResponseRedirect(next)
	
	
	
	
	
class FPostListView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		logged_in_user = request.user
		posts = Post.objects.filter(author__profile__followers__in=[logged_in_user.id]).order_by('-created_on')
		form = PostForm()

		context = {
			'fpost_list': posts,
			'form': form,
		}

		return render(request, 'Social/fpost_list.html', context)
	def post(self, request, *args, **kwargs):
		posts = Post.objects.all().order_by('-created_on')
		form = form = PostForm(request.POST, request.FILES) 

		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

		context = {
			'fpost_list': posts,
			'form': form,
		 }

		return render(request, 'Social/fpost_list.html', context)

class FPostDetailView(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form  = CommentForm()
		comments =  Comment.objects.filter(post=post).order_by('-created_on')
		context = {

			'post':  post,
			'form':form,
			'comments': comments,
		}

		return render(request, 'Social/fpost_detail.html', context)
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form  = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.post = post
			new_comment.save()

		comments =  Comment.objects.filter(post=post).order_by('-created_on')
		context = {

			'post':  post,
			'form':form,
			'comments': comments,
		}

		return render(request, 'Social/fpost_detail.html', context)

class FPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields  = ['body','image']
	template_name = 'Social/fpost_edit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('fpost-detail', kwargs={'pk': pk})

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class FPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model  = Post
	template_name =  'Social/fpost_delete.html'
	success_url = reverse_lazy('fpost-list')
	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class FCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'Social/fcomment_delete.html'
	success_url = reverse_lazy('fpost-list')
	comment = model
	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


