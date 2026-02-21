from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget,
    QTextEdit, QInputDialog
)

import json

# notes = {
#     "Welcome!": {
#         'text' : "ini adalah dummy teks",
#         'tags' : ['good', 'note']
#     }
# }

# with open('notes_data.json', 'w') as file:
#     json.dump(notes, file, ensure_ascii=False)


app = QApplication([]) #membuat aplikasi
window = QWidget() #tampilan window
window.setWindowTitle('Smart Notes') #pemberian judul aplikasi
window.resize(900, 600) #ukuran dari aplikasi

#kode dibawah ini membuat object widget semua
list_notes_label = QLabel('List of Notes')
list_notes = QListWidget()

button_note_create = QPushButton('Create note')
button_note_delete = QPushButton('Delete note')
button_note_save = QPushButton('Save note')

list_tags_label = QLabel("List of tags")
list_tags = QListWidget()

field_tag = QLineEdit()
field_tag.setPlaceholderText('Enter tag...')

button_tag_add = QPushButton('Add to note')
button_tag_delete = QPushButton('Untag from note')
button_tag_search = QPushButton('Search notes by tag')

field_text = QTextEdit() #pembuatan teks edit sebelah kiri

#kode dibawah ini untuk membuat layout dan menambahkan widget
main_layout = QHBoxLayout()

left_layout = QVBoxLayout()
left_layout.addWidget(field_text)

right_layout = QVBoxLayout()
right_layout.addWidget(list_notes_label)
right_layout.addWidget(list_notes)

button_Hlayout1 = QHBoxLayout()
button_Hlayout1.addWidget(button_note_create)
button_Hlayout1.addWidget(button_note_delete)

right_layout.addLayout(button_Hlayout1)
right_layout.addWidget(button_note_save)

right_layout.addWidget(list_tags_label)
right_layout.addWidget(list_tags)
right_layout.addWidget(field_tag)

button_Hlayout2 = QHBoxLayout()
button_Hlayout2.addWidget(button_tag_add)
button_Hlayout2.addWidget(button_tag_delete)

right_layout.addLayout(button_Hlayout2)

right_layout.addWidget(button_tag_search)

main_layout.addLayout(left_layout, stretch=2)
main_layout.addLayout(right_layout, stretch=1)
window.setLayout(main_layout)

def show_note(): #function untuk menampilkan catatan
    key = list_notes.selectedItems()[0].text() #mengambil tulisan/teks dari catatan yang kita pilih
    print(key) #print ke terminal untuk memastikan datanya benar atau tidak
    field_text.setText(notes[key]['text']) #memunculkan isi teks ke aplikasi
    list_tags.clear() #menghapus segala data di list tags
    list_tags.addItems(notes[key]['tags']) #memunculkan isi tag ke aplikasi

def add_note(): #menambahkan data catatan
    note_name, ok = QInputDialog.getText(window, 'Add note', 'Note Name:') #membuat input untuk judul catatan
    if ok and note_name != '': #jika klik ok dan judul tidak kosong
        notes[note_name] = {'text' : '', 'tags' : []} #memasukkan data baru ke variabel notes
        list_notes.addItem(note_name) #memperbarui list notes
        list_tags.addItems(notes[note_name]['tags']) #memperbarui lits tag

def save_note(): #function untuk menyimpan update catatan
    if list_notes.selectedItems(): #memastikan jika ada catatan yang dipilih
        key = list_notes.selectedItems()[0].text() #mengambil tulisan/teks dari catatan yang kita pilih
        notes[key]['text'] = field_text.toPlainText() #mengambil update isi catatan untuk disimpan
        with open('notes_data.json', 'w') as file: #menyimpan data di json
            json.dump(notes, file, ensure_ascii=False)
    else:
        print('Tidak ada catatan yang dipilih')

def del_note(): #function untuk menghapus catatan
    if list_notes.selectedItems(): #memastikan jika ada catatan yang dipilih
        key = list_notes.selectedItems()[0].text() #mengambil tulisan/teks dari catatan yang kita pilih
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file: #menyimpan data di json
            json.dump(notes, file, ensure_ascii=False)
    else:
        print('Tidak ada catatan yang dipilih')

def add_tag(): #function untuk menambahkan tag
    if list_notes.selectedItems(): #memastikan jika ada catatan yang dipilih
        key = list_notes.selectedItems()[0].text() #mengambil tulisan/teks dari catatan yang kita pilih
        tag = field_tag.text() #mengambil teks yang ada di input field tag
        if not tag in notes[key]['tags']: #memastikan data tag yang ingin ditambahkan belum ada
            notes[key]['tags'].append(tag) #menambahkan tag ke data
            list_tags.addItem(tag) #memasukkan data tag ke tampilan aplikasi
            field_tag.clear() #menghapus data di input sebelumnya
        with open('notes_data.json', 'w') as file: #menyimpan data di json
            json.dump(notes, file, ensure_ascii=False)
    else:
        print('Tidak ada catatan yang diplilih')

def del_tag(): #function untuk menghapus tag
    if list_notes.selectedItems(): #memastikan jika ada catatan yang dipilih
        key = list_notes.selectedItems()[0].text() #mengambil tulisan/teks dari catatan yang kita pilih
        tag = list_tags.selectedItems()[0].text() #mengambil teks dari list tags yang kita pilih
        notes[key]['tags'].remove(tag) #menghapus tag dari database variabel
        list_tags.clear() #menghapus seluruh data pada tampilan list tags
        list_tags.addItems(notes[key]['tags']) #mengupdate tampilan data di list tags
        with open('notes_data.json', 'w') as file: #menyimpan data di json
            json.dump(notes,file, ensure_ascii=False)
    else:
        print('Tidak ada catatan yang dipilih')

def search_tag(): #function untuk mencari sebuah tag
    tag = field_tag.text() #mengambil teks yang ada di input field tag
    #jika di tombolnya tulisannya adalah cari notes dan ada tag yang sudah masukkan di input
    if button_tag_search.text() == 'Search notes by tag' and tag:
        notes_filter = {} #menyimpan data sementara dari hasil pencarian tag sebelumnya
        for note in notes: #mengambil seluruh catatan menggunakan looping
            if tag in notes[note]['tags']: #jika tag yang dicari ada di database
                notes_filter[note] = notes[note] #memasukkan data notes yang ada di tag ke notes_filter
            button_tag_search.setText('Reset search') #mengganti tulisan pada tombol
            list_notes.clear() #menghapus seluruh data di list catatan
            list_tags.clear() #menghapus seluruh tags di list tags
            list_notes.addItems(notes_filter) #mengupdate data list catata menggunakan note filter
    elif button_tag_search.text() == 'Reset search': #jika tulisan pada tombol adalah reset search
        field_tag.clear() #menghapus tulisan di input
        list_notes.clear() #menghapus seluruh data di list catatan
        list_tags.clear() #menghapus seluruh data di list tags
        list_notes.addItems(notes) #mengembalikan ulang data sebelumnya 
        button_tag_search.setText('Search notes by tag') #mengganti tulisan pada tombol
    else:
        pass



#connect tombol
list_notes.itemClicked.connect(show_note) 
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_delete.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_delete.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

with open('notes_data.json', 'r') as file: #membaca data
    notes = json.load(file) #mengambil data disimpan di variabel notes

list_notes.addItems(notes) #memasukkan data catatan ke tampilan listnya

window.show()
app.exec_()