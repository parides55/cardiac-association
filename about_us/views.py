from django.core.paginator import Paginator
from django.db.models import Count, OuterRef, Q, Subquery
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views import generic
from .models import (
    People, Gallery, GalleryImage, GalleryVideo,
    GALLERY_COVER, image_url, video_poster_url,
)

ALBUMS_PER_PAGE = 12
INITIAL_TILES = 24  # tiles shown before the "Load more" button

# Create your views here.

def our_history(request):
    return render(request, "about_us/history.html")


def our_people(request):

    try:
        board_members = People.objects.exclude(position__in=[7, 8]).order_by('position')
        staff = People.objects.filter(position__in=[7, 8]).order_by('position')

        context = {
            'board_members': board_members,
            'staff': staff
        }
        
        return render(request, "about_us/people.html", context) 
    
    except People.DoesNotExist:
        messages.info(request, "No board members or staff found.")
        return render(request, "about_us/people.html")

    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return render(request, "about_us/people.html")


def gallery_view(request):
    """Album overview: one cover card per album, paginated."""
    first_image = (GalleryImage.objects.filter(gallery=OuterRef("pk"))
                    .order_by("order", "uploaded_at", "id").values("image")[:1])
    first_video = (GalleryVideo.objects.filter(gallery=OuterRef("pk"))
                    .order_by("order", "uploaded_at", "id").values("video")[:1])

    galleries = (
        Gallery.objects.select_related("cover_image")
        .annotate(
            image_count=Count("images", distinct=True),
            video_count=Count("videos", distinct=True),
            first_image=Subquery(first_image),
            first_video=Subquery(first_video),
        )
        # An album that has just been created and is still empty stays hidden.
        .filter(Q(image_count__gt=0) | Q(video_count__gt=0))
        .order_by("order", "-created_at", "-id")
    )

    page_obj = Paginator(galleries, ALBUMS_PER_PAGE).get_page(request.GET.get("page"))

    for gallery in page_obj:
        if gallery.cover_image_id:
            gallery.cover_url = image_url(gallery.cover_image.image, **GALLERY_COVER)
        elif gallery.first_image:
            gallery.cover_url = image_url(gallery.first_image, **GALLERY_COVER)
        else:
            gallery.cover_url = video_poster_url(gallery.first_video, **GALLERY_COVER)

    return render(request, "about_us/gallery.html", {"page_obj": page_obj})


def gallery_detail(request, pk):
    """A single album. Only this album's thumbnails are ever requested."""
    gallery = get_object_or_404(Gallery, pk=pk)
    images = list(gallery.images.all())
    context = {
        "gallery": gallery,
        "images": images,
        "image_total": len(images),
        "videos": gallery.videos.all(),
        "initial_tiles": INITIAL_TILES,
    }
    return render(request, "about_us/gallery_detail.html", context)
