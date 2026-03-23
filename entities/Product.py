class Product:

    def __init__(self, name: str, price: float, img: str, desc: str, url: str, ref: str, tags: list[str] = []):
        self.name = name
        self.price = price
        self.img = img
        self.desc = desc
        self.url = url
        self.ref = ref
        self.tags = tags

    def get_tags(self):
        return " ".join(self.tags)

     