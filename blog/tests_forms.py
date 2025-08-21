from django.test import TestCase
from .forms import CommentForm, PostForm


class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        comment_form = CommentForm({'body': 'This is a great post'})
        self.assertTrue(comment_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid(self):
        comment_form = CommentForm({'body': ''})
        self.assertFalse(comment_form.is_valid(), msg='Form is valid')


class TestPostFirm(TestCase):

    def test_form_is_valid(self):
        """Test for the PostForm"""
        post_form = PostForm({
            'title': 'Post Title',
            'customer': 'Naveen',
            'problem_reported': 'test_problem_reported',
            'rectification': 'test_rectification',
            'status': 0
            })
        self.assertTrue(post_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid(self):
        """Test for the PostForm"""
        post_form = PostForm({
            'title': '',
            'customer': '',
            'problem_reported': '',
            'rectification': '',
            'status': 0
            })
        self.assertFalse(post_form.is_valid(), msg='Form is valid')

    def test_title_is_required(self):
        """Test for the 'title' field"""
        form = PostForm({
            'title': '',
            'customer': 'Naveen',
            'problem_reported': 'test_problem_reported',
            'rectification': 'test_rectification',
            'status': 0
        })
        self.assertFalse(
            form.is_valid(),
            msg="Title was not provided, but the form is valid"
        )

    def test_customer_is_required(self):
        """Test for the 'customer' field"""
        form = PostForm({
            'title': 'Post Title',
            'customer': '',
            'problem_reported': 'test_problem_reported',
            'rectification': 'test_rectification',
            'status': 0
        })
        self.assertFalse(
            form.is_valid(),
            msg="Customer Name was not provided, but the form is valid"
        )

    def test_problem_reported_is_required(self):
        """Test for the 'problem_reported' field"""
        form = PostForm({
            'title': 'Post Title',
            'customer': 'Naveen',
            'problem_reported': '',
            'rectification': 'test_rectification',
            'status': 0
        })
        self.assertFalse(
            form.is_valid(),
            msg="Problem Reported was not provided, but the form is valid"
        )

    def test_rectification_is_required(self):
        """Test for the 'rectification' field"""
        form = PostForm({
            'title': 'Post Title',
            'customer': 'Naveen',
            'problem_reported': 'test_problem_reported',
            'rectification': '',
            'status': 0
        })
        self.assertFalse(
            form.is_valid(),
            msg="Rectification was not provided, but the form is valid"
        )
