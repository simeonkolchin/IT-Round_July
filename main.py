import qrcode
# пример данных
data = "Мероприятие: IT-Round \nИюль дата: 22 июля \nвремя: 15:00 \nсвободных мест: 67"
# имя конечного файла
filename = "qr.png"
# генерируем qr-код
img = qrcode.make(data)
# сохраняем img в файл
img.save(filename)