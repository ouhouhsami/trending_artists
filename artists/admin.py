import calendar
import time
from datetime import date

from django.contrib import admin
from django.conf.urls import patterns, url
from django.db.models import Count
from django import forms
from django.conf import settings
from django.forms.models import modelformset_factory
from django.shortcuts import render

import autocomplete_light

from pyechonest import artist
from pyechonest import config

from .models import Artist, Trend, Festival, Concert
from .forms import ArtistBulkInsertByName, FestivalBulkInsertArtistByName

config.ECHO_NEST_API_KEY=settings.ECHONEST_API


class ArtistForm(forms.ModelForm):
    echonest_id = forms.CharField(max_length=30, required=False)
    name = forms.CharField(max_length=255, required=False)

    def clean(self):
        cleaned_data=super(ArtistForm, self).clean()
        if cleaned_data['echonest_id'] != "" and cleaned_data['echonest_id'] != "":
            return cleaned_data
        if cleaned_data['echonest_id'] != "":
            cleaned_data['name'] = artist.Artist(name=cleaned_data['echonest_id']).name
        elif cleaned_data['name'] != "":
            echonest_id = artist.search(name=cleaned_data['name'])[0]
            cleaned_data['echonest_id'] = echonest_id.id
            cleaned_data['name'] = echonest_id.name
        return cleaned_data

    class Meta:
        model = Artist


class ArtistAdmin(admin.ModelAdmin):
    form = ArtistForm

    #list_display = ('name', 'last_familiarity', 'last_hotttnesss', 'festivals' )
    list_display = ('name', 'festivals', 'guest', 'born', 'death' )
    search_fields = ('name', )
    list_filter = ('festival', )
    date_hierarchy = 'born'

    def queryset(self, request):
        # this queryset allow us to filter real festival
        # not hypothetical ones
        festivals = Festival.objects.filter(year__lt=date.today().year + 1)
        artists = Artist.objects.all().extra(select = {
          "festival_count" : """
          SELECT COUNT(*)
          FROM artists_festival
            JOIN artists_festival_artists on artists_festival_artists.festival_id = artists_festival.id
          WHERE artists_festival_artists.artist_id = artists_artist.id
          AND artists_festival_artists.festival_id IN %s
          """ % "(%s)" % ",".join([str(festival.id) for festival in festivals.all()])
        }).order_by("-festival_count",)
        return artists

    def guest(self, obj):
        r = Festival.objects.filter(guest_artists=obj).filter(year__lt=date.today().year + 1)
        return True if r else False

    guest.boolean = True

    def festivals(self, obj):
        return "%s %s" % (obj.festival_count, Festival.objects.filter(artists=obj).filter(year__lt=date.today().year + 1).order_by('year').values_list('year', flat=True))

    festivals.short_description = 'Festivals'
    festivals.admin_order_field = 'festival_count'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        trends = Trend.objects.filter(artist__id=object_id).order_by('timestamp').values_list('timestamp', 'familiarity', 'hotttnesss')
        familiarity = [[calendar.timegm(trend[0].timetuple()) * 1000, trend[1]] for trend in trends]
        hotttnesss = [[calendar.timegm(trend[0].timetuple()) * 1000, trend[2]] for trend in trends]
        extra_context['familiarity'] = familiarity
        extra_context['hotttnesss'] = hotttnesss
        artist_ = Artist.objects.get(id=object_id)
        extra_context['songs'] = artist.Artist(artist_.echonest_id).songs
        return super(ArtistAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def bulk_add(self, request):
        opts = self.model._meta
        app_label = opts.app_label
        ArtistFormSet = modelformset_factory(Artist, form=ArtistForm, extra=20)
        if request.method == "POST":
            formset = ArtistFormSet(request.POST)
            for form in formset.forms:
                if form.is_valid():
                    form.save()
        formset = ArtistFormSet(queryset=Artist.objects.none())
        return render(request, 'admin/artists/artist/bulk_add.html',
                      {'formset': formset, 'app_label': app_label, 'opts':opts},)

    def bulk_add_by_name(self, request):
        opts = self.model._meta
        app_label = opts.app_label
        if request.method == "POST":
            form = ArtistBulkInsertByName(request.POST)
            if form.is_valid():
                artists = form.cleaned_data['artists'].split('\n')
                artists = [artist.strip() for artist in artists]
                for artist_ in artists:
                    print artist_
                    a = ArtistForm({'name':artist_})
                    try:
                        a.save()
                    except:
                        print 'not %s' % artist_
                    time.sleep(4)
                print artists
        form = ArtistBulkInsertByName()
        return render(request, 'admin/artists/artist/bulk_add_by_name.html',
                      {'form': form, 'app_label': app_label, 'opts':opts},)

    def get_urls(self):
        urls = super(ArtistAdmin, self).get_urls()
        extended_urls = patterns('',
            (r'^bulk-add/$', self.admin_site.admin_view(self.bulk_add)),
            (r'^bulk-add-by-name/$', self.admin_site.admin_view(self.bulk_add_by_name))
        )
        return extended_urls + urls

    class Media:
        js = ("flot/jquery.js", "flot/jquery.flot.js", "flot/jquery.flot.time.js")


class ConcertInline(admin.TabularInline):
    model = Concert
    form = autocomplete_light.modelform_factory(Concert)
    extra = 2 # how many rows to show


class FestivalAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Festival)
    list_display = ('__unicode__', 'title')
    list_editable = ('title', )
    inlines = (ConcertInline, )

    def bulk_add(self, request, id):
        opts = self.model._meta
        app_label = opts.app_label
        if request.method == "POST":
            form = ArtistBulkInsertByName(request.POST)
            festival = Festival.objects.get(id=id)
            if form.is_valid():
                artists = form.cleaned_data['artists']
                for _artist in artists.splitlines():
                    a = ArtistForm({'name':_artist.strip()})
                    print a.is_valid()
                    if a.is_valid():
                        _a = a.save()
                    else:
                        echonest = artist.search(name=_artist.strip())[0]
                        _a = Artist.objects.get(echonest_id=echonest.id)
                    if _a not in festival.artists.all():
                        festival.artists.add(_a)
                        try:
                            concert = festival._set.get(artist=_a)
                            #categoryentry = c.categoryentry_set.get(entry = e)
                        except Concert.DoesNotExist:
                            concert = Concert(festival=festival, artist=_a)
                            concert.save()
                            #categoryentry = CategoryEntry(category=c, entry=e)
                            #categoryentry.save()
                    #except ValueError, e:
                    #    print "Unexpected error:", e
                    #    print 'not %s' % _artist
                    time.sleep(1)
        form = FestivalBulkInsertArtistByName()
        return render(request, 'admin/artists/festival/bulk_add.html',
                      {'form': form, 'app_label': app_label, 'opts':opts},)

    def get_urls(self):
        urls = super(FestivalAdmin, self).get_urls()
        extended_urls = patterns('',
            url(r'(\d+)/bulk-add/$', self.admin_site.admin_view(self.bulk_add)),
        )
        return extended_urls + urls


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Trend)
admin.site.register(Festival, FestivalAdmin)
admin.site.register(Concert)
