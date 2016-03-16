# -*- coding: utf-8 -*-

from django import forms

class NewsCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    surename = forms.CharField(required=False)
    email = forms.CharField(required=False)
    site = forms.CharField(required=False)

    def clean(self):
        form_data = self.cleaned_data

        if not "comment" in form_data:
            self._errors["comment"] = "Вы не написали текст комментария"
        elif not form_data["comment"]:
            self._errors["comment"] = "Вы не написали текст комментария"
            del form_data['comment']

        return form_data

class NewsAddForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    surename = forms.CharField(required=False)
    email = forms.CharField(required=False)
    site = forms.CharField(required=False)

    def clean(self):
        form_data = self.cleaned_data

        if not "content" in form_data:
            self._errors["content"] = "Вы не написали текст новости"
        elif not form_data["content"]:
            self._errors["content"] = "Вы не написали текст новости"
            del form_data['content']

        return form_data

