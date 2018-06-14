from network import Network
from PIL import Image

network = Network(5, 4, 1)
for i in range(10):
    img = Network.get_image('C:\Windows\Fonts\ITCKRIST.TTF')
    network.force_teach(img)
    print('____________________________')
    img = Network.get_image('C:\Windows\Fonts\CHILLER.TTF')
    network.force_teach(img)
    print('____________________________')
    img = Network.get_image('C:\Windows\Fonts\corbeli.ttf')
    network.force_teach(img)
network.save_weights()
network.load_weights('w.txt')
img = Image.open('test.png')
network.cut_digits(img)
print('=======================')
for i in range(len(network.digits)):
    print(network.fill_network(i))
    network.paint_diagram().show()
