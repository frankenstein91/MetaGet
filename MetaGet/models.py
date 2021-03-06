from django.db import models
import requests, hashlib
import _hashlib
import django
from _datetime import datetime
from PIL import Image as ImageLib
import PIL.ExifTags, tempfile
from email.policy import default

# Create your models here.
class WebSite(models.Model):
    Url = models.URLField(blank=False, null=False)
    Scanned = models.BooleanField(default=False)
    LastScan = models.DateTimeField(null=True, blank=True)
    MD5Sum = models.CharField(max_length=32,null=True, blank=True)
    encoding = models.CharField(max_length=15,null=True, blank=True)
    ContentType = models.CharField(max_length=15,null=True, blank=True)
    Cookies = models.TextField(null=True, blank=True)
        
    
    def scan(self):
        site = requests.get(self.Url)
        self.MD5Sum = hashlib.md5(site.text.encode(encoding='utf_8')).hexdigest()
        self.LastScan = datetime.now()
        self.Scanned=True
        self.encoding = site.encoding
        self.ContentType = site.headers["Content-Type"]
        if self.ContentType == "image/jpeg":
            #self.Image_set.all().delete()
            ImageTemp = Image(Url=self, Bild = site.content, MD5sum = self.MD5Sum)
            ImageTemp.save()
            ImageTemp.Scan()
        self.Cookies = site.cookies
        self.save()
    
    def __str__(self):
        return self.Url
        


class Image(models.Model):
    Url = models.ForeignKey(WebSite, on_delete=models.CASCADE)
    Bild = models.BinaryField(blank=True, null=True)
    HasEXIF = models.BooleanField(default=False)
    CamModel = models.CharField(max_length=64, blank=True, null=True)
    DateTimeDigitized = models.DateTimeField(blank=True, null=True)
    MD5sum = models.CharField(max_length=32)
    ExifImageHeight = models.IntegerField(null=True, blank=True)
    ExifImageWidth = models.IntegerField(null=True, blank=True)
    
    def Scan(self):
        BildFile = tempfile.NamedTemporaryFile("w+b", suffix="Bild")
        BildFile.write(self.Bild)
        Bild = ImageLib.open(BildFile)
        if Bild._getexif() == None:
            self.HasEXIF = False
        else:
            self.HasEXIF = True
        exif = {PIL.ExifTags.TAGS[k]: v
                for k, v in Bild._getexif().items()
                if k in PIL.ExifTags.TAGS
                }
        self.CamModel = exif["Model"]
        self.DateTimeDigitized = exif["DateTimeDigitized"].replace(":", "-", 2)
        self.ExifImageHeight = int(exif["ExifImageHeight"])
        self.ExifImageWidth = int(exif["ExifImageWidth"])
    
        self.save()
        BildFile.close()
    def __str__(self):
        return "Image - " + self.MD5sum
    