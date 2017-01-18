import media, fresh_tomatoes # import library


#  call class Movie from media
Back_to_the_Future = media.Movie("Back to the Future",
                                 "Back to the Future is a 1985 American science fiction adventure comedy film directed by Robert Zemeckis and written by Zemeckis and Bob Gale.",
                                 "https://upload.wikimedia.org/wikipedia/en/thumb/d/d2/Back_to_the_Future.jpg/220px-Back_to_the_Future.jpg",
                                 "https://www.youtube.com/watch?v=qvsgGtivCgs")

Jurassic_Park  = media.Movie("Jurassic Park",
                             "Jurassic Park is a 1993 American science-fiction adventure film directed by Steven Spielberg. The first installment of the Jurassic Park franchise, it is based on the 1990 novel of the same name by Michael Crichton, with a screenplay written by Crichton and David Koepp.",
                             "https://upload.wikimedia.org/wikipedia/en/thumb/e/e7/Jurassic_Park_poster.jpg/220px-Jurassic_Park_poster.jpg",
                             "https://www.youtube.com/watch?v=lc0UehYemQA")

Guardians_of_the_Galaxy = media.Movie("Guardians of the Galaxy",
                                 "Guardians of the Galaxy (retroactively referred to as Guardians of the Galaxy Vol. 1) is a 2014 American superhero film based on the Marvel Comics superhero team of the same name, produced by Marvel Studios and distributed by Walt Disney Studios Motion Pictures.",
                                 "https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/GOTG-poster.jpg/220px-GOTG-poster.jpg",
                                 "https://www.youtube.com/watch?v=B16Bo47KS2g")


movies = [Back_to_the_Future, Jurassic_Park, Guardians_of_the_Galaxy] # create movie list
fresh_tomatoes.open_movies_page(movies) #  call class open_movies_page from fresh_tomatoes