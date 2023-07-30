from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from users.models import Subscription


def create_object(request, pk, serializer_in, serializer_out, model):
    '''
    Вспомогательные функции для создания связей
    в моделях Favorite, ShoppingCart, Subscription.
    '''
    user = request.user.id
    obj = get_object_or_404(model, id=pk)

    data_recipe = {'user': user, 'recipe': obj.id}
    data_subscribe = {'user': user, 'author': obj.id}

    if model is Recipe:
        serializer = serializer_in(data=data_recipe)
    else:
        serializer = serializer_in(data=data_subscribe)

    serializer.is_valid(raise_exception=True)
    serializer.save()
    serializer_to_response = serializer_out(obj, context={'request': request})
    return serializer_to_response


def delete_object(request, pk, model_object, model_for_delete_object):
    '''
    Вспомогательные функции для удаления связей
    в моделях Favorite, ShoppingCart, Subscription.
    '''
    user = request.user

    obj_recipe = get_object_or_404(model_object, id=pk)
    obj_subscription = get_object_or_404(model_object, id=pk)

    if model_for_delete_object is Subscription:
        object = get_object_or_404(
            model_for_delete_object, user=user, author=obj_subscription
        )
    else:
        object = get_object_or_404(
            model_for_delete_object, user=user, recipe=obj_recipe
        )
    object.delete()
