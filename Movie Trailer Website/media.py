import webbrowser #import library

'''This class is used to process information about the film and the opening of the movie trailer in a browser'''

class Movie(): # create class

    def __init__(self,movie_title,movie_storyline, poster_imges, trailer_youtube): # create function

        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_imges
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self): # create function
        webbrowser.open(self.trailer_youtube_url) # use function OPEN from library webbrowser for open trailer on youtube

