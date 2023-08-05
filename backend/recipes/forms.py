from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet


class NotAllowEmtyForm(BaseInlineFormSet):
    '''
    Класс "NotAllowEmtyForm", проверяет,
    если форма останеется пустой после редактирования
    будет брошено исключение и не позволит сохранить пустой рецепт.
    '''
    def clean(self):
        super(NotAllowEmtyForm, self).clean()

        counter_forms = 0
        counter_true = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            counter_forms += 1
            if data.get('DELETE') is True:
                counter_true += 1

        if counter_forms == counter_true:
            raise ValidationError(
                'Нельзя удалить все ингредиенты или теги из рецепта'
            )
