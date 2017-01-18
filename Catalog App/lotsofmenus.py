from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Shop, Base, MenuItem, User

engine = create_engine('sqlite:///shopbase.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="Ivan Baranov", email="justmetoyou@yandex.ru",
             picture="https://pbs.twimg.com/profile_images/557287123867279362/AHJEXcNA.jpeg")
session.add(User1)
session.commit()

# Item for Adidas
shop1 = Shop(name="Adidas")

session.add(shop1)
session.commit()

menuItem1 = MenuItem(name="ALPHABOUNCE CHINESE NEW YEAR SHOES",
                     description="CUSHIONED RUNNERS THAT HONOR THE LUNAR NEW YEAR.",
                     price="$100", image="adidas/1.jpg", shops=shop1, user_id=1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name="ALPHABOUNCE XENO SHOES",
                     description="SHOES WITH COMFORTABLE CUSHIONING AND AN IRIDESCENT LOOK.",
                     price="$150", image="adidas/2.jpg", shops=shop1, user_id=1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="ALPHABOUNCE SHOES",
                     description="SHOES WITH LONG-LASTING CUSHIONING FOR COMFORT AND FLEXIBILITY.",
                     price="$110", image="adidas/3.jpg", shops=shop1, user_id=1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(name="STAN SMITH SHOES",
                     description="STAN SMITH SHOES",
                     price="$75", image="adidas/4.jpg", shops=shop1, user_id=1)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(name="SUPERSTAR SHOES",
                     description="SUPERSTAR SHOES",
                     price="$80", image="adidas/6.jpg", shops=shop1, user_id=1)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(name="ACE 17.1 FIRM GROUND CLEATS",
                     description="BOSS-LEVEL DOMINANCE. MASTER OF CONTROL.",
                     price="$200", image="adidas/6.jpg", shops=shop1, user_id=1)

session.add(menuItem6)
session.commit()


# Item for Puma
shop2 = Shop(name="Puma")

session.add(shop2)
session.commit()


menuItem1 = MenuItem(user_id=1,
                     name="PUMA BY RIHANNA MENS VELVET CREEPER",
                     description="Rihanna has long been a gamechanger in the creative world - as a singer, a songwriter, an actress, a fashion designer, you name it.",
                     price="$150", image="puma/1.jpg", shops=shop2)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1,
                     name="IGNITE EVOKNIT MENS TRAINING SHOES",
                     description="Unsurpassed wearing comfort is a given with the all-new IGNITE evoKNIT and its form-fitting, mid-height knitted upper.",
                     price="$130", image="puma/2.jpg", shops=shop2)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1,
                     name="PULSE XT V2 FT MENS TRAINING SHOES",
                     description="Our Pulse XT is geared to enhance your boldness. It's more dynamic than any training shoe we've created so far. It's faster",
                     price="$75", image="puma/3.jpg", shops=shop2)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1,
                     name="EVOSPEED SL FRESH FG MENS FIRM GROUND SOCCER CLEATS ",
                     description="Meet the evoSPEED Fresh, an all-new version of the super-light evoSPEED SL. ",
                     price="$180", image="puma/4.jpg", shops=shop2)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1,
                     name="TITANTOUR IGNITE HIGH-TOP MENS GOLF SHOES",
                     description="As made famous by Rickie Fowler himself: the TITANTOUR IGNITE High-Top",
                     price="$220", image="puma/5.jpg", shops=shop2)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user_id=1,
                     name="FERRARI CHANGER IGNITE STATEMENT MENS SHOES",
                     description="When you're racing around tight corners at top speeds, fit is everything.",
                     price="#100", image="puma/6.jpg", shops=shop2)

session.add(menuItem6)
session.commit()

# Item for Nike
shop3 = Shop(name="Nike")

session.add(shop3)
session.commit()


menuItem1 = MenuItem(user_id=1,
                     name="NIKE LUNAR FORCE 1 DUCKBOOT",
                     description="Delivering complete cold-weather protection for all your outdoor pursuits",
                     price="$165", image="nike/1.jpg", shops=shop3)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1,
                     name="NIKE AIR MAX 95 SNEAKERBOOT",
                     description="The Nike Air Max 95 SneakerBoot Men's Boot updates the iconic '90s runner for cold-weather comfort with warm",
                    price="$200", image="nike/2.jpg", shops=shop3)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1,
                     name="NIKE AIR MAX THEA MID",
                     description="The modern Nike Air Max Thea Mid Women's Shoe comes equipped with updated design details for cold-weather comfort.",
                     price="$140", image="nike/3.jpg", shops=shop3)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1,
                     name="CONVERSE CHUCK II WATERPROOF",
                     description="The Converse Chuck II Waterproof Sneaker Boot combines a waterproof upper with plush Nike Lunarlon",
                     price="$140", image="nike/4.jpg", shops=shop3)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1,
                     name="CONVERSE CHUCK TAYLOR ALL STAR LEATHER AND FAUX FUR CHELSEE",
                     description="The Converse Chuck Taylor All Star Leather and Faux Fur Chelsee Boot takes a luxe approach with a supple leather upper",
                     price="$85", image="nike/5.jpg", shops=shop3)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user_id=1,
                     name="NIKE ROSHE MID WINTER STAMINA",
                     description="This Nike Roshe Mid Winter Stamina Big Kids' Shoe transforms the Zen-inspired icon with water-repellent material and tough traction",
                     price="$85", image="nike/6.jpg", shops=shop3)

session.add(menuItem6)
session.commit()



print("added price items!")
