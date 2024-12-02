import json
import xml.etree.ElementTree as ET

def convert_json_to_xmi(json_file, xmi_file):
    try:
        # Leer el archivo JSON generado por PlantUML
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Crear el elemento raíz del XMI
        xmi = ET.Element('xmi:XMI', {
            'xmlns:xmi': "http://www.omg.org/XMI",
            'version': "2.1"
        })

        # Crear el elemento principal para las clases
        uml_model = ET.SubElement(xmi, 'uml:Model', {
            'xmi:type': "uml:Model",
            'name': "GeneratedModel"
        })

        # Iterar sobre las clases en el JSON
        for element in data.get('elements', []):
            if element.get('type') == 'class':
                class_element = ET.SubElement(uml_model, 'packagedElement', {
                    'xmi:type': "uml:Class",
                    'name': element.get('name', 'UnnamedClass')
                })

                # Agregar atributos a la clase
                for attribute in element.get('fields', []):
                    ET.SubElement(class_element, 'ownedAttribute', {
                        'xmi:type': "uml:Property",
                        'name': attribute.get('name', 'UnnamedAttribute'),
                        'type': attribute.get('type', 'String')
                    })

                # Agregar métodos a la clase
                for method in element.get('methods', []):
                    ET.SubElement(class_element, 'ownedOperation', {
                        'xmi:type': "uml:Operation",
                        'name': method.get('name', 'UnnamedMethod')
                    })

        # Convertir a cadena de texto XMI
        tree = ET.ElementTree(xmi)
        tree.write(xmi_file, encoding="utf-8", xml_declaration=True)

        print(f"XMI generado exitosamente en {xmi_file}")

    except Exception as e:
        print(f"Error durante la conversión: {e}")

# Ruta del archivo JSON generado y del archivo XMI de salida
json_file = f'K:\\Development\\CURSOS\\UNIANDES\\Modulo 3\\Proyecto_3_kcgomez\\diagrama.json'
xmi_file = f'K:\\Development\\CURSOS\\UNIANDES\\Modulo 3\\Proyecto_3_kcgomez\\plantuml_export.puml'

# Llamar a la función para convertir
convert_json_to_xmi(json_file, xmi_file)
