from django.urls import path
from .views import PostListView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, ProfileView, ProfileEditView, AddFollower, RemoveFollower, AddLike, Dislike, UserSearch, Love, FPostListView, FPostDetailView, FPostEditView, FPostDeleteView, FCommentDeleteView

urlpatterns = [
	path('', PostListView.as_view(), name='post-list'),
	path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
	path('post/edit/<int:pk>', PostEditView.as_view(), name='post-edit'),
	path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
	path('post/<int:post_pk>/comment/delete/<int:pk>', CommentDeleteView.as_view(), name='comment-delete'),
	path('post/<int:pk>/like', AddLike.as_view(), name='like'),
	path('post/<int:pk>/dislike', Dislike.as_view(), name='dislike'),
	path('post/<int:pk>/love', Love.as_view(), name='loves'),
	path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
	path('profile/edit/<int:pk>', ProfileEditView.as_view(), name='profile-edit'),
	path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
	path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
	path('search/', UserSearch.as_view(), name='profile-search'),
	path('fpost', FPostListView.as_view(), name='fpost-list'),
	path('fpost/<int:pk>', FPostDetailView.as_view(), name='fpost-detail'),
	path('fpost/edit/<int:pk>', FPostEditView.as_view(), name='fpost-edit'),
	path('fpost/delete/<int:pk>', FPostDeleteView.as_view(), name='fpost-delete'),
	path('fpost/<int:post_pk>/comment/delete/<int:pk>', CommentDeleteView.as_view(), name='fcomment-delete'),
]
