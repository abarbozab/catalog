from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

#Items form Category Soccer
category = Category(user_id=1, name="Soccer")
session.add(category)
session.commit()

item = Item(user_id=1, category=category, title="Two shinguards",
             description='''The shin guard was inspired by the concept of a greave. A greave is a piece of armor
                          used to protect the shin. It is a Middle English term, derived from an Old French word,
                          greve (pronounced gri\'v), meaning shin or shin armor.[1] The etymology of this word not
                          only describes the use and purpose of shin guards, but also contributes to dating the
                          technology.''')
session.add(item)
session.commit()

item = Item(user_id=1, category=category, title="Jersey",
             description='''A jersey is an item of knitted clothing, traditionally in wool or cotton, with sleeves,
             worn as a pullover, as it does not open at the front, unlike a cardigan. It is usually close-fitting
             and machine knitted in contrast to a guernsey that is more often hand knit with a thicker yarn.
             The word is usually used interchangeably with sweater..''')
session.add(item)
session.commit()

item = Item(user_id=1, category=category, title="Soccer Cleats",
             description='''Cleats or studs are protrusions on the sole of a shoe, or on an external attachment to a
             shoe, that provide additional traction on a soft or slippery surface. In American English the term
             cleats is used synecdochically to refer to shoes featuring such protrusions. This does not happen in
             British English; the term 'studs' is never used to refer to the shoes, which would instead be known as
             'football boots', ''')
session.add(item)
session.commit()

#Items form Category BasketBall
category = Category(user_id=1, name="BasketBall")
session.add(category)
session.commit()

#Items form Category Baseball
category = Category(user_id=1, name="Baseball")
session.add(category)
session.commit()

item = Item(user_id=1, category=category, title="Bat",
             description='''A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the
             ball after it is thrown by the pitcher. By regulation it may be no more than 2.75 inches in diameter at
             the thickest part and no more than 42 inches (1,100 mm) long. Although historically bats approaching 3
             pounds (1.4 kg) were swung,[1] today bats of 33 ounces (0.94 kg) are common, topping out at 34 ounces
             (0.96 kg) to 36 ounces (1.0 kg)''')
session.add(item)
session.commit()

#Items form Category Frisbee
category = Category(user_id=1, name="Frisbee")
session.add(category)
session.commit()

item = Item(user_id=1, category=category, title="Frisbee",
             description='''A flying disc is a disc-shaped gliding toy or sporting item that is generally plastic and
             roughly 20 to 25 centimetres (8 to 10 in) in diameter with a lip,[1] used recreationally and competitively
             for throwing and catching, for example, in flying disc games. The shape of the disc, an airfoil in
             cross-section, allows it to fly by generating lift as it moves through the air while spinning. The term
             Frisbee, often used to generically describe all flying discs, is a registered trademark of the Wham-O toy
             company. Though such use is not encouraged by the company, the common use of the name as a generic term
             has put the trademark in jeopardy; accordingly, many "Frisbee" games are now known as "disc" games, like
             Ultimate or disc golf''')
session.add(item)
session.commit()

#Items form Category Snowboarding
category = Category(user_id=1, name="Snowboarding")
session.add(category)
session.commit()

item = Item(user_id=1, category=category, title="Goggles",
             description='''Goggles or safety glasses are forms of protective eyewear that usually enclose or protect
             the area surrounding the eye in order to prevent particulates, water or chemicals from striking the eyes.
             They are used in chemistry laboratories and in woodworking. They are often used in snow sports as well,
             and in swimming. Goggles are often worn when using power tools such as drills or chainsaws to prevent
             flying particles from damaging the eyes. Many types of goggles are available as prescription goggles
             for those with vision problems.''')
session.add(item)
session.commit()

item = Item(user_id=1, category=category, title="Snowboard",
             description='''Snowboards are boards that are usually the width of one\'s foot longways, with the ability
             to glide on snow.[1] Snowboards are differentiated from monoskis by the stance of the user. In monoskiing,
             the user stands with feet inline with direction of travel (facing tip of monoski/downhill) (parallel to
              long axis of board), whereas in snowboarding, users stand with feet transverse (more or less) to the
             longitude of the board. Users of such equipment may be referred to as snowboarders.''')
session.add(item)
session.commit()

#Items form Category Rock Climbing
category = Category(user_id=1, name="Rock Climbing")
session.add(category)
session.commit()

#Items form Category Foosball
category = Category(user_id=1, name="Foosball")
session.add(category)
session.commit()

#Items form Category Skating
category = Category(user_id=1, name="Skating")
session.add(category)
session.commit()

#Items form Category Hockey
category = Category(user_id=1, name="Hockey")
session.add(category)
session.commit()

item = Item(user_id=1, category=category, title="Stick",
             description='''A hockey stick is a piece of equipment used in field hockey, ice hockey , roller hockey
             or underwater hockey to move the ball or puck''')
session.add(item)
session.commit()

print "added menu items!"

