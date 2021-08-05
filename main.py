import sqlite3
from random import choice

"""
format date time
add info func
add last edited attribute
complete readme
"""

conn = sqlite3.connect("notes.db")
global cur
cur = conn.cursor()

def start():
	print("""
█▄░█ █▀█ ▀█▀ █▀▀ █ ▀█▀
█░▀█ █▄█ ░█░ ██▄ █ ░█░""")
	try:
		command = """
		CREATE TABLE notestable(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT UNIQUE NOT NULL,
		content TEXT,
		created DATETIME)
		"""
		cur.execute(command)
		conn.commit()
		print("Welcome to 𝑁𝑜𝑡𝑒𝐼𝑡")
		print("\nTABLE 'notestable' CREATED SUCCESSFULLY")
	except sqlite3.OperationalError:
		print("Welcome back to 𝑁𝑜𝑡𝑒𝐼𝑡")
	print("\n'help' to view all available commands and how to use them")
	user()

def new_note():
	title = input("TITLE(Press ENTER to cancel): ")
	if len(title) == 0:
		print("No new notes have been created")
		user()
	else:
		content = input("CONTENT: ")
		if len(content) == 0:
			content = title
		command = """
		INSERT INTO notestable(title, content, created)
		VALUES ('{t}', '{c}', CURRENT_TIMESTAMP)
		""".format(t = title, c = content)
		try:
			cur.execute(command)
			conn.commit()
			print("𝑁𝑜𝑡𝑒𝐼𝑡ed")
		except:
			print("There is already a note with the same title!")
		user()

def list_notes():
	command = """
	SELECT * FROM notestable
	"""
	cur.execute(command)
	result = cur.fetchall()
	if len(result) > 0:
		note_num = 1
		for i in result:
			print(f"{note_num}) {i[1]}")
			note_num += 1
	else:
		print("This place is empty. Feel free to add notes here using 'new'")
	user()

def view_note():
	note_title_list = user_input[1:]
	note_title = " ".join(note_title_list)
	if len(note_title) == 0:
		print("'help' to view all available commands and how to use them")
		user()
	else:
		command = """
		SELECT * FROM notestable WHERE title = '{t}'
		""".format(t = note_title)
		cur.execute(command)
		result = cur.fetchall()
		title = result[0][1]
		content = result[0][2]
		note_date = result[0][3][:10]
		note_time = result[0][3][11:16]
		note = """\n\tTITLE: {t}\t{n_t}\t{n_d}\n\t{c}
		""".format(t = title, n_t = note_time, n_d = note_date,c = content)
		print(note)
		user()

def edit_note():
	note_title_list = user_input[1:]
	note_title = " ".join(note_title_list)
	new_title = input("NEW TITLE(Press ENTER to leave it as it is): ")
	new_content = input("NEW CONTENT(Press ENTER to leave it as it is): ")
	if len(new_title) == 0 and len(new_content) == 0:
		print("NO edits have been made")
		user()
	elif len(new_title) == 0 and len(new_content) > 0:
		command = """
		UPDATE notestable
		SET content = '{n_c}'
		WHERE title = '{t}'
		""".format(n_c = new_content, t = note_title)
	else:
		command = """
		UPDATE notestable
		SET title = '{n_t}', content = '{n_c}'
		WHERE title = '{t}'
		""".format(n_t = new_title, n_c = new_content, t = note_title)
	cur.execute(command)
	conn.commit()
	print("1 edit has been made")
	user()

def delete_note():
	note_title_list = user_input[1:]
	note_title = " ".join(note_title_list)
	if len(note_title) == 0:
		print("No notes have been deleted")
		user()
	else:
		command = """
		DELETE FROM notestable WHERE title = '{t}'
		""".format(t = note_title)
		cur.execute(command)
		conn.commit()
		print("DELETED SUCCESSFULLY")
		user()

def info():
	pass

def exit():
	exit_text = [
	"Adios",
	"See ya later, alligator",
	"Bye bye",
	"Au revoir",
	"Hasta la vista",
	"Peace out",
	"Hasta luego"
	]
	print(choice(exit_text))

def help_func():
	help_screen = """
	Commands			Description
	------------------------------------------------------------------------
	new            			Create a new note
	list           			List all the notes that you have created
	view <note title>		Expand a note
	edit <note title>		Edit a note
	delete <note title>		Delete a note
	exit/quit			Exit NoteIt
	help 				View available commands
	"""
	print(help_screen)
	user()

def user():
	global user_input
	user_input = input("\n𝑁𝑜𝑡𝑒𝐼𝑡 -> ").split()
	user_command = user_input[0]
	commands = {
	"new": new_note,
	"list": list_notes,
	"view": view_note,
	"edit": edit_note,
	"delete": delete_note,
	"exit": exit,
	"quit": exit,
	"help": help_func
	}
	try:
		func = commands.get(user_command)
		return func()
	except:
		print("No such commands found")
		print("'help' to view all available commands and how to use them")
		user()

start()

cur.close()
conn.close()