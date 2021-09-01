import os
import random
import PIL
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect,request,abort
from bar import app,db
from models import Drinks,AllIngredients,Shots,MyCabinet,FavoriteDrink,PumpCount,Pumps,NeverHave,DrinkIf,TruthorShots,Colors,ShamePics,Wtw,RightPics,WrongPics,FavoriteShot
from forms import (AddDrinkForm,MyCabinetForm,LinkImageForm,AddPumpForm,QuestionForm,CreateCardForm,
		   ShameImageForm,ResponseImageForm)
from functions import *;


def save_cardpicture(form_picture):
    picture_fn = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/barpi', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_responsepicture(form_picture):
    picture_fn = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/barpi', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn


def save_shamepicture(form_picture):
    picture_fn = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/barpi', picture_fn)

    mywidth = 600
    i = Image.open(form_picture)
    wpercent =(mywidth/float(i.size[0]))
    hsize = int((float(i.size[1])*float(wpercent)))
    i =i.resize((mywidth,hsize),PIL.Image.ANTIALIAS)
    i.save(picture_path)

    return picture_fn



def fixdrink(custom):
	making=[]
	cc=PumpCount.query.get(1)
	pumpcount=cc.pump_count
	tz=len(custom)
	for chambr in range(1,pumpcount+1):
		cb=Pumps.query.get(chambr)
		for count in range(0,tz,2):
			#get the image name of the ingredient
			d=AllIngredients.query.filter_by(ingredient=custom[count]).first()
			
			#match it against what's in the pump to get the amount 
			#needed for the drink
			if d.ingredient_image==cb.ingredient:
				#get the pin of the pump
				making.append(cb.pinout)
				#get the time the pump will be running
				amt=float(custom[count+1])
				amount=caltime(amt,cb.flow)
				making.append(amount)
	pour(making)
	return;


@app.route("/pi_instructions")
def pi_instructions():
	return render_template("pi_instructions.html")

@app.route("/makegif")
def makegif():
	return render_template("gif_instructions.html")

@app.route("/voice")
def voice():
	return render_template("vc_instructions.html")




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/makeme')
def makedrink():
	
        options=[]
        options.append('/availabledrinks')
        options.append('static/barpi/availabledrinks.jpg')
        options.append('/lcabinet')
        options.append('/static/barpi/customdrinks.jpg')
        options.append('/whoscabinet')
        options.append('/static/barpi/mic.jpg')
	options.append('/Shotmenu')
        options.append('/static/barpi/ashot.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)


@app.route('/lcabinet')
def lcabinet():
	topics=[]
	t=Pumps.query.all()
	count=0
	for c in t:
		n=AllIngredients.query.filter_by(ingredient_image=c.ingredient).first()
		count=count+1
		topics.append({"image":c.ingredient,"name":n.ingredient,"count":count})

	return render_template('lcabinet.html', topics=topics,title="Liquor Cabinet")

@app.route("/lcabinet2/<ingr>")
def lcabinet2(ingr):
	topics=[]
	t=Pumps.query.all()
	
	for c in t:
		n=AllIngredients.query.filter_by(ingredient_image=c.ingredient).first()
		topics.append({"image":c.ingredient,"name":n.ingredient})

	return render_template('lcabinet2.html', topics=topics,title="Liquor Cabinet-Custom Drink",ingr=ingr)



@app.route('/settings')
def settings():
        options=[]
        options.append('/ckdrinkname')
        options.append('/static/barpi/addrink.jpg')
        options.append('/ckshotname')
        options.append('/static/barpi/addshot.jpg')
        options.append('/loadpump')
        options.append('/static/barpi/loadpump.jpg')
	options.append('/link_image')
        options.append('/static/barpi/link.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)


@app.route("/pumps")
def pumps():
	options=[]
	options.append('/loadpump')
        options.append('/static/barpi/loadpump.jpg')
        options.append('/flushpump')
        options.append('/static/barpi/fpump.jpg')
        options.append('/addpump')
        options.append('/static/barpi/addpump.jpg')
        options.append('/pump/update')
        options.append('/static/barpi/updpump.jpg')
	options.append('/confirmpump')
        options.append('/static/barpi/dpump.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)



@app.route("/summary")
def summary():
		ingredient=[]
		drink_ingredients=[]
		alldrinks=set()
		dr=Drinks.query.all()
		for d in dr:
			alldrinks.add(d.drink_name)
		total=len(alldrinks)	
		ingredients=AllIngredients.query.all()
		for i in ingredients:
			ingredient.append(i.ingredient)
		ingredient.sort()
		for ing in ingredient:
			d=Drinks.query.filter_by(drink_ingredient=ing).all()
			amt=len(d)
			if amt>1:
				drink="drinks"
			else:
				drink="drink"
			drink_ingredients.append({"amount":amt,"ingredient":ing,"drink":drink})

		return render_template('summary.html', drtype='Drinks',profile='profile7',
		ingredients=drink_ingredients,total=total,otherlink='/shot_summary',other='Shot Summary')

@app.route("/autoload",methods=['POST'])
def autoload():
	pumppics=[]
	drinkname = request.form['drinkname']
	c=PumpCount.query.get(1)
        pumpcount=c.pump_count+1
	d=Drinks.query.get(int(drinkname))
	drinkname=d.drink_name
	dr=Drinks.query.filter_by(drink_name=drinkname).all()
	
	
	for d in dr:

		p=AllIngredients.query.filter_by(ingredient=d.drink_ingredient).first()
		pumppics.append(p.ingredient_image)
	ds=len(dr)
	pumpcount=pumpcount-ds+1
	return render_template('autoload.html',loaded='loaded',pumppics=pumppics,pumpcount=pumpcount,drinkname=drinkname)

@app.route("/autoload2",methods=['POST'])
def autoload2():
        pumppics=[]
        shotname = request.form['drinkname']
        c=PumpCount.query.get(1)
        pumpcount=c.pump_count+1
        d=Shots.query.get(int(shotname))
        drinkname=d.shot_name
	
        dr=Shots.query.filter_by(shot_name=drinkname).all()
	for d in dr:

                p=AllIngredients.query.filter_by(ingredient=d.shot_ingredient).first()
                pumppics.append(p.ingredient_image)
	ds=len(dr)
	pumpcount=pumpcount-ds+1
        return render_template('autoload.html',loaded='loaded2',pumppics=pumppics,pumpcount=pumpcount,drinkname=drinkname)

@app.route("/autoload3",methods=['POST'])
def autoload3():
        pumppics=[]
        shotname = request.form['drinkname']
        c=PumpCount.query.get(1)
        pumpcount=c.pump_count+1
        d=Shots.query.get(int(shotname))
        drinkname=d.shot_name
	
        dr=Shots.query.filter_by(shot_name=drinkname).all()
	for d in dr:

                p=AllIngredients.query.filter_by(ingredient=d.shot_ingredient).first()
                pumppics.append(p.ingredient_image)
        return render_template('autoload.html',loaded='loaded3',pumppics=pumppics,pumpcount=pumpcount,
		drinkname=drinkname,gs='yes')




@app.route("/loaded/<drinkname>/<sp>")
def loaded(drinkname,sp):
	dr=Drinks.query.filter_by(drink_name=drinkname).all()
	a=int(sp)
	for d in dr:
		c=Pumps.query.get(a)
		if c is None:
			pass
		else:
			i=AllIngredients.query.filter_by(ingredient=d.drink_ingredient).first()
			c.ingredient=i.ingredient_image
			db.session.commit()
			a=a+1
	flash ("{}'s ingredients are loaded".format(drinkname),"success")
	return redirect(url_for('home'))

@app.route("/loaded2/<drinkname>/<sp>")
def loaded2(drinkname,sp):
        dr=Shots.query.filter_by(shot_name=drinkname).all()
        a=int(sp)
        for d in dr:
                c=Pumps.query.get(a)
                if c is None:
                        pass
                else:
                        i=AllIngredients.query.filter_by(ingredient=d.shot_ingredient).first()
                        c.ingredient=i.ingredient_image
                        db.session.commit()
                        a=a+1
	flash ("{}'s ingredients are loaded".format(drinkname),"success")
        return redirect(url_for('home'))

@app.route("/loaded3/<drinkname>")
def loaded3(drinkname):
        dr=Shots.query.filter_by(shot_name=drinkname).all()
        a=1
        for d in dr:
                c=Pumps.query.get(a)
                if c is None:
                        pass
                else:
			
                        i=AllIngredients.query.filter_by(ingredient=d.shot_ingredient).first()
                        c.ingredient=i.ingredient_image
                        db.session.commit()
                        a=a+1

	gs=GameShot.query.get(1)
	if gs is None:
		for d in dr:

			gs=GameShot(shot_name=drinkname,shot_ingredient=d.shot_ingredient,ingredient_amt=d.ingredient_amt)
			db.session.add(gs)
			db.session.commit()


        flash ("{}'s ingredients are locked and loaded!".format(drinkname),"success")
	flash ("{} is set as Game Shot".format(drinkname),"info")
        return redirect(url_for('games_menu'))





@app.route("/shot_summary")
def shot_summary():
		ingredient=[]
		shot_ingredients=[]
		allshots=set()
		dr=Shots.query.all()
		for d in dr:
			allshots.add(d.shot_name)
		total=len(allshots)	
		ingredients=AllIngredients.query.all()
		for i in ingredients:
			ingredient.append(i.ingredient)
		ingredient.sort()
		for ing in ingredient:
			d=Shots.query.filter_by(shot_ingredient=ing).all()
			amt=len(d)
			if amt>1:
				drink="shots"
			else:
				drink="shot"
			if amt==0:
                            pass
                        else:
                            shot_ingredients.append({"amount":amt,"ingredient":ing,"drink":drink})

		return render_template('summary.html', ingredients=shot_ingredients,drtype="Shots",otherlink='/summary',
		other="Drink Summary",profile='profile8',total=total)


@app.route("/alldrinks")
def alldrinks():
	drinks=set()
	drink=[]
	alldrinks=[]
	c=PumpCount.query.get(1)
	camt=c.pump_count+1
        dr=Drinks.query.all()

        for d in dr:
		drinks.add(d.drink_name)
        total=len(drinks)
	
	for d in drinks:
		dk=Drinks.query.filter_by(drink_name=d).all()
		
		iamt=len(dk)
		
		if iamt<camt:
			drink.append(d)
	drink.sort()
	total=len(drink)
	for d in drink:
		dk=Drinks.query.filter_by(drink_name=d).first()
		alldrinks.append(dk.id)
		alldrinks.append(dk.drink_name)
	tz=len(alldrinks)
	return render_template('alldrinks.html', alldrinks=alldrinks,profile='profile4',
	drtype='Drinks',title='Drink Listing',stype='summary',total=total,tz=tz)

@app.route("/allshots")
def allshots():
        drinks=set()
        alldrinks=[]
	drink=[]
	pump=[]
	c=PumpCount.query.get(1)
	camt=c.pump_count+1
        st=Shots.query.all()
	
        for d in st:
                drinks.add(d.shot_name)
	for s in drinks:
		sk=Shots.query.filter_by(shot_name=s).all()
		iamt=len(sk)
		if iamt<camt:
			drink.append(s)
	drink.sort()
	total=len(drink)
        for s in drink:
		sk=Shots.query.filter_by(shot_name=s).first()
		alldrinks.append(sk.id)
                alldrinks.append(sk.shot_name)
        tz=len(alldrinks)
        return render_template('alldrinks.html', alldrinks=alldrinks, profile='profile5',
	drtype='Shots',title='Shot Listing',stype='shot_summary',total=total,tz=tz)

@app.route("/profile3/<drinkname>")
def profile3(drinkname):
	ingredients=[]
	i=Shots.query.filter_by(shot_name=drinkname).first()
	id=i.id
	dr=Shots.query.filter_by(shot_name=drinkname).all()
	
	for d in dr:
		ingredients.append({"ingredient":d.shot_ingredient,"amount":d.ingredient_amt})
	
	return  render_template("drinkprofile2.html", drinkname=drinkname, drtype='Shot',action='autoload2',ingredients=ingredients,id=id)





@app.route('/profile4/<id>')
def profile4(id):
	ingredients=[]
	d=Drinks.query.get(int(id))
	drinkname=d.drink_name
	dr=Drinks.query.filter_by(drink_name=drinkname).all()

	for d in dr:
		ingredients.append({"ingredient":d.drink_ingredient,"amount":d.ingredient_amt})
	
	return  render_template("drinkprofile2.html", drtype='Drink',action='autoload',drinkname=drinkname, ingredients=ingredients,id=id)

@app.route("/profile5/<id>")
def profile5(id):
	ingredients=[]
	d=Shots.query.get(int(id))
	shotname=d.shot_name
	dr=Shots.query.filter_by(shot_name=shotname).all()
	for d in dr:
		ingredients.append({"ingredient":d.shot_ingredient,"amount":d.ingredient_amt})
	return  render_template("drinkprofile2.html", drinkname=shotname, drtype='Shot',action='autoload2',ingredients=ingredients,id=id)

@app.route("/profile6/<drinkname>")
def profile6(drinkname):
	ingredients=[]
	i=Drinks.query.filter_by(drink_name=drinkname).first()
	id=i.id
	dr=Drinks.query.filter_by(drink_name=drinkname).all()
	
	for d in dr:
		ingredients.append({"ingredient":d.drink_ingredient,"amount":d.ingredient_amt})
	
	return  render_template("drinkprofile2.html", drinkname=drinkname, drtype='Drink',action='autoload',ingredients=ingredients,id=id)



@app.route('/profile7/<ingredient>')
def profile7(ingredient):
	pdrinks=[]
	ing=AllIngredients.query.filter_by(ingredient=ingredient).first()
	pic=ing.ingredient_image
	ingr=Drinks.query.filter_by(drink_ingredient=ingredient).all()
	for i in ingr:
		d="-"+str(i.id)+"-"
		pdrinks.append("-"+i.drink_name)
		pd=Drinks.query.filter_by(drink_name=i.drink_name).all()
		for p in pd:
			pdrinks.append(p.drink_ingredient)
	
	return render_template('profileingredient.html', pdrinks=pdrinks, pic=pic)

@app.route('/profile8/<ingredient>')
def profile8(ingredient):
	pdrinks=[]
	ing=AllIngredients.query.filter_by(ingredient=ingredient).first()
	pic=ing.ingredient_image
	ingr=Shots.query.filter_by(shot_ingredient=ingredient).all()
	for i in ingr:
		d="-"+str(i.id)+"-"
		pdrinks.append("-"+i.shot_name)
		pd=Shots.query.filter_by(shot_name=i.shot_name).all()
		for p in pd:
			pdrinks.append(p.shot_ingredient)
	
	return render_template('profileingredient2.html', pdrinks=pdrinks, pic=pic)

@app.route("/profile9/<id>")
def profile9(id):
	ingredients=[]
	d=Shots.query.get(int(id))
	shotname=d.shot_name
	dr=Shots.query.filter_by(shot_name=shotname).all()
	for d in dr:
		ingredients.append({"ingredient":d.shot_ingredient,"amount":d.ingredient_amt})
	return  render_template("drinkprofile2.html", drinkname=shotname, drtype='Shot',action='autoload3',ingredients=ingredients,id=id)


@app.route("/availabledrinks")
def avdrinks():
	drinks=set()
	drink=[]
	alldrinks=[]
	avdrinks=[]
	pump=[]
	c=PumpCount.query.get(1)
	camt=c.pump_count+1
        dr=Drinks.query.all()

        for d in dr:
		drinks.add(d.drink_name)
        total=len(drinks)
	
	for d in drinks:
		dk=Drinks.query.filter_by(drink_name=d).all()
		
		iamt=len(dk)
		
		if iamt<camt:
			drink.append(d)
	drink.sort()
	for d in drink:
		dk=Drinks.query.filter_by(drink_name=d).first()
		alldrinks.append(dk.drink_name)
	#convert pump images to ingredient names then putting into a list
	for count in range(1,camt):
		a=Pumps.query.get(count)
		ai=AllIngredients.query.filter_by(ingredient_image=a.ingredient).first()
		pump.append(ai.ingredient)
	for av in alldrinks:
		ck=Drinks.query.filter_by(drink_name=av).all()
		ti=len(ck)
		avck=[]
		for c in ck:
			for p in pump:
				if p==c.drink_ingredient:
					avck.append("yes!")
	
		ack=len(avck)
		if ack==ti:
			avdrinks.append(av)
		tz=len(avdrinks)
	return render_template("avdrinks.html",drtype='Drinks',profile='profile',avdrinks=avdrinks,tz=tz)


@app.route("/profile/<drinkname>")
def profile(drinkname):
	ingredients=[]
	dk=Drinks.query.filter_by(drink_name=drinkname).first()
	id=dk.id
	dr=Drinks.query.filter_by(drink_name=drinkname).all()
	for d in dr:
		ingredients.append(d.drink_ingredient+"  "+str(d.ingredient_amt))
		

	return render_template("drinkprofile.html",ingredients=ingredients,drinkname=drinkname,id=id)

@app.route("/sprofile/<drinkname>")
def sprofile(drinkname):
	ingredients=[]
	dk=Shots.query.filter_by(shot_name=drinkname).first()
	id=dk.id
	dr=Shots.query.filter_by(shot_name=drinkname).all()
	for d in dr:
		ingredients.append(d.shot_ingredient+"  "+str(d.ingredient_amt))
	
	return render_template("shotprofile.html",ingredients=ingredients,drinkname=drinkname,id=id,typ='single',shot_amt=1,ep='home')


@app.route("/loadpump")
def loadpump():
	ingredients=[]
	ingredient=[]
	lc=AllIngredients.query.all()
	for l in lc:
		ingredient.append(l.ingredient)
	ingredient.sort()
	for ingr in ingredient:
		i=AllIngredients.query.filter_by(ingredient=ingr).first()
	
		ingredients.append(i.id)
		ingredients.append(i.ingredient)
	tz=len(ingredients)
	return render_template('pump_search.html', ingredients=ingredients,tz=tz,title="Load Pump")


@app.route("/loadpump/<ing>")
def pumpload(ing):
	lc=AllIngredients.query.get(ing)
	ingredient=lc.ingredient
	return render_template('pump_choices.html',ingredient=ingredient)


@app.route("/savepump/<ingredient>",methods= ['GET' , 'POST'])
def savepump(ingredient):
	if request.method=='GET':
		cc=PumpCount.query.get(1)
		pumpcount=cc.pump_count+1
		ch=Pumps.query.all()
		pumppics=[]
		for c in ch:
			pumppics.append(c.ingredient)
		ing=AllIngredients.query.filter_by(ingredient=ingredient).first()
		new=ing.ingredient_image

		return render_template('savepump.html',pumpcount=pumpcount,pumppics=pumppics,new=new)
	elif request.method == 'POST':
		chambr = request.form.getlist('Pump')
		pumpno=chambr[0]
		lc=AllIngredients.query.filter_by(ingredient=ingredient).first()
		k=Pumps.query.get(pumpno)
		old=AllIngredients.query.filter_by(ingredient_image=k.ingredient).first()
		old=old.ingredient
		new=lc.ingredient
		k.ingredient=lc.ingredient_image
		db.session.commit()
		flash('Pump {} has been changed from {} to {}'.format(pumpno,old,new),'success')

		return redirect(url_for('home'))

@app.route("/pump/testflow/<pump>/addpin",methods=['GET','POST'])
def ckaddpin(pump):
	if request.method=='GET':
		return render_template("enterinfo.html",itype='number',stype='Pin',ftype='pin')
	elif request.method=='POST':
		pin=request.form['pin']
		print pin
		return redirect(url_for('testflow',flow=0,pump=pump,pin=pin))
@app.route("/pump/testflow/<pump>/<pin>/<flow>",methods=['GET','POST'])
def testflow(pump,pin,flow):
	if request.method=='GET':
		
		return render_template("testflow.html",flow=flow,pump=pump,pin=pin)
	if request.method=='POST':
		nflow=request.form['flow'] 
		flow=int(flow)+int(nflow) 
		
		making=[pin,float(nflow)]
		pour(making)
		return redirect(url_for('testflow',pump=pump,flow=flow,pin=pin))


@app.route("/pump/testflow/save/<pump>/<flow>")
def testflowsave(pump,flow):
	np=Pumps.query.get(pump)
	if np is None:
		return redirect(url_for('addpump',flow=flow))
	oldrate=np.flow
	nflow=float(flow)*.10
	np.flow=nflow
	db.session.commit()
	
	flash("pump {}'s  flowrate has been changed form {} to {}".format(pump,oldrate,np.flow),"warning")
	return redirect(url_for('home'))


@app.route("/allpics")
def allpics():
	pics=[]
	pic=AllIngredients.query.all()
	for p in pic:
		pics.append({"name":p.ingredient,"image":p.ingredient_image})
	pics.sort()
	return render_template("allpics.html",pics=pics)



@app.route("/ckdrinkname",methods=['GET','POST'])
def ckdrink():
	if request.method=='GET':
		return render_template("enterinfo.html",itype='text',stype='Drink name',ftype='drink')
	elif request.method=='POST':
		drink=request.form['drink']
		ck=Drinks.query.filter_by(drink_name=drink).first()
		if ck is None:
			return redirect(url_for('add_drink',drink=drink))
		flash('{} is already in the database'.format(drink),'danger')
		return redirect(url_for('home'))




@app.route("/add_drink/<drink>", methods=['GET', 'POST'])
def add_drink(drink):
	form=AddDrinkForm()
	if form.validate_on_submit():

		FI=request.form.getlist('ingredients')
		dingr=FI[0]
		if dingr=='0':
			ingrd=request.form['ingredient']
			image='nopic.gif'
			newingr=AllIngredients(ingredient=ingrd,ingredient_image=image)
			db.session.add(newingr)
			db.session.commit()
			#get the last ingredient entered to put into drink ingredient
			di=AllIngredients.query.filter_by(ingredient=ingrd).first()
			dingr=di.id

		drk=AllIngredients.query.get(int(dingr))
		amount=float(form.ingredient_amt.data)
		new=Drinks(drink_name=drink,drink_ingredient=drk.ingredient,ingredient_amt=amount)
		db.session.add(new)
		db.session.commit()
		if form.addmore.data==True:
			flash('{} has been added to {}'.format(drk.ingredient,drink), 'success')
			return redirect(url_for('add_drink',drink=drink))
		if form.update.data==True:
			u=Drinks.query.filter_by(drink_name=drink).first()
			return redirect(url_for('drinkupdate',id=u.id))
		flash("{} has been added to the Library".format(drink),"success")
		return redirect(url_for('home'))

	dingredients=[]
	ingredient=[]
	ingredients=[]
	newdrink=Drinks.query.filter_by(drink_name=drink).all()
	for d in newdrink:
		dingredients.append(d.drink_ingredient)
		dingredients.append(d.ingredient_amt)
	tz=len(dingredients)

	ti=AllIngredients.query.all()
	for i in ti:
		ingredient.append(i.ingredient)
	ingredient.sort()
	for ingr in ingredient:
		i=AllIngredients.query.filter_by(ingredient=ingr).first()
		ingredients.append(i.id)
		ingredients.append(i.ingredient)
	
	ingredients.append("0")
	ingredients.append("other")
	tsize=len(ingredients)
	

	return render_template("add_drink.html",ingredients=ingredients,form=form,drink=drink,dingredients=dingredients,tsize=tsize,tz=tz)


@app.route("/ckshotname",methods=['GET','POST'])
def ckshot():
	if request.method=='GET':
		return render_template("enterinfo.html",itype='text',stype='Shot name',ftype='drink')
	elif request.method=='POST':
		drink=request.form['drink']
		ck=Shots.query.filter_by(shot_name=drink).first()
		if ck is None:
			return redirect(url_for('add_shot',drink=drink))
		flash('{} is already in the database'.format(drink),'danger')
		return redirect(url_for('home'))


@app.route("/add_shot/<drink>", methods=['GET', 'POST'])
def add_shot(drink):
	form=AddDrinkForm()
	if form.validate_on_submit():
		
		FI=request.form.getlist('ingredients')
		dingr=FI[0]
		if dingr=='0':
			ingrd=request.form['ingredient']
			image='nopic.gif'
			newingr=AllIngredients(ingredient=ingrd,ingredient_image=image)
			db.session.add(newingr)
			db.session.commit()
			di=AllIngredients.query.count()
			dingr=str(di)
			
		drk=AllIngredients.query.get(int(dingr))
		amount=float(form.ingredient_amt.data)
		new=Shots(shot_name=drink,shot_ingredient=drk.ingredient,ingredient_amt=amount)
		db.session.add(new)
		db.session.commit()
		if form.addmore.data==True:
			flash('{} shot has been added to the list'.format(drink), 'success')
			return redirect(url_for('add_shot',drink=drink))
		if form.update.data==True:
			u=Shots.query.filter_by(shot_name=drink).first()
			return redirect(url_for('shotupdate',id=u.id))
		flash("{} has been added to the Library".format(drink),"success")
		return redirect(url_for('home'))

	dingredients=[]
	ingredient=[]
	ingredients=[]
	newshot=Shots.query.filter_by(shot_name=drink).all()
	for d in newshot:
		dingredients.append(d.shot_ingredient)
		dingredients.append(d.ingredient_amt)
	tz=len(dingredients)

	ti=AllIngredients.query.all()
	for i in ti:
		ingredient.append(i.ingredient)
	ingredient.sort()
	for ingr in ingredient:
		i=AllIngredients.query.filter_by(ingredient=ingr).first()
		ingredients.append(i.id)
		ingredients.append(i.ingredient)
	
	ingredients.append("0")
	ingredients.append("other")
	tsize=len(ingredients)
	

	return render_template("add_drink.html",ingredients=ingredients,form=form,drink=drink,dingredients=dingredients,tsize=tsize,tz=tz)







@app.route("/Shotmenu")
def shotmenu():
	options=[]
        options.append('/setshaker')
        options.append('static/barpi/afew.jpg')
        options.append('/setshots')
        options.append('/static/barpi/orjust1.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)


@app.route("/setshots")
def avshots():
	shots=set()
	shot=[]
	allshots=[]
	avshots=[]
	pump=[]
	c=PumpCount.query.get(1)
	camt=c.pump_count+1
	sr=Shots.query.all()
	for s in sr:
		shots.add(s.shot_name)
	total=len(shots)
	for s in shots:
		sk=Shots.query.filter_by(shot_name=s).all()
		iamt=len(sk)
		if iamt<camt:
			shot.append(s)
	shot.sort()
	for s in shot:
		sk=Shots.query.filter_by(shot_name=s).first()
		allshots.append(sk.shot_name)
	#convert pump images to ingredient names then putting into a list
	for count in range(1,camt):
		a=Pumps.query.get(count)
		ai=AllIngredients.query.filter_by(ingredient_image=a.ingredient).first()
		pump.append(ai.ingredient)
	for av in allshots:
		sk=Shots.query.filter_by(shot_name=av).all()
		ti=len(sk)
		avck=[]
		for c in sk:
			for p in pump:
				if p==c.shot_ingredient:
					avck.append("yes!")
		ack=len(avck)
		if ack==ti:
			avshots.append(av)
		tz=len(avshots)
		
	return render_template("avdrinks.html",drtype='Shots',profile='sprofile',avdrinks=avshots,tz=tz)

@app.route("/addcabinet/<ingredient>",methods= ['GET' , 'POST'])
def addcabinet(ingredient):
	form=MyCabinetForm()
	if form.validate_on_submit():
		own=request.form.getlist('owners')
        	owner=own[0]
        	if owner=='other':
        		owner=request.form['newowner']
		ci=AllIngredients.query.filter_by(ingredient=ingredient).first()
		ckc=MyCabinet.query.filter_by(ingredient=ci.ingredient_image,owner=owner).first()
		if ckc is not None:
			flash("{} is already in {}'s liquor Cabinet".format(ingredient,owner),"warning")
			return redirect(url_for('home'))
		cab=MyCabinet(ingredient=ci.ingredient_image,owner=owner)
        	db.session.add(cab)
        	db.session.commit()
        	if form.addmore.data==True:
        		flash("{} has been added to {}'s Cabinet".format(ingredient,owner),"success")
                	return redirect(url_for('loadpump'))
        	flash("{} has been added to {}'s Cabinet".format(ingredient,owner),"success")
        	return redirect(url_for('home'))


	owners=set()
	myc=MyCabinet.query.all()
	if myc is None:
		pass
	else:
		for me in myc:
			owners.add(me.owner)
		
	
	
	owners.add("other")

	return render_template("add2mycabinet.html",ingredient=ingredient,owners=owners,form=form)

@app.route("/whoscabinet", methods=['GET','POST'])
def whoscabinet():
        if request.method=='GET':
        	owners=set()
	        myc=MyCabinet.query.all()
	        for m in myc:
		        owners.add(m.owner)
	        return render_template("choosewhoscabinet.html",owners=owners)
        elif request.method=='POST':
		bottles=[]
                name = request.form.getlist('owners')
		owner=name[0]
                ck=MyCabinet.query.filter_by(owner=owner).all()
		for c in ck:
			n=AllIngredients.query.filter_by(ingredient_image=c.ingredient).first()
			bottles.append({"image":c.ingredient,"name":n.ingredient})

		return render_template("cabinet.html",bottles=bottles,owner=owner,title="My Cabinet")

		
                return redirect(url_for('home'))
		

@app.route("/viewmycabinet",methods=['POST'])
def viewmycabinet(owner):
	bottles=[]
	my=MyCabinet.query.filter_by(owner=owner).all()
	for c in my:
		bottles.append(c.ingredient)
	return render_template("viewmycabinet.html",bottles=bottles,owner=owner)

@app.route("/link_image")
def link_image():
	missingpics=[]
	misspic=[]
	np=AllIngredients.query.filter_by(ingredient_image='nopic.gif').all()
	for p in np:
		misspic.append(p.ingredient)
	misspic.sort()
	for  pic in misspic:
		c=AllIngredients.query.filter_by(ingredient=pic).first()
		missingpics.append(c.id)
		missingpics.append(c.ingredient)
	tz=len(missingpics)
	return render_template("missingpics.html",missingpics=missingpics,tz=tz)

def save_picture(form_picture):
    picture_fn = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/drinks', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn


@app.route("/link_image/<id>",methods=['GET','POST'])
def linked_image(id):
	form=LinkImageForm()
	if form.validate_on_submit():
		li=AllIngredients.query.get(int(id))

		li.ingredient_image = save_picture(form.ingredient_image.data)
		db.session.commit()

		flash("{}'s image has been updated!".format(li.ingredient),"success")
		return redirect(url_for('home'))

	li=AllIngredients.query.get(int(id))
	ingredient=li.ingredient
	return render_template("updateimage.html",form=form,ingredient=ingredient,id=id)

@app.route("/cabinetdrinks/<owner>")
def cabinetdrinks(owner):
	#create list for cabinet
	cabinet=[]
	mycabinet=[]
	mc=MyCabinet.query.filter_by(owner=owner).all()
	for m in mc:
		cabinet.append(m.ingredient)
	#the list is pic filename turn them into ingredient names
	for c in cabinet:
		d=AllIngredients.query.filter_by(ingredient_image=c).first()
		mycabinet.append(d.ingredient)
	drinks=set()
	drink=[]
	alldrinks=[]
	avdrinks=[]
	adrinks=[]
	c=PumpCount.query.get(1)
	camt=c.pump_count+1
        dr=Drinks.query.all()

        for d in dr:
		drinks.add(d.drink_name)
        total=len(drinks)
	
	for d in drinks:
		dk=Drinks.query.filter_by(drink_name=d).all()
		
		iamt=len(dk)
		
		if iamt<camt:
			drink.append(d)
	drink.sort()
	for d in drink:
		dk=Drinks.query.filter_by(drink_name=d).first()
		alldrinks.append(dk.drink_name)
	
	for av in alldrinks:
		ck=Drinks.query.filter_by(drink_name=av).all()
		ti=len(ck)
		avck=[]
		#checks each ingredient to see if it's there has to all be in order to make it
		for c in ck:
			print c.drink_ingredient
			for p in mycabinet:
				if p==c.drink_ingredient:
					avck.append("yes!")
		ack=len(avck)
		if ack==ti:
			adrinks.append(av)
		#to use profile 4 and not make another web page
		#one more list
		print adrinks
	for a in adrinks:
		myc=Drinks.query.filter_by(drink_name=a).first()
		avdrinks.append(myc.id)
		avdrinks.append(myc.drink_name)
	tz=len(avdrinks)
	return render_template("avcdrinks.html",drtype='Drinks',profile='profile4',avdrinks=avdrinks,tz=tz)

@app.route("/cabinetshots/<owner>")
def cabinetshots(owner):
	#creat list for cabinet
	cabinet=[]
	mycabinet=[]
	mc=MyCabinet.query.filter_by(owner=owner).all()
	for m in mc:
		cabinet.append(m.ingredient)
	#the list is pic filename turn them into ingredient names
	for c in cabinet:
		d=AllIngredients.query.filter_by(ingredient_image=c).first()
		mycabinet.append(d.ingredient)
	shots=set()
	shot=[]
	allshots=[]
	avshots=[]
	ashots=[]
	pump=[]
	c=PumpCount.query.get(1)
	camt=c.pump_count+1
	sr=Shots.query.all()
	for s in sr:
		shots.add(s.shot_name)
	total=len(shots)
	for s in shots:
		sk=Shots.query.filter_by(shot_name=s).all()
		iamt=len(sk)
		if iamt<camt:
			shot.append(s)
	shot.sort()
	for s in shot:
		sk=Shots.query.filter_by(shot_name=s).first()
		allshots.append(sk.shot_name)
	#convert pump images to ingredient names then putting into a list
	for count in range(1,camt):
		a=Pumps.query.get(count)
		ai=AllIngredients.query.filter_by(ingredient_image=a.ingredient).first()
		pump.append(ai.ingredient)
	for av in allshots:
		sk=Shots.query.filter_by(shot_name=av).all()
		ti=len(sk)
		avck=[]
		for c in sk:
			for p in mycabinet:
				if p==c.shot_ingredient:
					avck.append("yes!")
		ack=len(avck)
		if ack==ti:
			ashots.append(av)
	#to use profile 4 and not make another web page
	#one more list
	for a in ashots:
		myc=Shots.query.filter_by(shot_name=a).first()
		avshots.append(myc.id)
		avshots.append(myc.shot_name)
	tz=len(avshots)
	return render_template("avcdrinks.html",drtype='Shots',profile='profile5',avdrinks=avshots,tz=tz)

@app.route("/remove/<owner>/<ingredient>")
def remove(owner,ingredient):
	cd=MyCabinet.query.filter_by(ingredient=ingredient,owner=owner).first()
	ingredient=cd.ingredient
	id=cd.id
	return render_template("removefromcabinet.html",ingredient=ingredient,id=id)

@app.route("/removecabinet/<id>")
def removecabinet(id):
	ri=MyCabinet.query.get(id)
	owner=ri.owner
	ingredient=ri.ingredient
	db.session.delete(ri)
	db.session.commit()
	flash("{} has been removed from {}'s Cabinet".format(ingredient,owner), "success")
	return redirect(url_for('home'))

@app.route("/makingdrink",methods=['POST'])
def makingdrink():
	#first make a empty list for which pin and how long
	making=[]
	#next get the number of pumps
	cc=PumpCount.query.get(1)
	pumpcount=cc.pump_count
	#next get the drink's name
	drinkno=request.form['drinkname']
	d=Drinks.query.get(int(drinkno))
	drinkname=d.drink_name
	#convert the ingredient image to the ingredient name

	for chambr in range(1,pumpcount+1):
		cb=Pumps.query.get(chambr)
		#get the pin to the pump
		making.append(cb.pinout)
		#get the ingredient in the pump and find out 
		#how much is needed in the drink
		i=AllIngredients.query.filter_by(ingredient_image=cb.ingredient).first()
		di=Drinks.query.filter_by(drink_name=drinkname,drink_ingredient=i.ingredient).first()
		#if what's in the pump isn't needed...
		if di is None:
			making.pop()
		else:
			amt=float(di.ingredient_amt)
			#convert the amount into lengh of how long the
			#pump is to run
			amount=caltime(amt,cb.flow)
			making.append(amount)

	pour(making)
	return redirect(url_for('home'))
@app.route("/custom/<ingredient>",methods=['GET','POST'])
def custom(ingredient):
	if request.method=='GET':
		i=AllIngredients.query.filter_by(ingredient=ingredient).first()
		ingredient_image=i.ingredient_image
		return render_template("customdrink.html",ingredient=ingredient,ingredient_image=ingredient_image)
	elif request.method=='POST':
		amt=request.form['quantity']
		ingr=ingredient+';'+amt
		ingredients=ingr.split(';')
		
		return render_template("viewcustom.html",ingr=ingr,ingredients=ingredients)

@app.route("/custom/<ingr>/<nxtingr>",methods=['GET','POST'])
def custom1(ingr,nxtingr):
	if request.method=='GET':
		i=AllIngredients.query.filter_by(ingredient=nxtingr).first()
		ingredient_image=i.ingredient_image
		return render_template("customdrink.html",nxtingr=nxtingr,ingredient_image=ingredient_image)
	elif request.method=='POST':
		amt=request.form['quantity']
		nxtingr=nxtingr+';'+amt
		ingr=ingr+';'+nxtingr
		ingredients=ingr.split(';')
		return render_template("viewcustom.html",ingr=ingr,ingredients=ingredients)



@app.route("/makecustom/<ingr>")
def makecustom(ingr):
	custom=ingr.split(';')
	fixdrink(custom)
	return redirect(url_for('home'))
	

@app.route("/ckcustomdrkname/<ingr>",methods=['GET','POST'])
def ckcustomdrkname(ingr):
	if request.method=='GET':
		return render_template("enterinfo.html",itype='text',stype='Drink Name',ftype='drink')
	elif request.method=='POST':
		drink=request.form['drink']
		ck=Drinks.query.filter_by(drink_name=drink).first()
		if ck is None:
			return redirect(url_for('savecustomdrk',ingr=ingr,drink=drink))
		flash('The name {} already exist. Choose another name'.format(drink),'danger')
		return redirect(url_for('ckcustomdrkname',ingr=ingr))

@app.route("/savcustomdrk/<drink>/<ingr>")
def savecustomdrk(drink,ingr):
	i=ingr.split(';')
	tz=len(i)
	for count in range(0,tz,2):
		custom=Drinks(drink_name=drink,drink_ingredient=i[count],ingredient_amt=i[count+1])
		db.session.add(custom)
		db.session.commit()
	flash('{} has been saved'.format(drink),"info")
	custom=ingr.split(';')
	fixdrink(custom)
	flash('Your custom drink is ready',"success")
	return redirect(url_for('home'))

@app.route("/ckcustomshotname/<ingr>",methods=['GET','POST'])
def ckcustomshotname(ingr):
	if request.method=='GET':
		return render_template("enterinfo.html",stype='Shot Name',itype='text',ftype='drink')
	elif request.method=='POST':
                drink=request.form['drink']
                ck=Shots.query.filter_by(shot_name=drink).first()
                if ck is None:
                        return redirect(url_for('savcustomshot',ingr=ingr,drink=drink))
                flash('The name {} already exist. Choose another name'.format(drink),'danger')
                return redirect(url_for('ckcustomshotname',ingr=ingr))

@app.route("/savcustomshot/<drink>/<ingr>")
def savcustomshot(drink,ingr):
	i=ingr.split(';')
        tz=len(i)
        for count in range(0,tz,2):
                custom=Shots(shot_name=drink,shot_ingredient=i[count],ingredient_amt=i[count+1])
                db.session.add(custom)
                db.session.commit()
        flash('{} has been saved'.format(drink),"info")
	custom=ingr.split(';')
	fixdrink(custom)
	flash('Your custom shot is ready',"success")
	return redirect(url_for('home'))


@app.route("/addpump", methods=['GET', 'POST'])
def addpump():
	form=AddPumpForm()
	if form.validate_on_submit():
		flowrate=float(form.flow.data)/10
		addpump=Pumps(ingredient="new.gif",pinout=form.pinout.data,flow=flowrate)
		
		db.session.add(addpump)
		db.session.commit()
		c=PumpCount.query.get(1)
		c.pump_count=c.pump_count+1
		db.session.commit()
		flash("New Pump has been added","success")
		return redirect(url_for('home'))
	c=PumpCount.query.get(1)
	new=c.pump_count
	new=new+1
	return render_template("addpump.html",form=form,new=new)


@app.route("/confirmpump")
def confirmpump():
	ch=PumpCount.query.get(1)
	dc=Pumps.query.get(ch.pump_count)
	return render_template("delpump.html",dc=dc)


@app.route("/confirm/delete/<id>", methods=['POST'])
def delete_pump(id):
	delch=Pumps.query.get(id)
	db.session.delete(delch)
	c=Pumps.query.count()
	cc=PumpCount.query.get(1)
	cc.pump_count=c
	db.session.commit()
	flash("Pump has been deleted!","success")
	return redirect(url_for('home'))

@app.route("/pump/update")
def chupdate():
	pumps=[]
	ch=Pumps.query.all()
	for c in ch:
		pumps.append(c.id)
		pumps.append(c.pinout)
		flow=c.flow*10
		#to remove the decimal point
		flow=int(flow)
		pumps.append(flow)
	tz=len(pumps)
	return render_template("seepumps.html",pumps=pumps,tz=tz)


@app.route("/pump/reset/<id>" ,methods=['GET','POST'])
def creset(id):
	if request.method=='GET':
		rc=Pumps.query.get(id)
		oldpin=rc.pinout
		oldflow=rc.flow
		flowrate=0	
		return render_template("resetpump.html",oldpin=oldpin,oldflow=oldflow,rc=rc,flowrate=flowrate)
	elif request.method=='POST':
		r=Pumps.query.get(id)
		pinout=request.form['pin']
		flowrate=request.form['flow']
		if pinout=='':
			pass
		else:
			old=r.pinout
			r.pinout=pinout
			db.session.commit()
			flash ("Pump {}'s pin  has been changed from {} to {}".format(id,old,pinout), "success")
		if flowrate=='':
				pass
		else:
			
			old=r.flow
			flowrate=float(flowrate)
			flowrate=flowrate/10
			r.flow=flowrate
			db.session.commit()
			flash ("Pump {}'s flow rate  has been changed from {} to {}".format(id,old,r.flow), "success")
		return redirect(url_for('home'))

@app.route("/flushpump", methods=['GET','POST'])
def fpump():
	if request.method=='GET':
		c=PumpCount.query.get(1)
		pumps=int(c.pump_count)+1
		return render_template("flushpumps.html",pumps=pumps)
	elif request.method=='POST':
		making=[]
		
	 	ch=request.form.getlist('pump')
		c=len(ch)
		cc=PumpCount.query.get(1)
                chs=int(cc.pump_count)+1
		
		if c==0 :
			for count in range(1,chs):
				cn=Pumps.query.get(count)
				making.append(cn.pinout)
				amount=caltime(1,cn.flow)
                       		making.append(amount)
		for f in ch:
			cn=Pumps.query.get(f)
			making.append(cn.pinout)
			amount=caltime(.50,cn.flow)
			making.append(amount)
		pour(making)
		return redirect(url_for('home'))


@app.route("/drinks/update")
def update_drinks():
	
	drinks=set()
	drink=[]
	alldrinks=[]
	
        dr=Drinks.query.all()

        for d in dr:
		drinks.add(d.drink_name)
	for dk in drinks:
		drink.append(dk)
	drink.sort()
	for d in drink:
		dr=Drinks.query.filter_by(drink_name=d).first()
		alldrinks.append(dr.id)
		alldrinks.append(d)
	tz=len(alldrinks)
	return render_template("updatedrinks.html",drtype='drinks',alldrinks=alldrinks,tz=tz)


@app.route("/drinks/update/<id>")
def drinkupdate(id):
	ingredients=[]
	d=Drinks.query.get(int(id))
	drinkname=d.drink_name
	dr=Drinks.query.filter_by(drink_name=drinkname).all()

	for d in dr:
		ingredients.append({"id":d.id,"ingredient":d.drink_ingredient,"amount":d.ingredient_amt})
	remove='/drinks/delete/'+drinkname
	return  render_template("updatedrink.html", remove=remove,drtype='drink',drinkname=drinkname, ingredients=ingredients,id=id)	

@app.route("/ingredients/update")
def ingrupdate():
	ingredients=[]
	allingr=[]
	il=AllIngredients.query.all()
	#create a file to sort
	for i in il:
		ingredients.append(i.ingredient)
	ingredients.sort()
	#add id to sorted file
	for ingredient in ingredients:
		ingr=AllIngredients.query.filter_by(ingredient=ingredient).first()
		allingr.append(ingr.id)
		allingr.append(ingr.ingredient)

	tz=len(allingr)
	return render_template("updateingredients.html",allingr=allingr,tz=tz)



@app.route("/ingredients/confirm/<id>")
def ingrconfirm(id):
	indrinks=[]
	inshots=[]
	ingred=AllIngredients.query.get(id)
	ingredient=ingred.ingredient
	pic=ingred.ingredient_image
	drinks=Drinks.query.filter_by(drink_ingredient=ingredient).all()
	for i in drinks:
		indrinks.append(i.drink_name)
	shots=Shots.query.filter_by(shot_ingredient=ingredient).all()
	for i in shots:
		inshots.append(i.shot_name)
	dc=len(indrinks)
	sc=len(inshots)

	return render_template("deleteingredient.html",pic=pic,ingredient=ingredient,indrinks=indrinks,inshots=inshots,id=id,dc=dc,sc=sc)


@app.route("/ingredients/delete/<id>")
def ingrdelete(id):
	ingredient=AllIngredients.query.get(id)
	db.session.delete(ingredient)
	db.session.commit()
	flash('{} has been deleted!'.format(ingredient.ingredient),'success')
	return redirect(url_for('home'))



@app.route("/drinks/delete/<drinkname>",methods=['POST'])
def delete_drink(drinkname):
	
	deleteme=Drinks.query.filter_by(drink_name=drinkname).all()
	for d in deleteme:
		k=Drinks.query.get(d.id)
		db.session.delete(k)
		db.session.commit()
	flash("{} has been deleted!".format(drinkname),"success")
	return redirect(url_for('home'))

@app.route("/drink/updated/<id>")
def update_ingr(id):
	ingr=Drinks.query.get(id)
	task=url_for('updateingr',id=id)
	return render_template("drinkupdate.html",drinkname=ingr.drink_name,task=task,ingredient=ingr.drink_ingredient,
	amt=ingr.ingredient_amt,id=ingr.id)


@app.route("/ingredient/delete/<id>",methods=['POST'])
def delingr(id):
	k=Drinks.query.get(id)
	d=Drinks.query.filter_by(drink_name=k.drink_name).first()
	i=k.drink_ingredient
	db.session.delete(k)
	db.session.commit()
	flash("{} has been deleted!".format(i),"success")
	return redirect(url_for('drinkupdate',id=d.id))

@app.route("/ingredient/update/<id>",methods=['GET','POST'])
def updateingr(id):
	if request.method=='GET':
		u=Drinks.query.get(id)
	
		return render_template("chgingredient.html",ingredient=u.drink_ingredient,drinkname=u.drink_name,
		amt=u.ingredient_amt)
	elif request.method=='POST':
		amount=request.form['amount']
		c=Drinks.query.get(id)
		old=c.ingredient_amt
		c.ingredient_amt=amount
		db.session.commit()
		flash("{} in {} has been change from {} to {}".format(c.drink_ingredient,c.drink_name,old,c.ingredient_amt),"success")
		return redirect(url_for('drinkupdate',id=c.id))

@app.route("/ingredient/shot/update/<id>",methods=['GET','POST'])
def updateingr2(id):
	if request.method=='GET':
		u=Shots.query.get(id)
		return render_template("chgingredient.html",u=u)
	elif request.method=='POST':
		amount=request.form['amount']
		c=Shots.query.get(id)
		old=c.ingredient_amt
		c.ingredient_amt=amount
		db.session.commit()
		flash("{} in {} has been change from {} to {}".format(c.shot_ingredient,c.shot_name,old,c.ingredient_amt),"success")
		return redirect(url_for('shotupdate',id=c.id))




@app.route("/update_menu")
def update_menu():
	options=[]
        options.append('/drinks/update')
        options.append('/static/barpi/updatedrinks.jpg')
        options.append('/shots/update')
        options.append('/static/barpi/updateshots.jpg')
        options.append('/ingredients/update')
        options.append('/static/barpi/dingredient.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)



@app.route("/shots/update")
def update_shots():
	
	shots=set()
	shot=[]
	allshots=[]
	
        dr=Shots.query.all()

        for d in dr:
		shots.add(d.shot_name)
	for dk in shots:
		shot.append(dk)
	shot.sort()
	for d in shot:
		dr=Shots.query.filter_by(shot_name=d).first()
		allshots.append(dr.id)
		allshots.append(d)
	tz=len(allshots)
	return render_template("updatedrinks.html",drtype='shots',alldrinks=allshots,tz=tz)


@app.route("/shots/update/<id>")
def shotupdate(id):
	ingredients=[]
	d=Shots.query.get(int(id))
	shotname=d.shot_name
	dr=Shots.query.filter_by(shot_name=shotname).all()

	for d in dr:
		ingredients.append({"id":d.id,"ingredient":d.shot_ingredient,"amount":d.ingredient_amt})
	remove='/shots/delete/'+shotname
	return  render_template("updatedrink.html", remove=remove,drtype='shot',drinkname=shotname, ingredients=ingredients,id=id)
	
	
@app.route("/shot/updated/<id>")
def update_ingr2(id):
	ingr=Shots.query.get(id)
	task=url_for('updateingr2',id=id)
	return render_template("drinkupdate.html",task=task,drinkname=ingr.shot_name,ingredient=ingr.shot_ingredient,
        amt=ingr.ingredient_amt,id=ingr.id)


@app.route("/shots/delete/<shotname>",methods=['POST'])
def delete_shot(shotname):

        deleteme=Shots.query.filter_by(shot_name=shotname).all()
        for d in deleteme:
                k=Shots.query.get(d.id)
                db.session.delete(k)
                db.session.commit()
        flash("{} has been deleted!".format(shotname),"success")
        return redirect(url_for('home'))

@app.route("/ingredient/shot/delete/<id>",methods=['POST'])
def delingr2(id):
        k=Shots.query.get(id)
        d=Shots.query.filter_by(shot_name=k.shot_name).first()
        i=k.shot_ingredient
        db.session.delete(k)
        db.session.commit()
        flash("{} has been deleted!".format(i),"success")
        return redirect(url_for('shotupdate',id=d.id))


@app.route("/setshaker", methods=['GET' , 'POST'])
def setshaker():
	if request.method=='GET':
		return render_template("shaker.html")
	elif request.method =='POST':
		shot_amt = request.form['drinkno']
		shots=set()
		shot=[]
		allshots=[]
		avshots=[]
		pump=[]
		c=PumpCount.query.get(1)
		camt=c.pump_count+1
		sr=Shots.query.all()
		for s in sr:
			shots.add(s.shot_name)
		total=len(shots)
		for s in shots:
			sk=Shots.query.filter_by(shot_name=s).all()
			iamt=len(sk)
			if iamt<camt:
				shot.append(s)
		shot.sort()
		for s in shot:
			sk=Shots.query.filter_by(shot_name=s).first()
			allshots.append(sk.shot_name)
		#convert pump images to ingredient names then putting into a list
		for count in range(1,camt):
			a=Pumps.query.get(count)
			ai=AllIngredients.query.filter_by(ingredient_image=a.ingredient).first()
			pump.append(ai.ingredient)
		for av in allshots:
			sk=Shots.query.filter_by(shot_name=av).all()
			ti=len(sk)
			avck=[]
			for c in sk:
				for p in pump:
					if p==c.shot_ingredient:
						avck.append("yes!")
			ack=len(avck)
			if ack==ti:
				avshots.append(av)
		tz=len(avshots)
		print  avshots

		return render_template("avdrinks.html", drtype='Shots',
		multi='yes',avshots=avshots, tz=tz,shot_amt=shot_amt,ep='st8')

@app.route("/sprofile2/<drinkname>/<shot_amt>/<ep>")
def sprofile2(drinkname,shot_amt,ep):
	ingredients=[]
	dr=Shots.query.filter_by(shot_name=drinkname).all()
	nshots=int(shot_amt)
	dk=Shots.query.filter_by(shot_name=drinkname).first()
	id=dk.id
	for d in dr:
		
		amt=d.ingredient_amt*nshots
		ingredients.append(d.shot_ingredient+"  "+str(amt))
	
	return render_template("shotprofile.html",ingredients=ingredients,drinkname=drinkname,id=id,typ='multiple',shot_amt=shot_amt,ep=ep)
@app.route("/makingshot/<typ>/<shot_amt>/<ep>",methods=['POST'])
def makingshot(typ,shot_amt,ep):
	#note: 
	#when making a drink or a shot ingredient MUST be in the pumps!

	#first make a empty list for which pin and how long
	making=[]
	#next get the number of pumps
	cc=PumpCount.query.get(1)
	pumpcount=cc.pump_count
	#next get the shot's name
	drinkno=request.form['drinkname']
	d=Shots.query.get(int(drinkno))
	drinkname=d.shot_name
	#convert the ingredient image to the ingredient name

	for chambr in range(1,pumpcount+1):
		cb=Pumps.query.get(chambr)
		#get the pin to the pump
		making.append(cb.pinout)
		#get the ingredient in the pump and find out 
		#how much is needed in the drink
		i=AllIngredients.query.filter_by(ingredient_image=cb.ingredient).first()
		di=Shots.query.filter_by(shot_name=drinkname,shot_ingredient=i.ingredient).first()
		#if what's in the pump isn't needed...
		#it is removed
		if di is None:
			making.pop()
		else:
			if typ=='multiple':
				amt=float(di.ingredient_amt*int(shot_amt))
			else:
				
				amt=float(di.ingredient_amt)
			#convert the amount into lengh of how long the
			#calulated in functions.py - caltime
			amount=caltime(amt,cb.flow)
			making.append(amount)

	pour(making)
	if ep=='st8':
		return redirect(url_for('home'))

	return redirect(url_for(ep))



@app.route("/games_menu")
def games_menu():
	options=[]
        options.append('/games-choose_shot')
        options.append('/static/barpi/chooseshot.jpg')
        options.append('/view_games')
        options.append('/static/barpi/vgames.jpg')
        options.append('/games_settings')
        options.append('/static/barpi/gamesettings.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)



@app.route("/games_settings")
def game_settings():
	options=[]
        options.append('/tos/createcard')
        options.append('/static/barpi/toscard.jpg')
        options.append('/drinkif/questions')
        options.append('/static/barpi/drinkifq.jpg')
        options.append('/neverhave/questions')
        options.append('/static/barpi/neverhaveq.jpg')
        options.append('/wtw/addliquors')
        options.append('/static/barpi/addwtw.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)



@app.route("/view_games")
def view_games():
	options=[]
        options.append('/ckgameshot/tos')
        options.append('/static/barpi/tos.jpg')
        options.append('/ckgameshot/drink_if')
        options.append('/static/barpi/drinkif.jpg')
        options.append('/ckgameshot/neverhave')
        options.append('/static/barpi/neverhave.jpg')
        options.append('/wtw')
        options.append('/static/barpi/water.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)


@app.route("/drinkif")
def drink_if():
	return render_template("drink_if.html")


@app.route("/drinkif/instructions")
def diinstructions():
	return render_template("di_instructions.html")


@app.route("/drinkif/questions", methods=['GET','POST'])
def di_questions():
	form=QuestionForm()
	if form.validate_on_submit():
		level=request.form['level']
		cat=request.form.getlist('categories')
		type=cat[0]
		if type=='other':
                        type=request.form['category']

		drink=DrinkIf(question=form.question.data,level=level,type=type)
		db.session.add(drink)
		db.session.commit()
		flash("Your question has been saved","success")
		return redirect(url_for('drink_if'))
	cat=set()
	categories=[]
	dq=DrinkIf.query.all()
	if dq is None:
		pass
	else:
		for q in dq:
			cat.add(q.type)
	for c in cat:
		categories.append(c)
	categories.sort()
	categories.append("other")
	return render_template("drinkifquestionaire.html",categories=categories,form=form,drinkgame='Drink If...')


@app.route("/neverhave")
def neverhave():
	return render_template("neverhave.html")


@app.route("/neverhave/instructions")
def nhinstructions():
        return render_template("nh_instructions.html")

@app.route("/neverhave/questions", methods=['GET','POST'])
def nh_questions():
        form=QuestionForm()
        if form.validate_on_submit():
                level=request.form['level']
                cat=request.form.getlist('categories')
                type=cat[0]
		if type=='other':
			type=request.form['category']

                drink=NeverHave(question=form.question.data,level=level,type=type)
                db.session.add(drink)
                db.session.commit()
                flash("Your question has been saved","success")
                return redirect(url_for('neverhave'))
        cat=set()
        categories=[]
        dq=NeverHave.query.all()
        if dq is None:
                pass
        else:
                for q in dq:
                        cat.add(q.type)
        for c in cat:
                categories.append(c)
        categories.sort()
        categories.append("other")
        return render_template("drinkifquestionaire.html",categories=categories,form=form,drinkgame='Never Have I ever....')

@app.route("/neverhave/play", methods=['GET','POST'])
def never_have_play():
        if request.method=='GET':
                cat=set()
                categories=[]
                di=NeverHave.query.all()
                for d in di:
                        cat.add(d.type)
                for c in cat:
                        categories.append(c)
                categories.sort()
                return render_template("di-playsettings.html",categories=categories)
	if request.method=='POST':
                questions=[]
                categories=request.form.getlist('cat')
                level=request.form.getlist('level')
                l=len(level)
                if l==0:
                        flash(" You missed adding a level are you drunk or something? Try again!","warning")
                        return redirect(url_for('never_have_play'))
                for category in categories:
                        ca=NeverHave.query.filter_by(type=category,level=level[0]).all()
                        for c in ca:
                                questions.append(c.question)
                q=len(questions)
                if q==0:
                        question="played this game"
                        return render_template("question.html",question=question,typed="Never have I ever...",goback="/ckgameshot/neverhave")
                question=random.choice(questions)
                return render_template("question.html",question=question,typed="Never have I ever...",goback="/ckgameshot/neverhave")




@app.route("/drinkif/play", methods=['GET','POST'])
def drinkif_play():
	if request.method=='GET':
		cat=set()
		categories=[]
		di=DrinkIf.query.all()
		for d in di:
			cat.add(d.type)
		for c in cat:
			categories.append(c)
		categories.sort()
		return render_template("di-playsettings.html",categories=categories)
	if request.method=='POST':
		questions=[]
		categories=request.form.getlist('cat')
		level=request.form.getlist('level')
		l=len(level)
		if l==0:
			flash(" You missed adding a level are you drunk or something? Try again!","warning")
			return redirect(url_for('drinkif_play'))
		for category in categories:
			ca=DrinkIf.query.filter_by(type=category,level=level[0]).all()
			for c in ca:
				questions.append(c.question)
		q=len(questions)
		if q==0:
			question="you are playing this game"
			return render_template("question.html",question=question,typed="Drink If...",goback="/ckgameshot/drink_if")
		question=random.choice(questions)
		return render_template("question.html",question=question,typed="Drink If...",goback="/ckgameshot/drink_if")
		flash ("{}".format(question),"success")
		return redirect(url_for('home'))

@app.route("/carol")
def carousel():
	return render_template("carousel.html")

@app.route("/tos")
def tos():
	return render_template("tos.html")


@app.route("/tos/createcard", methods=['GET','POST'])
def createcard():
	form=CreateCardForm()
	title='Truth or Shots'
	if form.validate_on_submit():
		print form.card_image.data
		if form.card_image.data:
                               picture_file = save_cardpicture(form.card_image.data)
		print picture_file
		colors=set()
		color=[]
		fonts=[]
		cc=Colors.query.all()
		#set colors(not fonts)and using a set to elimate dupes
		for c in cc:
			colors.add(c.color_code)
		#convert to a list
		for clr in colors:
			color.append(clr)
		card=random.choice(color)
		#now get the font then randomize it
		cf=Colors.query.filter_by(color_code=card).all()
		for f in cf:
			fonts.append(f.font)
		font=random.choice(fonts)
	
		tos=TruthorShots(ctitle=form.ctitle.data,font=font,question=form.question.data,card=card,pic=picture_file)
		db.session.add(tos)
		db.session.commit()
		return redirect(url_for('ckcard'))

	return render_template("createcard.html",form=form,drinkgame='Truth or Shots',title=title)

@app.route("/tos/ckcard")
def ckcard():
	#get the last entry to view
	descending=TruthorShots.query.order_by(TruthorShots.id.desc())
	last=descending.first()
	return render_template("tos-view.html",last=last)

@app.route("/tos/chgcolors")
def chgcolors():
		#get the last entry to view
        	descending=TruthorShots.query.order_by(TruthorShots.id.desc())
        	last=descending.first()

		colors=set()
                color=[]
                fonts=[]
                cc=Colors.query.all()
                #set colors(not fonts)and using a set to elimate dupes
                for c in cc:
                        colors.add(c.color_code)
                #convert to a list
                for clr in colors:
                        color.append(clr)
                card=random.choice(color)
                #now get the font then randomize it
                cf=Colors.query.filter_by(color_code=card).all()
                for f in cf:
                        fonts.append(f.font)
                last.font=random.choice(fonts)
		last.card=card
		return render_template("tos-view.html",last=last)

@app.route("/tos/play")
def tos_play():
	count=TruthorShots.query.count()
	card=random.randint(1,count)
	tos=TruthorShots.query.get(card)

	return render_template("tos-play.html",tos=tos)

@app.route("/tos/update/<card>/<font>",methods=['GET','POST'])
def tos_update(card,font):
	#get the last entry to view
	descending=TruthorShots.query.order_by(TruthorShots.id.desc())
        last=descending.first()
	chg=TruthorShots.query.get(last.id)
	chg.font=font
	chg.card=card
	print chg.card+" change"
	db.session.commit()
	flash("You card has been saved!","success")
	return redirect(url_for('tos'))



@app.route("/tos/instructions")
def tos_info():
	return render_template("tos_instructions.html")

@app.route("/games-choose_shot")
def choose_shot():
	gs=GameShot.query.get(1)
	gt=Shots.query.filter_by(shot_name=gs.shot_name).first()
	drinkname=gs.shot_name
	return render_template("ckgameshot.html",drinkname=drinkname,id=gt.id)

@app.route("/ckgameshot/<ep>")
def ckgameshot(ep):
	gs=GameShot.query.all()
	
	for g in gs:
		print g.shot_ingredient
		si=AllIngredients.query.filter_by(ingredient=g.shot_ingredient).first()
		ckb=Pumps.query.filter_by(ingredient=si.ingredient_image).first()
		if ckb is None:
			flash("Game Shot is not loaded in the liquor cabinet","warning")
			return redirect(url_for('choose_shot',ep=ep))
	
	if ep == 'drink_if' or ep == 'neverhave':
			return redirect(url_for('setplayers',ep=ep))

	return redirect(url_for(ep))


@app.route("/games-shot_change/<drinkname>")
def change_gameshot(drinkname):
	gs=GameShot.query.filter_by(shot_name=drinkname).all()
	for g in gs:
		
		db.session.delete(g)
		db.session.commit()
	alldrinks=allshots2()
        tz=len(alldrinks)
        return render_template("alldrinks.html",profile='profile9',drtype='Shots',alldrinks=alldrinks,tz=tz)

@app.route("/games/setplayers/<ep>", methods=['GET','POST'])
def setplayers(ep):
	if request.method=='GET':
		if ep=='drink_if':
			game='Drink If...'
		if ep=='neverhave':
			game='Never have I ever...'
		return render_template("setplayers.html",game=game)
	if request.method=='POST':
		shot_amt=request.form['drinkno']
		if shot_amt=='0':
			flash("{}".format(ep),"danger")
			return redirect(url_for(ep))
		else:
			gs=GameShot.query.get(1)
			return redirect(url_for('sprofile2',drinkname=gs.shot_name,shot_amt=shot_amt,ep=ep))


@app.route("/tos/drink")
def tos_drink():
	pics=[]
	sp=ShamePics.query.all()
	for p in sp:
		pics.append(p.pic)
	pic=random.choice(pics)
	custom=[]
        sht=GameShot.query.all()
        for s in sht:
                custom.append(s.shot_ingredient)
                custom.append(s.ingredient_amt)
        fixdrink(custom)

	return render_template("tos_drink.html",pic=pic)




@app.route("/tos/shamepic",methods=['GET','POST'])
def shamepic():
	form=ShameImageForm()
	if form.validate_on_submit():
		pic = save_shamepicture(form.pic.data)
		sp=ShamePics(pic=pic)
		db.session.add(sp)
		db.session.commit()
		flash("your image has been saved!","success")
		return redirect(url_for('view_games'))

	return render_template("shameimage.html",form=form)

@app.route("/wtw")
def wtw():
	return render_template("wtw.html")

@app.route("/wtw/instructions")
def wtwinstructions():
	return render_template("wtw_instructions.html")

@app.route("/wtw/addliquors")
def addliqours():
	ingredients=[]
	li=AllIngredients.query.order_by("ingredient")
	for i in li:
		ingredients.append(i.id)
		ingredients.append(i.ingredient_image)
	tz=len(ingredients)
	return render_template("addliquors.html",ingredients=ingredients, tz=tz)

@app.route("/wtw/addliquor/<id>")
def addliquor(id):
	i=AllIngredients.query.get(id)
	liquor=Wtw(ingredient=i.ingredient)
	db.session.add(liquor)
	db.session.commit()
	flash("{} has been added to the Where's the water list".format(i.ingredient),"success")
	return redirect(url_for('wtw'))

@app.route("/wtw/ck")
def wtwck():
	ckingr=[]
	cked=[]
	liq=Wtw.query.all()

	for l in liq:
		s=AllIngredients.query.filter_by(ingredient=l.ingredient).first()
		for count in range(1,4):
			c=Pumps.query.get(count)

			if c.ingredient==s.ingredient_image:
				ckingr.append(s.ingredient_image)

	ck=len(ckingr)
	if ck!=3:
		flash("Set up liquor Cabinet first","info")
		return redirect(url_for('wtw_set'))
	return redirect(url_for('wtw_play'))




@app.route("/wtw/set",methods=['GET','POST'])
def wtw_set():
	if request.method=='GET':
		liquors=Wtw.query.order_by("ingredient")
			
		return render_template("wtw-set.html",liquors=liquors)
	elif request.method=='POST':
		liquor=[]
		liquors=request.form.getlist('liq')
		for liq in liquors:
			l=Wtw.query.get(int(liq))
			p=AllIngredients.query.filter_by(ingredient=l.ingredient).first()
			liquor.append(p.ingredient_image)

		liquor.append('water.gif')
		a=1
		for l in liquor:
			c=Pumps.query.get(a)
			if c is None:
				pass
			else:
				c.ingredient=l
				db.session.commit()
			a=a+1
		flash("Liquors are set","success")
		return redirect(url_for('wtw_play'))


@app.route("/wtw/play",methods=['GET','POST'])
def wtw_play():
	making=[]
	pick=[]
	for count in range(1,4):
		p=Pumps.query.get(count)
		pick.append(p.ingredient)
	choice=(random.choice(pick))
	c=Pumps.query.filter_by(ingredient=choice).first()
	making.append(c.pinout)
	#hiding the answer 
	
	answer="12384711"+str(c.pinout)+"2923032adkfhs"
	making.append(33.0)
	pour(making)
	return render_template("wtw-choose.html",answer=answer)
	
@app.route("/wtw/play/<answer>/<ranswer>")
def wtw_answer(answer,ranswer):
	#decode the answer
	re=ranswer[8:]
	t=len(re)
	ra=re[:t-13]
	real=Pumps.query.filter_by(pinout=int(ra)).first()
	if real.ingredient!='water.gif':
		ranswer='notwater'
	else:
		ranswer='water'
	if answer==ranswer:
		pics=[]
        	sp=RightPics.query.all()
        	for p in sp:
        	        pics.append(p.pic)
        	pic=random.choice(pics)
		result='You got it right!'
		making=rchoice()
		pour(making)
        	return render_template("wtw-results.html",pic=pic,result=result)

	else:
		pics=[]
                sp=WrongPics.query.all()
                for p in sp:
                        pics.append(p.pic)
                pic=random.choice(pics)
		result="You're wrong you have to take a drink"
		making=rchoice()
                pour(making)

                return render_template("wtw-results.html",pic=pic,result=result)


@app.route("/wtw/add/response",methods=['GET','POST'])
def responsepic():
        form=ResponseImageForm()
        if form.validate_on_submit():
                pic = save_responsepicture(form.pic.data)
                if form.response.data==True:
			response='right'
			sp=RightPics(pic=pic)
			db.session.add(sp)
                        db.session.commit()
		else:
			response='wrong'
			sp=WrongPics(pic=pic)
                	db.session.add(sp)
                	db.session.commit()
                flash("your {} image has been saved!".format(response),"success")
                return redirect(url_for('wtw'))
	return render_template("responseimage.html",form=form)

@app.route("/favorite")
def faves():
	options=[]
        options.append('/favorite/choose')
        options.append('/static/barpi/cfav.jpg')
        options.append('/dfavorites')
        options.append('/static/barpi/dfav.jpg')
        options.append('/mfavorites')
        options.append('/static/barpi/mfav.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)




@app.route("/favorite/choose")
def fchoose():
	options=[]
	options.append('/favorite/drink/search')
	options.append('/static/barpi/favdrink.jpg')
	options.append('/favorite/shot/search')
	options.append('/static/barpi/favshot.jpg')
	tz=len(options)
        return render_template("menu.html",options=options,tz=tz)

@app.route("/dfavorites")
def dfavorites():
	options=[]
        options.append('/favorite/drink/name')
        options.append('/static/barpi/favdrink.jpg')
        options.append('/favorite/shot/name')
        options.append('/static/barpi/favshot.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)



@app.route("/mfavorites")
def mfavs():
	options=[]
        options.append('/favorite/make/drink')
        options.append('/static/barpi/favdrink.jpg')
        options.append('/favorite/make/shot')
        options.append('/static/barpi/favshot.jpg')
        tz=len(options)
        return render_template("menu.html",options=options,tz=tz)



@app.route("/favorite/drink/search")
def favdrink():
	return redirect(url_for('alldrinks'))


@app.route("/favorite/shot/search")
def favshot():
        return redirect(url_for('allshots'))

@app.route("/favorite/make/drink")
def mname():
	name=set()
        names=[]
        dn=FavoriteDrink.query.all()
        for n in dn:
                name.add(n.owner)
        for n in name:
                names.append(n)
        names.sort()
        return render_template("makefavs.html",names=names,type="drink")

@app.route("/favorite/make/shot")
def mname2():
	name=set()
        names=[]
        dn=FavoriteShot.query.all()
        for n in dn:
                name.add(n.owner)
        for n in name:
                names.append(n)
        names.sort()
        return render_template("makefavs.html",names=names,type="shot")


@app.route("/favorite/make/drink/<owner>/check")
def ckowner(owner):
	ck=FavoriteDrink.query.filter_by(owner=owner).all()
        for c in ck:
                i=AllIngredients.query.filter_by(ingredient=c.drink_ingredient).first()
                di=Pumps.query.filter_by(ingredient=i.ingredient_image).first()
                if di is None:
			pumppics=[]
			for l in ck:
				i=AllIngredients.query.filter_by(ingredient=l.drink_ingredient).first()
				pumppics.append(i.ingredient_image)
				
			return render_template("autoload.html",pumppics=pumppics,makeit='yes',owner=owner,type="drink")
	

	return redirect(url_for('mowner',owner=owner))




@app.route("/favorite/make/drink/<owner>/loaded")
def mloaded(owner):
	pics=[]
	fd=FavoriteDrink.query.filter_by(owner=owner).all()
	for p in fd:
		i=AllIngredients.query.filter_by(ingredient=p.drink_ingredient).first()
		pics.append(i.ingredient_image)

	
	a=1
	for pic in pics:
		print pic
		c=Pumps.query.get(a)
		c.ingredient=pic
		db.session.commit()
		a=a+1
	flash("Ingredients are locked and loaded","success")
	return redirect(url_for('mowner',owner=owner))


@app.route("/favorite/make/shot/<owner>/loaded")
def mloaded2(owner):
        pics=[]
        fd=FavoriteShot.query.filter_by(owner=owner).all()
        for p in fd:
                i=AllIngredients.query.filter_by(ingredient=p.shot_ingredient).first()
                pics.append(i.ingredient_image)


        a=1
        for pic in pics:
                print pic
                c=Pumps.query.get(a)
                c.ingredient=pic
                db.session.commit()
                a=a+1
        flash("Ingredients are locked and loaded","success")
        return redirect(url_for('mowner2',owner=owner))



@app.route("/favorite/make/shot/<owner>/check")
def ckowner2(owner):

	ck=FavoriteShot.query.filter_by(owner=owner).all()
        for c in ck:
                i=AllIngredients.query.filter_by(ingredient=c.shot_ingredient).first()
                di=Pumps.query.filter_by(ingredient=i.ingredient_image).first()
                if di is None:
			pumppics=[]
			for l in ck:
				i=AllIngredients.query.filter_by(ingredient=l.shot_ingredient).first()
				pumppics.append(i.ingredient_image)
				
			return render_template("autoload.html",pumppics=pumppics,makeit='yes',owner=owner,type="shot")
		return redirect(url_for('mowner2',owner=owner))






@app.route("/favorite/make/drink/<owner>")
def mowner(owner):
	custom=[]
	mk=FavoriteDrink.query.filter_by(owner=owner).all()
	for m in mk:
		custom.append(m.drink_ingredient)
		custom.append(m.ingredient_amt)
	fixdrink(custom)
	
	flash("You make it this far","success")
	return redirect(url_for('home'))


@app.route("/favorite/make/shot/<owner>")
def mowner2(owner):
	custom=[]
	mk=FavoriteShot.query.filter_by(owner=owner).all()
	for m in mk:
		custom.append(m.shot_ingredient)
		custom.append(m.ingredient_amt)
	fixdrink(custom)
	flash("It's done, Drink up!","success")

        return redirect(url_for('home'))




@app.route("/favorite/drink/name")
def dname():
	name=set()
	names=[]
	dn=FavoriteDrink.query.all()
	for n in dn:
		name.add(n.owner)
	for n in name:
		names.append(n)
	names.sort()
	return render_template("deletefavs.html",names=names,type="drink")

@app.route("/favorite/shot/name")
def dname2():
        name=set()
        names=[]
        dn=FavoriteShot.query.all()
        for n in dn:
                name.add(n.owner)
        for n in name:
                names.append(n)
        names.sort()
        return render_template("deletefavs.html",names=names,type="shot")



@app.route("/favorite/Drink", methods=['POST'])
def fdrink():
	drinkid= request.form['drinkname']
	d = Drinks.query.get(int(drinkid))
	drinkname=d.drink_name
	return render_template("fav.html",drtype='drink',drinkname=drinkname)


@app.route("/favorite/Shot", methods=['POST'])
def fshot():
	shotid= request.form['drinkname']
	s = Shots.query.get(int(shotid))
	drinkname=s.shot_name
	return render_template("fav.html",drtype='shot',drinkname=drinkname)


@app.route("/favorite/drink/<drinkname>/add", methods=['POST'])
def favadd(drinkname):
		owner=request.form['name']

		dr=Drinks.query.filter_by(drink_name=drinkname).all()
		for d in dr:
			fav=FavoriteDrink(drink_ingredient=d.drink_ingredient,ingredient_amt=d.ingredient_amt,owner=owner)
			db.session.add(fav)
			db.session.commit()
		flash("{} is now listed as {}'s Favorite Drink".format(drinkname,owner),"success")
		return redirect(url_for('home'))


@app.route("/favorite/shot/<shotname>/add", methods=['POST'])
def favadd2(shotname):
                owner=request.form['name']

                dr=Shots.query.filter_by(shot_name=shotname).all()
                for d in dr:
                        fav=FavoriteShot(shot_ingredient=d.shot_ingredient,ingredient_amt=d.ingredient_amt,owner=owner)
                        db.session.add(fav)
                        db.session.commit()
                flash("{} is now listed as {}'s Favorite Shot".format(shotname,owner),"success")
                return redirect(url_for('home'))


@app.route("/favorite/drink/<owner>/delete")
def favdel(owner):
	df=FavoriteDrink.query.filter_by(owner=owner).all()
	for d in df:
		kf=FavoriteDrink.query.get(d.id)
		db.session.delete(kf)
		db.session.commit()
	flash("{}'s favorite drink has been removed".format(owner),"success")
	return redirect(url_for('home'))

@app.route("/favorite/shot/<owner>/delete")
def favdel2(owner):
	df=FavoriteShot.query.filter_by(owner=owner).all()
	for d in df:
		kf=FavoriteShot.query.get(d.id)
		db.session.delete(kf)
		db.session.commit()
	flash("{}'s favorite shot has been removed".format(owner),"success")
        return redirect(url_for('home'))

@app.route("/make/shot/<sht>")
def makeshot(sht):
	shot=sht.title()
	print shot
	custom=[]
	ms=Shots.query.filter_by(shot_name=shot).all()
	for s in ms:
		custom.append(s.shot_ingredient)
		custom.append(s.ingredient_amt)
	fixdrink(custom)
	return redirect(url_for('home'))

@app.route("/oops/<making>")
def oops(making):
        return render_template("oops.html",makiing=making)

@app.route("/fix_oops/<making>")
def fix_oops(making):
        pour(making)
        flash("It's ready!","success")
        return redirect(url_for('home'))


