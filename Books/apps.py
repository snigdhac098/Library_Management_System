from django.apps import AppConfig



class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Books'

    def ready(self):
        import Books.signals  # ✅ signals.py কে ইমপোর্ট করা হচ্ছে
