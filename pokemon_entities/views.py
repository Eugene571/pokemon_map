import folium
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_pokemon_image_url(request, pokemon):
    return request.build_absolute_uri(pokemon.picture.url) if pokemon.picture else DEFAULT_IMAGE_URL


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    local_time = localtime()

    pokemon_entities = PokemonEntity.objects.filter(
        disappear_at__gt=local_time,
        appeared_at__lt=local_time
    )

    for entity in pokemon_entities:
        image_url = get_pokemon_image_url(request, entity.pokemon)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            image_url
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = get_pokemon_image_url(request, pokemon)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    local_time = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = pokemon.entities.filter(
        disappear_at__gt=local_time,
        appeared_at__lt=local_time
    )

    for entity in pokemon_entities:
        image_url = get_pokemon_image_url(request, entity.pokemon)
        add_pokemon(folium_map, entity.lat, entity.lon, image_url)

    pokemon_view = {
        'pokemon_id': pokemon.id,
        'img_url': get_pokemon_image_url(request, pokemon),
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        "description": pokemon.description,
    }

    if pokemon.previous_evolution:
        pokemon_view['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': get_pokemon_image_url(request, pokemon.previous_evolution),
            'title_ru': pokemon.previous_evolution.title_ru,
            'title_en': pokemon.previous_evolution.title_en,
            'title_jp': pokemon.previous_evolution.title_jp
        }

    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        pokemon_view['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'img_url': get_pokemon_image_url(request, next_evolution),
            'title_ru': next_evolution.title_ru
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_view
    })
