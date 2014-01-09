from django.db import models


class Artist(models.Model):
    echonest_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)
    born = models.DateField(blank=True, null=True)
    death = models.DateField(blank=True, null=True)

    def last_familiarity(self):
        try:
            return Trend.objects.filter(artist=self).last().familiarity
        except:
            return None
    last_familiarity.short_description = 'Latest familiarity'
    #last_familiarity.admin_order_field = 'trend__familiarity'

    def last_hotttnesss(self):
        try:
            return Trend.objects.filter(artist=self).last().hotttnesss
        except:
            return None
    last_hotttnesss.short_description = 'Latest hotttnesss'
    #last_hotttnesss.admin_order_field = 'trend__hotttnesss'

    def __unicode__(self):
        return "%s" % (self.name)


class Festival(models.Model):
    year = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    guest_artists = models.ManyToManyField(Artist, related_name="festival_guest")
    artists = models.ManyToManyField(Artist, related_name="festival", through="Concert")
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-year']

    def __unicode__(self):
        return "%s - %s" % (self.year, ', '.join(self.guest_artists.all().values_list('name', flat=True)))


class Concert(models.Model):
    artist = models.ForeignKey(Artist)
    festival = models.ForeignKey(Festival)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table='artists_festival_artists'   #change main_ to your application
        unique_together = (('festival', 'artist'))

    def __unicode__(self):
        return "%s - %s" % (self.artist.name, self.comment)


class Trend(models.Model):
    artist = models.ForeignKey('Artist')
    timestamp = models.DateTimeField(auto_now_add=True)
    familiarity = models.FloatField()
    hotttnesss = models.FloatField()
