import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.utils import timezone

from .models import Author, BlogPost, Category, Tag
from .views import (
    get_similar_posts,
    index,
    post,
    posts_by_author,
    posts_by_category,
    posts_by_tag,
)


def make_user(username="testuser"):
    return User.objects.create_user(username=username, password="pass")


def make_author(user, name="Test Author", slug="test-author"):
    return Author.objects.create(
        user=user,
        name=name,
        slug=slug,
        bio="A bio.",
        image_url="http://example.com/img.jpg",
    )


def make_category(name="Fiction", slug="fiction"):
    return Category.objects.create(name=name, slug=slug)


def make_tag(name="Python", slug="python"):
    return Tag.objects.create(name=name, slug=slug)


def make_post(author, category=None, slug="test-post", is_published=True, **kwargs):
    return BlogPost.objects.create(
        title="Test Post",
        slug=slug,
        author=author,
        category=category,
        content="<p>Hello</p>",
        is_published=is_published,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------


class AuthorModelTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.author = make_author(self.user)

    def test_str(self):
        self.assertEqual(str(self.author), "Test Author")

    def test_fields(self):
        self.assertEqual(self.author.name, "Test Author")
        self.assertEqual(self.author.slug, "test-author")
        self.assertEqual(self.author.bio, "A bio.")

    def test_optional_fields_blank(self):
        author = Author.objects.create(
            user=make_user("other"),
            name="No Bio",
            slug="no-bio",
        )
        self.assertIsNone(author.bio)
        self.assertIsNone(author.image_url)


class CategoryModelTests(TestCase):
    def test_str(self):
        cat = make_category()
        self.assertEqual(str(cat), "Fiction")

    def test_slug_is_unique(self):
        make_category(name="Fiction", slug="fiction")
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            make_category(name="Fiction 2", slug="fiction")


class TagModelTests(TestCase):
    def test_str(self):
        tag = make_tag()
        self.assertEqual(str(tag), "Python")

    def test_slug_is_unique(self):
        make_tag(name="Python", slug="python")
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            make_tag(name="Python2", slug="python")


class BlogPostModelTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.author = make_author(self.user)
        self.category = make_category()

    def test_str(self):
        p = make_post(self.author, self.category)
        self.assertEqual(str(p), "Test Post")

    def test_published_at_auto_set_on_publish(self):
        p = make_post(self.author, self.category, slug="auto-pub", is_published=True)
        self.assertIsNotNone(p.published_at)

    def test_published_at_not_set_when_unpublished(self):
        p = make_post(
            self.author, self.category, slug="no-pub", is_published=False
        )
        self.assertIsNone(p.published_at)

    def test_published_at_not_overwritten_on_resave(self):
        p = make_post(self.author, self.category, slug="resave", is_published=True)
        original_ts = p.published_at
        p.title = "Updated Title"
        p.save()
        self.assertEqual(p.published_at, original_ts)

    def test_default_ordering_by_published_at_desc(self):
        now = timezone.now()
        p1 = make_post(
            self.author,
            self.category,
            slug="p1",
            published_at=now,
        )
        p2 = make_post(
            self.author,
            self.category,
            slug="p2",
            published_at=now + timezone.timedelta(hours=1),
        )
        posts = list(BlogPost.objects.all())
        self.assertEqual(posts[0], p2)
        self.assertEqual(posts[1], p1)

    def test_tags_many_to_many(self):
        tag = make_tag()
        p = make_post(self.author, self.category, slug="tagged")
        p.tags.add(tag)
        self.assertIn(tag, p.tags.all())

    def test_category_nullable(self):
        p = make_post(self.author, None, slug="no-cat")
        self.assertIsNone(p.category)


# ---------------------------------------------------------------------------
# get_similar_posts Tests
# ---------------------------------------------------------------------------


class GetSimilarPostsTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.author = make_author(self.user)
        self.cat1 = make_category(name="Cat1", slug="cat1")
        self.cat2 = make_category(name="Cat2", slug="cat2")
        self.tag1 = make_tag(name="Tag1", slug="tag1")
        self.tag2 = make_tag(name="Tag2", slug="tag2")

    def test_returns_same_category_posts(self):
        target = make_post(self.author, self.cat1, slug="target")
        p2 = make_post(self.author, self.cat1, slug="same-cat-1")
        p3 = make_post(self.author, self.cat1, slug="same-cat-2")
        p4 = make_post(self.author, self.cat1, slug="same-cat-3")
        similar = get_similar_posts(target)
        similar_ids = [p.id for p in similar]
        for p in [p2, p3, p4]:
            self.assertIn(p.id, similar_ids)
        self.assertNotIn(target.id, similar_ids)

    def test_falls_back_to_tags_when_few_category_posts(self):
        target = make_post(self.author, self.cat1, slug="target-tag")
        target.tags.add(self.tag1)
        tagged = make_post(self.author, self.cat2, slug="tagged-post")
        tagged.tags.add(self.tag1)
        similar = get_similar_posts(target)
        similar_ids = [p.id for p in similar]
        self.assertIn(tagged.id, similar_ids)

    def test_falls_back_to_random_when_few_tagged_posts(self):
        target = make_post(self.author, self.cat1, slug="target-rand")
        other = make_post(self.author, self.cat2, slug="other-rand")
        similar = get_similar_posts(target)
        self.assertNotIn(target, similar)
        self.assertLessEqual(len(similar), 3)

    def test_excludes_target_post(self):
        target = make_post(self.author, self.cat1, slug="target-excl")
        get_similar_posts(target)  # should not raise
        similar = get_similar_posts(target)
        self.assertNotIn(target, similar)

    def test_returns_at_most_three(self):
        target = make_post(self.author, self.cat1, slug="target-limit")
        for i in range(5):
            make_post(self.author, self.cat1, slug=f"extra-{i}")
        similar = get_similar_posts(target)
        self.assertLessEqual(len(similar), 3)


# ---------------------------------------------------------------------------
# View Tests
# ---------------------------------------------------------------------------


class BlogViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = make_user()
        self.author = make_author(self.user)
        self.category = make_category()
        self.tag = make_tag()
        self.post_obj = make_post(
            self.author, self.category, slug="hello-world"
        )
        self.post_obj.tags.add(self.tag)

    def test_index_returns_200(self):
        request = self.factory.get("/")
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_returns_200(self):
        request = self.factory.get("/post/hello-world/")
        response = post(request, post_slug="hello-world")
        self.assertEqual(response.status_code, 200)

    def test_post_detail_returns_404_for_unknown_slug(self):
        from django.http import Http404

        request = self.factory.get("/post/unknown/")
        with self.assertRaises(Http404):
            post(request, post_slug="does-not-exist")

    def test_posts_by_tag_returns_200(self):
        request = self.factory.get("/tag/python/")
        response = posts_by_tag(request, tag_slug="python")
        self.assertEqual(response.status_code, 200)

    def test_posts_by_tag_returns_404_for_unknown(self):
        from django.http import Http404

        request = self.factory.get("/tag/nope/")
        with self.assertRaises(Http404):
            posts_by_tag(request, tag_slug="nope")

    def test_posts_by_author_returns_200(self):
        request = self.factory.get("/author/test-author/")
        response = posts_by_author(request, author_slug="test-author")
        self.assertEqual(response.status_code, 200)

    def test_posts_by_author_returns_404_for_unknown(self):
        from django.http import Http404

        request = self.factory.get("/author/nobody/")
        with self.assertRaises(Http404):
            posts_by_author(request, author_slug="nobody")

    def test_posts_by_category_returns_200(self):
        request = self.factory.get("/category/fiction/")
        response = posts_by_category(request, category_slug="fiction")
        self.assertEqual(response.status_code, 200)

    def test_posts_by_category_returns_404_for_unknown(self):
        from django.http import Http404

        request = self.factory.get("/category/nope/")
        with self.assertRaises(Http404):
            posts_by_category(request, category_slug="nope")

    def test_index_context_contains_posts(self):
        request = self.factory.get("/")
        response = index(request)
        self.assertIn(b"Test Post", response.content)

    def test_posts_by_tag_context_shows_tag_name(self):
        request = self.factory.get("/tag/python/")
        response = posts_by_tag(request, tag_slug="python")
        self.assertIn(b"Python", response.content)

    def test_posts_by_author_context_shows_author_name(self):
        request = self.factory.get("/author/test-author/")
        response = posts_by_author(request, author_slug="test-author")
        self.assertIn(b"Test Author", response.content)
