from datetime import datetime
from bar import db



class Drinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink_name=db.Column(db.String(100), nullable=False)
    drink_ingredient=db.Column(db.String(100), nullable=False)
    ingredient_amt=db.Column(db.Integer)
    def __repr__(self):
        return "Drinks('{},{},{}')".format(self.drink_name,self.drink_ingredient,self.ingredient_amt)



class AllIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient=db.Column(db.String(100), nullable=False)
    ingredient_image=db.Column(db.String(20),default='nopic.jpg')
    def __repr__(self):
        return "AllIngredients('{}')".format(self.ingredient)

class Shots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shot_name=db.Column(db.String(100), nullable=False)
    shot_ingredient=db.Column(db.String(100), nullable=False)
    ingredient_amt=db.Column(db.Integer)
    def __repr__(self):
        return "Shots('{},{},{}')".format(self.shot_name,self.shot_ingredient,self.ingredient_amt)

class Pumps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient=db.Column(db.String(100), nullable=False)
    pinout=db.Column(db.Integer)
    flow=db.Column(db.Integer)
    def __repr__(self):
        return "Pumps('{},{},{}')".format(self.ingredient,self.pinout,self.flow)

class MyCabinet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient=db.Column(db.String(100), nullable=False)
    owner=db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return "MyCabinet('{},{}')".format(self.ingredient,self.owner)

class FavoriteDrink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink_ingredient=db.Column(db.String(100), nullable=False)
    ingredient_amt=db.Column(db.Integer)
    owner=db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return "FavoriteDrink('{},{},{}')".format(self.drink_ingredient,self.ingredient_amt,self.owner)

class FavoriteShot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shot_ingredient=db.Column(db.String(100), nullable=False)
    ingredient_amt=db.Column(db.Integer)
    owner=db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return "FavoriteShot('{},{},{}')".format(self.shot_ingredient,self.ingredient_amt,self.owner)



class GameShot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shot_name=db.Column(db.String(100), nullable=False)
    shot_ingredient=db.Column(db.String(100), nullable=False)
    ingredient_amt=db.Column(db.Integer)
    def __repr__(self):
        return "GameShot('{},{},{}')".format(self.shot_name,self.shot_ingredient,self.ingredient_amt)

class PumpCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pump_count=db.Column(db.Integer)
    def __repr__(self):
        return "PumpCount('{}')".format(self.Pump_count)


class DrinkIf(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question=db.Column(db.Text, nullable=False )
	level=db.Column(db.Integer,nullable=False )
        type=db.Column(db.Text, nullable=False )

	def __repr__(self):

	        return "DrinkIf('{},{},{}')".format(self.question,self.level,self.type)

class TruthorShots(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ctitle=db.Column(db.Text, nullable=False)
	font=db.Column(db.Text,nullable=False)
	question=db.Column(db.Text,nullable=False)
	card=db.Column(db.Text, nullable=False)
	pic=db.Column(db.String(20),default='shooter.jpg')

	def __repr__(self):

                return "TruthorShots('{},{},{},{}')".format(self.ctitle,self.font,self.question,self.card,self.pic)

class ShamePics(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	pic=db.Column(db.String(20),default='wimpy1.jpg')

	def __repr__(self):

                return "ShamePics('{}')".format(self.pic)

class RightPics(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        pic=db.Column(db.String(20),default='wimpy1.jpg')

        def __repr__(self):

                return "RightPics('{}')".format(self.pic)

class WrongPics(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        pic=db.Column(db.String(20),default='wimpy1.jpg')

        def __repr__(self):

                return "WrongPics('{}')".format(self.pic)


class Wtw(db.Model):
        id = db.Column(db.Integer, primary_key=True)
	ingredient=db.Column(db.String(100), nullable=False)

        def __repr__(self):

                return "Wtw('{}')".format(self.ingredient)




class Colors(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	color_code=db.Column(db.Text,nullable=False)
	font=db.Column(db.Text,nullable=False)
	
	def __repr__(self):

                return "Colors('{},{}')".format(self.color_code,self.font)


class NeverHave(db.Model):
	id = db.Column(db.Integer, primary_key=True)
        question=db.Column(db.Text, nullable=False )
        level=db.Column(db.Integer,nullable=False )
	type=db.Column(db.Text, nullable=False )


        def __repr__(self):

        	return "NeverHave('{},{},{}')".format(self.question,self.level,self.type)
	
