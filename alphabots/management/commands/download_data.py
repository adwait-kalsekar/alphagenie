from django.core.management.base import BaseCommand 
from alphabots.utils.data_downloader import download_data

class Command(BaseCommand):
    help = 'Download data from yFinace and save it to the static directory'
  
    def handle(self, *args, **kwargs): 
        try:
            download_data()
            print("Data Downloaded successfully")
        except Exception as e:
            print(f"Failed to download data: {e}")
