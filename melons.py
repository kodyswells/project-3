import csv

melon_dict = {}

class Melon:
    def __init__(
        self,
        melon_id,
        common_name,
        price,
        image_url,
        color,
        seedless,
    ):
        self.melon_id = melon_id
        self.common_name = common_name
        self.price = price
        self.image_url = image_url
        self.color = color
        self.seedless = seedless

    def __repr__(self):
        return (
            f"<Melon: {self.melon_id}, {self.common_name}>"
        )

    def price_str(self) -> str:
        return f"${self.price:.2f}"
    
    @classmethod
    def get_by_id(cls, melon_id):
        return melon_dict.get(melon_id)

    @classmethod
    def get_all(cls):
        return list(melon_dict.values())


with open("melons.csv") as csvfile:
    rows = csv.DictReader(csvfile)

    for row in rows:
        melon_id = row['melon_id']
        melon = Melon(
            melon_id,
            row['common_name'],
            float(row['price']),
            row['image_url'],
            row['color'],
            eval(row['seedless'])
        )

        melon_dict[melon_id] = melon

# Test output
print(melon_dict)

def get_by_id(melon_id):

    return melon_dict.get(melon_id)

def get_all():
   return list(melon_dict.values())