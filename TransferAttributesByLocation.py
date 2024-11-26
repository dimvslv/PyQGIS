from qgis.core import QgsProject, QgsField, edit
from PyQt5.QtCore import QVariant

layer1_name = 'гос_долг_пост_rec4'      # Имя слоя с атрибутами
layer2_name = 'rec_in_gos_wgs_43n_4'    # Имя слоя, куда нужно добавить атрибуты

# Загрузите слои
layer1 = QgsProject.instance().mapLayersByName(layer1_name)[0]
layer2 = QgsProject.instance().mapLayersByName(layer2_name)[0]

# Поля для записи атрибутов (добавляются в layer2)
field_name1 = 'kad_num'  # Поле для кадастрового номера
field_name2 = 'kad_area'  # Поле для площади
field_name3 = 'percent'  # Поле для площади

# Добавляем поле для кадастрового номера, если его нет
if field_name1 not in [field.name() for field in layer2.fields()]:
    layer2.dataProvider().addAttributes([QgsField(field_name1, QVariant.String)])  # Кадастровый номер
    layer2.updateFields()

# Добавляем поле для площади, если его нет
if field_name2 not in [field.name() for field in layer2.fields()]:
    layer2.dataProvider().addAttributes([QgsField(field_name2, QVariant.Double)])  # Площадь
    layer2.updateFields()
    
if field_name3 not in [field.name() for field in layer2.fields()]:
    layer2.dataProvider().addAttributes([QgsField(field_name3, QVariant.Double)])  # Процент
    layer2.updateFields()

# Переносим атрибуты
with edit(layer2):
    for feature2 in layer2.getFeatures():
        geom2 = feature2.geometry()
        for feature1 in layer1.getFeatures():
            geom1 = feature1.geometry()
            if geom1.intersects(geom2):  # Проверяем пересечение
                # Записываем кадастровый номер
                feature2[field_name1] = feature1['kad_num']
                # Записываем площадь
                feature2[field_name2] = feature1['area_m2dec']
                # Записываем процентное соотношение
                feature2[field_name3] = (feature2['area']/feature1['area_m2dec'])*100
        layer2.updateFeature(feature2)

print("Атрибуты успешно перенесены!")