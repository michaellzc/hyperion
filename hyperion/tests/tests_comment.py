from django.test import TestCase
from hyperion.models import Comment, UserProfile, Post
from django.contrib.auth.models import User


class CommentTestCase(TestCase):

    def setUp(self):
        pass

    def test_create_comment(self):
        # u2 comments to post created by u1
        u1 = User.objects.create(
            username="c1",
            first_name="c",
            last_name="1"
        ).profile
        u2 = User.objects.create(
            username="c2",
            first_name="c",
            last_name="2"
        ).profile
        p1 = Post.objects.create(
            author=u1,
            title="u1 post",
            content="test content",
        )
        c1 = Comment.objects.create(
            author=u2,
            comment="u2 comment",
            post=p1
        )
        self.assertEquals(c1.comment, "u2 comment")
        self.assertEquals(c1.author, u2)
        self.assertEquals(c1.post, p1)
        self.assertEquals(list(Comment.objects.filter(post=p1)), [c1])
        self.assertEquals(list(Comment.objects.filter(author__display_name="c2")), [c1])
        # how to find the comment from user object

    def test_multi_user_comment_in_same_post(self):
        # multiple user comments in one post
        u1 = User.objects.create(
            username="c1",
            first_name="c",
            last_name="1"
        ).profile
        u2 = User.objects.create(
            username="c2",
            first_name="c",
            last_name="2"
        ).profile
        u3 = User.objects.create(
            username="c3",
            first_name="c",
            last_name="3"
        ).profile
        p1 = Post.objects.create(
            author=u1,
            title="u1 post",
            content="test content",
        )
        c1 = Comment.objects.create(
            author=u1,
            comment="u1 comment",
            post=p1
        )
        c2 = Comment.objects.create(
            author=u2,
            comment="u2 comment",
            post=p1
        )
        c3 = Comment.objects.create(
            author=u3,
            comment="u3 comment",
            post=p1
        )
        self.assertEquals(list(Comment.objects.filter(post=p1)), [c1, c2, c3])

    # TODO: FIND PROBLEM IN DESIGN MODEL COMMENT
    def test_same_user_multi_comments_in_same_post(self):
        u1 = User.objects.create(
            username="c1",
            first_name="c",
            last_name="1"
        ).profile
        u2 = User.objects.create(
            username="c2",
            first_name="c",
            last_name="2"
        ).profile
        p1 = Post.objects.create(
            author=u1,
            title="u1 post",
            content="test content",
        )
        c1 = Comment.objects.create(
            author=u2,
            comment="u2 comment(1)",
            post=p1
        )
        c2 = Comment.objects.create(
            author=u2,
            comment="u2 comment(2)",
            post=p1
        )
        self.assertEquals(list(Comment.objects.filter(post=p1)), [c1, c2])
        self.assertEquals(list(Comment.objects.filter(author__display_name="c2")), [c1, c2])

    # def test_same_user_comment_in_multi_post_by_same_author(self):
    #     u1 = User.objects.create(
    #         username="c1",
    #         first_name="c",
    #         last_name="1"
    #     )
    #     u2 = User.objects.create(
    #         username="c2",
    #         first_name="c",
    #         last_name="2"
    #     )
    #     p1 = Post.objects.create(
    #         author=u1,
    #         title="u1 post",
    #         content="test content",
    #     )
    #     p2 = Post.objects.create(
    #         author=u1,
    #         title="u1 post(2)",
    #         content="test content",
    #     )
    #     c1 = Comment.objects.create(
    #         author=u2,
    #         comment="u2 comment to p1",
    #         post=p1
    #     )
    #     c2 = Comment.objects.create(
    #         author=u2,
    #         comment="u2 comment to p2",
    #         post=p2
    #     )
    #     self.assertEquals(list(Comment.objects.filter(author__username="c2")), [c1, c2])
    #     self.assertEquals(list(Comment.objects.filter(post=p1)), [c1])
    #     self.assertEquals(list(Comment.objects.filter(post=p2)), [c2])

    def test_same_user_comment_in_multi_post_by_different_author(self):
        u1 = User.objects.create(
            username="c1",
            first_name="c",
            last_name="1"
        ).profile
        u2 = User.objects.create(
            username="c2",
            first_name="c",
            last_name="2"
        ).profile
        u3 = User.objects.create(
            username="c3",
            first_name="c",
            last_name="3"
        ).profile
        p1 = Post.objects.create(
            author=u1,
            title="u1 post",
            content="test content",
        )
        p2 = Post.objects.create(
            author=u2,
            title="u2 post",
            content="test content",
        )
        c1 = Comment.objects.create(
            author=u3,
            comment="u3 comment to p1 written by u1",
            post=p1
        )
        c2 = Comment.objects.create(
            author=u3,
            comment="u3 comment to p2 written by u2",
            post=p2
        )
        self.assertEquals(list(Comment.objects.filter(author__display_name="c3")), [c1, c2])

    # def test_multi_user_comment_in_multi_post_by_different_author(self):
    #     pass



