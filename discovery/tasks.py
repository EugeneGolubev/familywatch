from celery import shared_task


@shared_task
def sync_tmdb_discovery() -> str:
    # Phase 1 placeholder. Phase 6 will fetch trending/popular/upcoming titles.
    return "tmdb discovery sync placeholder"
