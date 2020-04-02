
from ssaw.designer import create_questionnaire, export_questionnaire


myquest = create_questionnaire('Some title', defaultsection=True)

s1 = myquest.Children[0]  # first section
s1.add_statictext('this is a static text', hideifdisabled=True)


q = s1.add_question(variablename='var1', questiontext='text', mask='##--')
q.add_validation('1> 2', 'always false')

yesnoquestions = [
    ['Do you have a fridge?', 'fridge'],
    ['Do you have a car?', 'car'],
    ['Do you have a stereo?', 'stereo']
]
for item in yesnoquestions:
    q = s1.add_question(questiontext=item[0], variablename=item[1], questiontype=0)
    q.add_option('1', 'Yes')
    q.add_option('2', 'No')

q = s1.add_question(questiontext='this is multichoice quest', questiontype=3, yesno=True)
q.add_option('1', 'do you like apples?')
q.add_option('2', 'do you like oranges?')
q.add_option('3', 'both?')

s1.add_question(questiontype=4, questiontext='numeric quest', isinteger=True)

myquest.add_macro(name='macro1', content='3>4')
myquest.add_macro(name='macro2', content='1>4', description='second macro')

#myquest.add_lookuptable(tablename='table1', filename='170209.txt')

#myquest.add_attachment(name='picture', filename="c:\\temp\\avatar-2.png")

#myquest.add_translation(name='random', filename="c:\\temp\\965976b6d7144d07b8bf0c9d16599d20.xlsx")

export_questionnaire(myquest, ".")