from django.db import models
import requests, hashlib
import _hashlib
import django
from _datetime import datetime

# Create your models here.
class WebSite(models.Model):
    Url = models.URLField(blank=False, null=False)
    Scanned = models.BooleanField(null=False)
    LastScan = models.DateTimeField(null=True, blank=True)
    MD5Sum = models.CharField(max_length=32,null=True, blank=True)
    encoding = models.CharField(max_length=15,null=True, blank=True)
    ContentType = models.CharField(max_length=15,null=True, blank=True)
    
    
    def scan(self):
        site = requests.get(self.Url)
        self.MD5Sum = hashlib.md5(site.text.encode(encoding='utf_8')).hexdigest()
        self.LastScan = datetime.now()
        self.Scanned=True
        self.encoding = site.encoding
        self.ContentType = site.headers["Content-Type"]
        self.save()
        
        
        