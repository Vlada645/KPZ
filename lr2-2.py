from graphviz import Digraph

# UML-діаграма прецедентів використання
diagram = Digraph(format='png', filename='use_case_diagram_vertical')
diagram.attr(rankdir='TB', size='7,10')

# Актор
diagram.node('User', 'Користувач', shape='actor')

# Прецеденти
diagram.node('UC1', 'Запуск програми', shape='ellipse')
diagram.node('UC2', 'Отримання поточної дати та часу', shape='ellipse')
diagram.node('UC3', 'Додавання нового запису в DataFrame', shape='ellipse')
diagram.node('UC4', 'Збереження DataFrame у CSV', shape='ellipse')
diagram.node('UC5', 'Перегляд збережених записів', shape='ellipse')

# Зв’язки
diagram.edge('User', 'UC1')
diagram.edge('UC1', 'UC2')
diagram.edge('UC2', 'UC3')
diagram.edge('UC3', 'UC4')
diagram.edge('User', 'UC5')

# Рендер
diagram.render('use_case_diagram_vertical.png', format="png", cleanup=True)
print("Діаграму збережено у файл use_case_diagram_vertical.png.")
