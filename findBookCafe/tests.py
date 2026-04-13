import json

from django.http import Http404
from django.test import RequestFactory, TestCase

from .models import City, Collection, Region, Shop, SimplePage
from .views import (
    cafe,
    cafe_city,
    cafe_region,
    cafes,
    collection,
    collections,
    findTemplate,
    findType,
    index,
    map,
    page404,
    simple_page,
)

QUILL_CONTENT = json.dumps(
    {"delta": {"ops": [{"insert": "test"}]}, "html": "<p>test</p>"}
)


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def make_city(name="Athens", slug="athens"):
    return City.objects.create(name=name, name_en=name, slug=slug)


def make_region(city, name="Syntagma", slug="syntagma"):
    return Region.objects.create(city=city, name=name, name_en=name, slug=slug)


def make_shop(region, name="Test Cafe", slug="test-cafe", shop_type="CAF", **kwargs):
    return Shop.objects.create(
        name=name,
        name_en=name,
        slug=slug,
        type=shop_type,
        latitude=37.97,
        longitude=23.72,
        address="Test St 1",
        region=region,
        isBookShop=True,
        description=QUILL_CONTENT,
        **kwargs,
    )


def make_simple_page(title="About", slug="about"):
    return SimplePage.objects.create(
        title=title,
        slug=slug,
        content=QUILL_CONTENT,
    )


def make_collection(title="Best Cafes", slug="best-cafes"):
    return Collection.objects.create(
        title=title,
        description="A great list",
        slug=slug,
    )


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------


class CityModelTests(TestCase):
    def test_creation(self):
        city = make_city()
        self.assertEqual(city.name, "Athens")
        self.assertEqual(city.slug, "athens")


class RegionModelTests(TestCase):
    def test_creation(self):
        city = make_city()
        region = make_region(city)
        self.assertEqual(region.name, "Syntagma")
        self.assertEqual(region.city, city)


class ShopModelTests(TestCase):
    def setUp(self):
        self.city = make_city()
        self.region = make_region(self.city)

    def test_creation(self):
        shop = make_shop(self.region)
        self.assertEqual(shop.name, "Test Cafe")
        self.assertEqual(shop.type, "CAF")

    def test_str_contains_name(self):
        shop = make_shop(self.region, shop_type="CAF")
        self.assertIn("Test Cafe", str(shop))
        self.assertIn("CAF", str(shop))

    def test_ordering_by_order_position(self):
        shop1 = make_shop(self.region, name="Z Cafe", slug="z-cafe", order_position=2)
        shop2 = make_shop(self.region, name="A Cafe", slug="a-cafe", order_position=1)
        shops = list(Shop.objects.all())
        self.assertEqual(shops[0], shop2)
        self.assertEqual(shops[1], shop1)

    def test_library_type(self):
        lib = make_shop(self.region, name="Test Lib", slug="test-lib", shop_type="LIB")
        self.assertEqual(lib.type, "LIB")


class SimplePageModelTests(TestCase):
    def test_str(self):
        page = make_simple_page()
        self.assertEqual(str(page), "About")

    def test_slug_unique(self):
        make_simple_page(title="About", slug="about")
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            make_simple_page(title="Other", slug="about")


class CollectionModelTests(TestCase):
    def setUp(self):
        self.city = make_city()
        self.region = make_region(self.city)

    def test_str(self):
        col = make_collection()
        self.assertEqual(str(col), "Best Cafes")

    def test_shops_many_to_many(self):
        col = make_collection()
        shop = make_shop(self.region)
        col.shops.add(shop)
        self.assertIn(shop, col.shops.all())

    def test_ordering_by_order_position(self):
        col1 = Collection.objects.create(
            title="Z", description="d", slug="z", order_position=2
        )
        col2 = Collection.objects.create(
            title="A", description="d", slug="a", order_position=1
        )
        cols = list(Collection.objects.all())
        self.assertEqual(cols[0], col2)
        self.assertEqual(cols[1], col1)


# ---------------------------------------------------------------------------
# Helper Function Tests
# ---------------------------------------------------------------------------


class FindTypeTests(TestCase):
    def test_cafes_returns_caf(self):
        self.assertEqual(findType("cafes"), "CAF")

    def test_libraries_returns_lib(self):
        self.assertEqual(findType("libraries"), "LIB")

    def test_unknown_returns_empty_string(self):
        self.assertEqual(findType("other"), "")

    def test_empty_string_returns_empty_string(self):
        self.assertEqual(findType(""), "")


class FindTemplateTests(TestCase):
    def test_cafes_returns_cafes_template(self):
        self.assertEqual(findTemplate("cafes"), "cafes.html")

    def test_libraries_returns_libraries_template(self):
        self.assertEqual(findTemplate("libraries"), "libraries.html")

    def test_unknown_returns_empty_string(self):
        self.assertEqual(findTemplate("other"), "")


# ---------------------------------------------------------------------------
# View Tests
# ---------------------------------------------------------------------------


class FindBookCafeViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.city = make_city()
        self.region = make_region(self.city)
        self.shop = make_shop(self.region, shop_type="CAF")
        self.library = make_shop(
            self.region,
            name="Test Library",
            slug="test-library",
            shop_type="LIB",
        )
        self.simple_pg = make_simple_page()
        self.col = make_collection()
        self.col.shops.add(self.shop)

    # index
    def test_index_returns_200(self):
        request = self.factory.get("/")
        response = index(request)
        self.assertEqual(response.status_code, 200)

    # cafes
    def test_cafes_view_returns_200_for_cafes(self):
        request = self.factory.get("/cafes/")
        response = cafes(request, type="cafes")
        self.assertEqual(response.status_code, 200)

    def test_cafes_view_returns_200_for_libraries(self):
        request = self.factory.get("/libraries/")
        response = cafes(request, type="libraries")
        self.assertEqual(response.status_code, 200)

    def test_cafes_view_raises_404_for_invalid_type(self):
        request = self.factory.get("/invalid/")
        with self.assertRaises(Http404):
            cafes(request, type="invalid")

    # cafe_city
    def test_cafe_city_returns_200(self):
        request = self.factory.get(f"/cafes/{self.city.slug}/")
        response = cafe_city(request, type="cafes", city=self.city.slug)
        self.assertEqual(response.status_code, 200)

    def test_cafe_city_raises_404_for_unknown_city(self):
        request = self.factory.get("/cafes/nowhere/")
        with self.assertRaises(Http404):
            cafe_city(request, type="cafes", city="nowhere")

    # cafe_region
    def test_cafe_region_returns_200(self):
        request = self.factory.get(
            f"/cafes/{self.city.slug}/{self.region.slug}/"
        )
        response = cafe_region(
            request,
            type="cafes",
            city=self.city.slug,
            region=self.region.slug,
        )
        self.assertEqual(response.status_code, 200)

    def test_cafe_region_raises_404_for_unknown_region(self):
        request = self.factory.get(f"/cafes/{self.city.slug}/nowhere/")
        with self.assertRaises(Http404):
            cafe_region(
                request,
                type="cafes",
                city=self.city.slug,
                region="nowhere",
            )

    # cafe detail
    def test_cafe_detail_returns_200(self):
        request = self.factory.get(
            f"/cafes/{self.city.slug}/{self.region.slug}/{self.shop.slug}/"
        )
        response = cafe(
            request,
            type="cafes",
            city=self.city.slug,
            region=self.region.slug,
            cafe=self.shop.slug,
        )
        self.assertEqual(response.status_code, 200)

    def test_cafe_detail_raises_404_for_unknown_cafe(self):
        request = self.factory.get(
            f"/cafes/{self.city.slug}/{self.region.slug}/nowhere/"
        )
        with self.assertRaises(Http404):
            cafe(
                request,
                type="cafes",
                city=self.city.slug,
                region=self.region.slug,
                cafe="nowhere",
            )

    # map
    def test_map_returns_200(self):
        request = self.factory.get("/map/")
        response = map(request)
        self.assertEqual(response.status_code, 200)

    # simple_page
    def test_simple_page_returns_200(self):
        request = self.factory.get("/page/about/")
        response = simple_page(request, page_slug="about")
        self.assertEqual(response.status_code, 200)

    def test_simple_page_raises_404_for_unknown_slug(self):
        request = self.factory.get("/page/nope/")
        with self.assertRaises(Http404):
            simple_page(request, page_slug="nope")

    # collection
    def test_collection_returns_200(self):
        request = self.factory.get("/collections/best-cafes/")
        response = collection(request, page_slug="best-cafes")
        self.assertEqual(response.status_code, 200)

    def test_collection_raises_404_for_unknown_slug(self):
        request = self.factory.get("/collections/nope/")
        with self.assertRaises(Http404):
            collection(request, page_slug="nope")

    # collections list
    def test_collections_returns_200(self):
        request = self.factory.get("/collections/")
        response = collections(request)
        self.assertEqual(response.status_code, 200)

    # page404 handler
    def test_page404_renders_404_template(self):
        request = self.factory.get("/missing/")
        response = page404(request, Exception("not found"))
        self.assertEqual(response.status_code, 200)

    # content assertions
    def test_map_includes_shop_name_in_response(self):
        request = self.factory.get("/map/")
        response = map(request)
        self.assertIn(b"Test Cafe", response.content)

    def test_simple_page_shows_title(self):
        request = self.factory.get("/page/about/")
        response = simple_page(request, page_slug="about")
        self.assertIn(b"About", response.content)

    def test_collection_shows_title(self):
        request = self.factory.get("/collections/best-cafes/")
        response = collection(request, page_slug="best-cafes")
        self.assertIn(b"Best Cafes", response.content)

    # pagination
    def test_cafes_pagination_page_param(self):
        request = self.factory.get("/cafes/?page=1")
        response = cafes(request, type="cafes")
        self.assertEqual(response.status_code, 200)

    def test_cafes_pagination_out_of_range_page(self):
        request = self.factory.get("/cafes/?page=999")
        response = cafes(request, type="cafes")
        self.assertEqual(response.status_code, 200)
