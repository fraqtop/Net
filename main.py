from Net.Network import Net
from PIL import Image

n = Net(5, 4, 1)
# for i in range(5):
#     img = Net.get_image('C:\Windows\Fonts\ITCKRIST.TTF')
#     n.force_teach(img)
#     print('____________________________')
#     img = Net.get_image('C:\Windows\Fonts\CHILLER.TTF')
#     n.force_teach(img)
#     print('____________________________')
#     img = Net.get_image('C:\Windows\Fonts\corbeli.ttf')
#     n.force_teach(img)
# n.save()
n.load('w.txt')
img = Image.open('qwe.png')
n.cut_digits(img)
print('=======================')
for i in range(len(n.digits)):
    print(n.fill_network(i))
    n.paint_diagram().show()
