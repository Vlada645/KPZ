import graphviz
from graphviz import Digraph

def create_diagram(diagram_type):
    # Створення об'єкта діаграми
    diagram = Digraph(comment=f'{diagram_type} Diagram')

    # Додавання учасників
    participants = ['T', 'TS', 'O', 'SE', 'M']
    labels = ['Trader', 'Trading System', 'Order', 'Stock Exchange', 'Module']
    for p, l in zip(participants, labels):
        diagram.node(p, l)
    # Визначення взаємодій
    interactions = [
        ('T', 'TS', 'ЗапитПозики (сума, умови)'),
        ('TS', 'O', 'СтворитиБорг (сума, відсотки)'),
        ('O', 'SE', 'РезервуватиКошти()'),
        ('SE', 'T', 'НадатиПозиченіКошти()'),
        ('T', 'M', 'ПовернутиБорг (сума, відсотки)'),
        ('M', 'SE', 'ЗакритиБорг()'),
        ('SE', 'O', 'ОновитиСтатусБоргу()')
    ]

    for start, end, label in interactions:
        diagram.edge(start, end, label)

    # Виведення діаграми
    diagram.render(f'{diagram_type.lower()}_diagram', format='png', view=True)

# Виклик функцій для створення діаграм
create_diagram('Interaction')
create_diagram('Collaboration')
