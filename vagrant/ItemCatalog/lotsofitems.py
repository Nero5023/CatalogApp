from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User
from datetime import datetime
from random import randint

engine = create_engine('sqlite:///categoryitems.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def randomTime():
	return datetime(2015, randint(3,12), randint(1,30), 
				randint(1,23), randint(1,59))


user1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
	picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

category1 = Category(name = 'Soccer')

session.add(category1)
session.commit()

item1 = Item(name='FIFA World Cup', description='''The FIFA World Cup, 
	often simply called the World Cup, is an international association 
	football competition contested by the senior men's national teams 
	of the members of Internationale de Football Association 
	(FIFA), the sport's global governing body. The championship has been 
	awarded every four years since the inaugural tournament in 1930, 
	except in 1942 and 1946 when it was not held because of the Second 
	World War. The current champion is Germany, which won its fourth 
	title at the 2014 tournament in Brazil.The current format of the 
	competition involves a qualification phase, which currently takes 
	place over the preceding three years, to determine which teams qualify 
	for the tournament phase, which is often called the World Cup Finals. 
	32 teams, including the automatically qualifying host nation(s), compete 
	in the tournament phase for the title at venues within the host nation(s) 
	over a period of about a month.''', date_time=randomTime(), 
	category=category1, user=user1, picture='/upload/worldcup.jpg')
session.add(item1)
session.commit()

item2 = Item(name='UEFA Champions League', description='''The UEFA 
	Champions League, known simply as the Champions League, is an 
	annual continental club football competition organised by the 
	Union of European Football Associations (UEFA) and contested by 
	top-division European clubs. It is one of the most prestigious 
	tournaments in the world and the most prestigious club competition
	in European football, played by the national league champion (and,
	for some nations, one or more runners-up) of each UEFA national  
	association. The final of the 2012-13 tournament was the most
	watched UEFA Champions League final to date, as well as the most 
	watched annual sporting event worldwide in 2013, drawing 360 million 
	television viewers.''',
	date_time=randomTime(), category=category1, user=user1, picture='/upload/UEFAChampionsLeague.jpg')
session.add(item2)
session.commit()




category2 = Category(name='Basketball')
session.add(category2)
session.commit()

item3 = Item(name='NBA', description='''The National Basketball Association (NBA) 
	is the pre-eminent men's professional basketball league in North America, 
	and is widely considered to be the premier men's professional basketball 
	league in the world. It has 30 franchised member clubs (29 in the United 
	States and 1 in Canada), and is an active member of USA Basketball (USAB),
	which is recognized by FIBA (also known as the International Basketball Federation)
	 as the national governing body for basketball in the United States. The NBA is 
	 one of the four major North American professional sports leagues. NBA players 
	 are the world's best paid sportsmen, by average annual salary per player.''',
			date_time=randomTime(), category=category2, user=user1, picture='/upload/nba.jpg')
session.add(item3)
session.commit()


item4 = Item(name='Michael Jordan', description='''Michael Jeffrey Jordan 
	(born February 17, 1963), also known by his initials, MJ, 
	is an American former professional basketball player. He is also 
	a businessman, and principal owner and chairman of the Charlotte 
	Hornets. Jordan played 15 seasons in the National Basketball Association 
	(NBA) for the Chicago Bulls and Washington Wizards. His biography on the 
	NBA website states: "By acclamation, Michael Jordan is the greatest 
	basketball player of all time."Jordan was one of the most effectively 
	marketed athletes of his generation and was considered instrumental in 
	popularizing the NBA around the world in the 1980s and 1990s.''',
			date_time=randomTime(), category=category2, user=user1, picture='/upload/jordan.jpg')
session.add(item4)
session.commit()


category3 = Category(name='Baseball')
session.add(category3)
session.commit()

item5 = Item(name='MLB', description='''Major League Baseball (MLB) is a 
	professional baseball organization that is the oldest of the four major 
	professional sports leagues in the United States and Canada. A total of 
	30 teams now play in the American League (AL) and National League (NL), 
	with 15 teams in each league. The AL and NL operated as separate legal 
	entities from 1901 and 1876 respectively. After cooperating but remaining 
	legally separate entities since 1903, in 2000 the leagues merged into a 
	single organization led by the Commissioner of Baseball. The organization 
	also oversees minor league baseball leagues, which comprise about 240 teams 
	affiliated with the major-league clubs. With the World Baseball Softball 
	Confederation, MLB manages the international World Baseball Classic tournament.''',
			date_time=randomTime(), category=category3, user=user1, picture='/upload/mlb.jpg ')
session.add(item5)
session.commit()

category4 = Category(name='Frisbee')
session.add(category4)
session.commit()

item6 = Item(name='Frisbee', description='''A flying disc is a disc-shaped 
	gliding toy or sporting item that is generally plastic and roughly 20 to 
	25 centimetres (8 to 10 in) in diameter with a lip, used recreationally 
	and competitively for throwing and catching, for example, in flying disc games. 
	The shape of the disc, an airfoil in cross-section, allows it to fly by 
	generating lift as it moves through the air while spinning. The term Frisbee,
	often used to generically describe all flying discs, is a registered trademark 
	of the Wham-O toy company. Though such use is not encouraged by the company, 
	the common use of the name as a generic term has put the trademark in jeopardy;
	accordingly, many "Frisbee" games are now known as "disc" games, like Ultimate 
	or disc golf.''',
			date_time=randomTime(), category=category4, user=user1, picture='/upload/flyingdisc.jpg')
session.add(item6)
session.commit()

category5 = Category(name='Snowboarding')
session.add(category5)
session.commit()

item7 = Item(name='Snowboard', description='''Snowboards are boards 
	that are usually the width of one's foot longways, with the ability to 
	glide on snow.[1] Snowboards are differentiated from monoskis by the 
	stance of the user. In monoskiing, the user stands with feet inline with 
	direction of travel (facing tip of monoski/downhill) (parallel to long axis 
	of board), whereas in snowboarding, users stand with feet transverse (more 
	or less) to the longitude of the board. Users of such equipment may be 
	referred to as snowboarders. Commercial snowboards generally require 
	extra equipment such as bindings and special boots which help secure 
	both feet of a snowboarder, who generally rides in an upright position.
	These types of boards are commonly used by people at ski hills or 
	resorts for leisure, entertainment, and competitive purposes in 
	the activity called snowboarding.''', date_time=randomTime(), category=category5,
	user=user1,picture="/upload/snowboard.jpg")
session.add(item7)
session.commit()


category6 = Category(name='Rock Climbing')
session.add(category6)
session.commit()

item8 = Item(name='Kernmantle rope', description='''Kernmantle rope is rope 
	constructed with its interior core (the kern) protected by a woven 
	exterior sheath (mantle) designed to optimize strength, durability,
	 and flexibility. The core fibers provide the tensile strength of the rope,
	  while the sheath protects the core from abrasion during use. The name is
	   derived from the German word Kernmantel, which means core[-and-]jacket.''',
			date_time=randomTime(), category=category6, user=user1, picture='/upload/rope.jpg')
session.add(item8)
session.commit()



category7 = Category(name='Foosball')
session.add(category7)
session.commit()


item9 = Item(name='Table football', description='''Table football, also known as 
	table soccer (as in the German "Tischfubball"), foosball, baby-foot or kicker,
	 is a table-top game, sport, that is loosely based on association football.''',
			date_time=randomTime(), category=category7, user=user1, picture='/upload/tablefootball.jpg')
session.add(item9)
session.commit()

category8 = Category(name='Skating')
session.add(category8)
session.commit()


category9 = Category(name='Hockey')
session.add(category9)
session.commit()

item10 = Item(name='NHL', description='''The National Hockey League (NHL; French: 
	Ligue nationale de hockey-LNH) is a professional ice hockey league composed of
	30 member clubs: 23 in the United States and 7 in Canada. Headquartered in New 
	York City, the NHL is considered to be the premier professional ice hockey league 
	in the world, and one of the major professional sports leagues in the United 
	States and Canada. The Stanley Cup, the oldest professional sports trophy in 
	North America, is awarded annually to the league playoff champion at the end 
	of each season.''',
			date_time=randomTime(), category=category9, user=user1, picture='/upload/nhl.jpg')
session.add(item10)
session.commit()

print "Added items!"


