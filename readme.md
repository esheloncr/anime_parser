This is anime parser integred with Django.
API endpoints: <br>
  /books - Get all books from DB <br>
  /books/id - Get, put, delete a book from DB <br>
  /books/ - POST, create a new book. It takes data with 'title' and 'page_counter' <br>
  /anime - Get random anime from myanimelist.net <br>
  /anime-fact - Get random fact about random anime. <br>
  This was django REST API implementation. <br>
DRF endpoints: <br>
  /api/anime - GET, POST. POST Parameters:
    title: name of anime
    episodes: count of episodes
    rank: rating of anime
    genres: list of genres
    
  /api/genres - GET, POST. POST Parameters:
    genre: genre name
 
 For run service use: docker-compose -f docker-compose-dev.yml up --build (-d for daemon) <br>
 Testing coverage:
 ![](images/coverage.png)
