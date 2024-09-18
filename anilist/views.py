from django.shortcuts import render
import requests 
import datetime
  
def get_data_from_anilist(query, variables=None):
    url = 'https://graphql.anilist.co'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    json_data = {
        'query': query,
        'variables': variables or {}  # Si no hay variables, usar un diccionario vacío
    }
    
    response = requests.post(url, headers=headers, json=json_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# Vista para mostrar la lista de animes
def anime_list(request):
    query = '''
    query {
      Page(page: 1, perPage: 10) {
        media(type: ANIME) {
          id
          title {
            romaji
          }
          description
          episodes
        }
      }
    }
    '''
    anime_data = get_data_from_anilist(query)
    return render(request, 'anime.html', {'anime_data': anime_data['data']['Page']['media']})

# Vista para mostrar la lista de mangas
def manga_list(request):
    query = '''
    query {
      Page(page: 1, perPage: 10) {
        media(type: MANGA) {
          id
          title {
            romaji
          }
          description
          chapters
        }
      }
    }
    '''
    manga_data = get_data_from_anilist(query)
    return render(request, 'manga.html', {'manga_data': manga_data['data']['Page']['media']})

# Vista para mostrar la lista de personajes
def character_list(request):
    query = '''
    query {
      Page(page: 1, perPage: 10) {
        characters {
          id
          name {
            full
          }
        }
      }
    }
    '''
    character_data = get_data_from_anilist(query)
    return render(request, 'personajes.html', {'character_data': character_data['data']['Page']['characters']})

# Vista para mostrar la lista de staff
def staff_list(request):
    query = '''
    query {
      Page(page: 1, perPage: 10) {
        staff {
          id
          name {
            full
          }
        }
      }
    }
    '''
    staff_data = get_data_from_anilist(query)
    return render(request, 'staff.html', {'staff_data': staff_data['data']['Page']['staff']})

def get_featured_animes():
    query = '''
    {
        Page(page: 1, perPage: 12) {
            media(type: ANIME, sort: SCORE_DESC) {
                id
                title {
                    romaji
                }
                coverImage {
                    large
                }
                averageScore
            }
        }
    }
    '''
    anime_data = get_data_from_anilist(query)
    if anime_data:
        print("Datos de animes populares:", anime_data['data']['Page']['media'])
        return anime_data['data']['Page']['media']
    else:
        print("No se obtuvieron datos de animes.")
    return []


def get_featured_mangas():
    query = '''
    {
        Page(page: 1, perPage: 12) {
            media(type: MANGA, sort: SCORE_DESC) {
                id
                title {
                    romaji
                }
                coverImage {
                    large
                }
                averageScore
            }
        }
    }
    '''
    manga_data = get_data_from_anilist(query)
    if manga_data:
        print("Datos de mangas populares:", manga_data['data']['Page']['media'])
        return manga_data['data']['Page']['media']
    else:
        print("No se obtuvieron datos de mangas.")
    return []




# Vista home para mostrar animes y mangas populares
def home(request):
    try:
        featured_animes = get_featured_animes()
        featured_mangas = get_featured_mangas()
                
        # Agrega estos prints para ver si obtienes datos
        print("Animes Populares:", featured_animes)
        print("Mangas Populares:", featured_mangas)

    except Exception as e:
        featured_animes = []
        featured_mangas = []
        print(f"Error: {e}")  # Para saber si ocurre algún error

    context = {
        'featured_animes': featured_animes,
        'featured_mangas': featured_mangas,
    }
    return render(request, 'inicio.html', context)

# Muestra información detallada de los animes
def get_anime_detail(anime_id):
    query = '''
    query ($id: Int) {
      Media(id: $id, type: ANIME) {
        title {
          romaji
        }
        coverImage {
          large
        }
        bannerImage
        description
        format
        episodes
        duration
        status
        startDate {
          year
          month
          day
        }
        endDate {
          year
          month
          day
        }
        season
        averageScore
        popularity
        source
        genres
        studios {
          nodes {
            name
          }
        }
        relations {
          edges {
            relationType(version: 2)
            node {
              id
              title {
                romaji
              }
              coverImage {
                large
              }
            }
          }
        }
        characters {
          edges {
            node {
              id
              name {
                full
              }
              image {
                large
              }
            }
            voiceActors(language: JAPANESE) {
              name {
                full
              }
              image {
                large
              }
            }
          }
        }
        staff {
          edges {
            node {
              id
              name {
                full
              }
              image {
                large
              }
              primaryOccupations
            }
          }
        }
      }
    }
    '''
    
    variables = {'id': anime_id}
    anime_data = get_data_from_anilist(query, variables)
    
    if anime_data:
        anime = anime_data['data']['Media']
        
        # Formatear las fechas de inicio y fin
        anime['formatted_start_date'] = format_date(anime['startDate'])
        anime['formatted_end_date'] = format_date(anime['endDate'])

        return anime

    return None



def format_date(date_obj):
    if date_obj['year'] and date_obj['month'] and date_obj['day']:
        return f"{date_obj['day']:02}/{date_obj['month']:02}/{date_obj['year']}"
    return None





def anime_detail(request, anime_id):
    anime_data = get_anime_detail(anime_id)
    if anime_data:
        return render(request, 'animedetail.html', {'anime': anime_data})
    else:
        return render(request, 'animedetail.html', {'error': 'No se encontró información para este anime.'})


def manga_detail(request, manga_id):
    query = '''
    query ($id: Int) {
        Media(id: $id, type: MANGA) {
            title {
                romaji
            }
            description
            averageScore
            characters {
                edges {
                    node {
                        name {
                            full
                        }
                    }
                }
            }
            staff {
                edges {
                    node {
                        name {
                            full
                        }
                    }
                }
            }
        }
    }
    '''
    variables = {
        'id': manga_id
    }
    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    manga_data = response.json().get('data', {}).get('Media', {})

    return render(request, 'mangadetail.html', {'manga': manga_data})