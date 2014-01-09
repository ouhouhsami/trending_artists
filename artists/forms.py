from django import forms


class ArtistBulkInsertByName(forms.Form):
	artists = forms.CharField(widget=forms.Textarea)


class FestivalBulkInsertArtistByName(forms.Form):
    artists = forms.CharField(widget=forms.Textarea)
