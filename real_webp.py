from PIL import ImageColor,Image
import re
import colors

HEADER_REGEX = r"RWP (\d+) (\d+)"

class RealWebP:
    def __init__(self,width:int,height:int) -> None:
        self.width=width
        self.height=height
        self.data=[]
        for i in range(width*height):
            self.data.append("black")

    def get_color(self,x:int,y:int):
        return self.data[x+y*self.width]
    
    def get_rgb(self,x:int,y:int):
        return ImageColor.getcolor(self.get_color(x,y),'RGB')
    
    def save_to_img(self,fname:str):
        img = Image.new("RGB",(self.width,self.height))
        pix = img.load()
        for y in range(self.height):
            for x in range(self.width):
                pix[x,y] = self.get_rgb(x,y)
        img.save(fname)
    
    def load_from_img(self, fname: str, should_dither: bool = False):
        # print("Loading")
        img = Image.open(fname)
        img = img.convert("RGB")
        out = img.quantize(palette=colors.paletteImg, dither=(Image.Dither.FLOYDSTEINBERG if should_dither else Image.Dither.NONE))
        out = out.convert("RGB")
        # out.save("thing.png")
        pix = out.load()
        self.data = []
        self.width = out.width
        self.height = out.height
        # print(f"{self.width=},{self.height=}")
        for y in range(out.height):
            # print(y)
            for x in range(out.width):
                color = pix[x,y]
                color_name = None
                
                for k in colors.COLORS.keys():
                    c = colors.COLORS[k]
                    if color[0] == c[0] and color[1] == c[1] and color[2] == c[2]:
                        color_name = k
                        break
                # print(color_name)
                self.data.append(color_name)
        # print("loaded")
                
    
    def save(self,fname:str):
        with open(fname,'w') as f:
            f.write(f"RWP {self.width} {self.height}\n")
            for y in range(self.height):
                for x in range(self.width):
                    f.write(self.get_color(x,y))
                    f.write(" ")
                f.write("\n")
    
    def load(self,fname:str):
        with open(fname,'r') as f:
            text = f.read()
            lines = text.split("\n")
            first = lines[0]
            lines.pop(0)

            m = re.match(HEADER_REGEX,first)
            self.width = int(m.group(1))
            self.height = int(m.group(2))

            self.data = []
            for line in lines:
                if line.strip(" \t") == "":
                    continue    
                colors = line.split(" ")
                colors = filter(lambda x: x.strip(" \t")!="", colors)
                self.data.extend(colors)


if __name__ == "__main__":
    rwp = RealWebP(0,0)
    rwp.load_from_img("/home/calvin/Pictures/glass monkeys tiny.png",should_dither=True)
    rwp.save("monke.rwp")
    rwp.load("monke.rwp")
    rwp.save_to_img("out.png")
